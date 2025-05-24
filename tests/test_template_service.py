from unittest.mock import Mock

import pytest

from app.services.template_service import TemplateService


class TestTemplateService:
    @pytest.fixture
    def template_service(self):
        """Создает экземпляр TemplateService для тестов"""
        return TemplateService()

    @pytest.fixture
    def mock_managers(self, template_service):
        """Мокает менеджеры конфигураций и шаблонов"""
        template_service.templates_manager = Mock()
        template_service.configs_manager = Mock()
        return template_service

    def test_template_exists_true(self, mock_managers):
        """Тест проверки существования шаблона - положительный сценарий"""
        mock_managers.templates_manager.file_exists.return_value = True

        result = mock_managers.template_exists('test_template')

        assert result is True
        mock_managers.templates_manager.file_exists.assert_called_once_with('test_template.yaml')

    def test_template_exists_false(self, mock_managers):
        mock_managers.templates_manager.file_exists.return_value = False

        result = mock_managers.template_exists('nonexistent_template')

        assert result is False
        mock_managers.templates_manager.file_exists.assert_called_once_with('nonexistent_template.yaml')

    def test_load_template_success(self, mock_managers):
        template_content = 'template content with {{domain}}'
        mock_managers.templates_manager.file_exists.return_value = True
        mock_managers.templates_manager.read_file.return_value = template_content

        result = mock_managers.load_template('test_template')

        assert result == template_content
        mock_managers.templates_manager.file_exists.assert_called_once_with('test_template.yaml')
        mock_managers.templates_manager.read_file.assert_called_once_with('test_template.yaml')

    def test_load_template_not_found(self, mock_managers):
        mock_managers.templates_manager.file_exists.return_value = False

        with pytest.raises(FileNotFoundError) as exc_info:
            mock_managers.load_template('nonexistent_template')

        assert "Template 'nonexistent_template' not found" in str(exc_info.value)
        mock_managers.templates_manager.file_exists.assert_called_once_with('nonexistent_template.yaml')

    def test_generate_slug_domain_with_dots(self, template_service):
        result = template_service.generate_slug_domain('example.com')
        assert result == 'example-com'

    def test_generate_slug_domain_with_underscores(self, template_service):
        result = template_service.generate_slug_domain('test_example.com')
        assert result == 'test-example-com'

    def test_generate_slug_domain_with_hyphens(self, template_service):
        result = template_service.generate_slug_domain('test-example.com')
        assert result == 'test-example-com'

    def test_generate_slug_domain_complex(self, template_service):
        result = template_service.generate_slug_domain('sub_domain.test-site.example.com')
        assert result == 'sub-domain-test-site-example-com'

    def test_process_template_success(self, mock_managers):
        template_content = 'host: {{domain}}\nservice: {{slug_domain}}-service'
        expected_result = '# TEMPLATE_NAME: test_template\nhost: example.com\nservice: example-com-service'

        mock_managers.templates_manager.file_exists.return_value = True
        mock_managers.templates_manager.read_file.return_value = template_content

        result = mock_managers.process_template('test_template', 'example.com')

        assert result == expected_result

    def test_process_template_with_complex_domain(self, mock_managers):
        template_content = 'domain: {{domain}}\nslug: {{slug_domain}}'
        expected_result = (
            '# TEMPLATE_NAME: complex_template\ndomain: sub.test-site.example.com\nslug: sub-test-site-example-com'
        )

        mock_managers.templates_manager.file_exists.return_value = True
        mock_managers.templates_manager.read_file.return_value = template_content

        result = mock_managers.process_template('complex_template', 'sub.test-site.example.com')

        assert result == expected_result

    def test_create_config_from_template_success(self, mock_managers):
        template_content = 'host: {{domain}}'
        mock_managers.templates_manager.file_exists.return_value = True
        mock_managers.templates_manager.read_file.return_value = template_content

        success, message = mock_managers.create_config_from_template('test_template', 'example.com')

        assert success is True
        assert message == "Config created successfully for domain 'example.com'"
        mock_managers.configs_manager.write_file.assert_called_once_with(
            'example.com.yaml', '# TEMPLATE_NAME: test_template\nhost: example.com'
        )

    def test_create_config_from_template_template_not_found(self, mock_managers):
        mock_managers.templates_manager.file_exists.return_value = False

        success, message = mock_managers.create_config_from_template('nonexistent_template', 'example.com')

        assert success is False
        assert message == "Template 'nonexistent_template' not found"
        mock_managers.configs_manager.write_file.assert_not_called()

    def test_create_config_from_template_write_error(self, mock_managers):
        template_content = 'host: {{domain}}'
        mock_managers.templates_manager.file_exists.return_value = True
        mock_managers.templates_manager.read_file.return_value = template_content
        mock_managers.configs_manager.write_file.side_effect = Exception('Write error')

        success, message = mock_managers.create_config_from_template('test_template', 'example.com')

        assert success is False
        assert 'Error creating config: Write error' in message

    def test_create_config_from_template_template_load_error(self, mock_managers):
        mock_managers.templates_manager.file_exists.return_value = True
        mock_managers.templates_manager.read_file.side_effect = Exception('Read error')

        success, message = mock_managers.create_config_from_template('test_template', 'example.com')

        assert success is False
        assert 'Error creating config: Read error' in message
        mock_managers.configs_manager.write_file.assert_not_called()
