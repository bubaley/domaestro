from unittest.mock import Mock, patch

from app.schemas.domain import DomainRegisterRequest, RegenerateRequest
from app.services.domain_service import (
    extract_template_name_from_config,
    list_configs,
    regenerate_configs,
    register_domain,
    validate_domain,
)


class TestExtractTemplateNameFromConfig:
    def test_extract_template_name_success(self):
        config_content = '# TEMPLATE_NAME: test_template\nhost: example.com'
        result = extract_template_name_from_config(config_content)
        assert result == 'test_template'

    def test_extract_template_name_with_spaces(self):
        config_content = '#   TEMPLATE_NAME:   test_template   \nhost: example.com'
        result = extract_template_name_from_config(config_content)
        assert result == 'test_template'

    def test_extract_template_name_no_template(self):
        config_content = 'host: example.com\nport: 80'
        result = extract_template_name_from_config(config_content)
        assert result is None

    def test_extract_template_name_empty_content(self):
        result = extract_template_name_from_config('')
        assert result is None

    def test_extract_template_name_none_content(self):
        result = extract_template_name_from_config(None)
        assert result is None

    def test_extract_template_name_wrong_format(self):
        config_content = '# WRONG_TEMPLATE: test_template\nhost: example.com'
        result = extract_template_name_from_config(config_content)
        assert result is None


class TestRegisterDomain:
    @patch('app.services.domain_service.check_cname_a_record')
    @patch('app.services.domain_service.TemplateService')
    def test_register_domain_success(self, mock_template_service_class, mock_check_dns):
        mock_check_dns.return_value = (True, 'DNS OK')
        mock_template_service = Mock()
        mock_template_service.create_config_from_template.return_value = (True, 'Config created')
        mock_template_service_class.return_value = mock_template_service

        request = DomainRegisterRequest(domain='example.com', template='test_template')

        result = register_domain(request)

        assert result.domain == 'example.com'
        assert result.success is True
        assert result.template == 'test_template'
        assert result.error is None

        mock_check_dns.assert_called_once_with('example.com')
        mock_template_service.create_config_from_template.assert_called_once_with('test_template', 'example.com')

    @patch('app.services.domain_service.check_cname_a_record')
    def test_register_domain_dns_check_failed(self, mock_check_dns):
        mock_check_dns.return_value = (False, 'DNS record not found')

        request = DomainRegisterRequest(domain='example.com', template='test_template')

        result = register_domain(request)

        assert result.domain == 'example.com'
        assert result.success is False
        assert result.error == 'DNS record not found'
        assert result.template == 'test_template'

    @patch('app.services.domain_service.check_cname_a_record')
    @patch('app.services.domain_service.TemplateService')
    def test_register_domain_template_creation_failed(self, mock_template_service_class, mock_check_dns):
        mock_check_dns.return_value = (True, 'DNS OK')
        mock_template_service = Mock()
        mock_template_service.create_config_from_template.return_value = (False, 'Template not found')
        mock_template_service_class.return_value = mock_template_service

        request = DomainRegisterRequest(domain='example.com', template='nonexistent_template')

        result = register_domain(request)

        assert result.domain == 'example.com'
        assert result.success is False
        assert result.error == 'Template not found'
        assert result.template == 'nonexistent_template'


class TestValidateDomain:
    @patch('app.services.domain_service.config_exists')
    def test_validate_domain_config_not_found(self, mock_config_exists):
        mock_config_exists.return_value = False

        request = DomainRegisterRequest(domain='example.com')

        result = validate_domain(request)

        assert result.domain == 'example.com'
        assert result.success is False
        assert result.error == 'Config not found'

    @patch('app.services.domain_service.config_exists')
    @patch('app.services.domain_service.check_cname_a_record')
    @patch('app.services.domain_service.ConfigsManager')
    def test_validate_domain_success(self, mock_configs_manager_class, mock_check_dns, mock_config_exists):
        mock_config_exists.return_value = True
        mock_check_dns.return_value = (True, 'DNS OK')

        mock_configs_manager = Mock()
        mock_configs_manager.read_file.return_value = '# TEMPLATE_NAME: test_template\nhost: example.com'
        mock_configs_manager_class.return_value = mock_configs_manager

        request = DomainRegisterRequest(domain='example.com')

        result = validate_domain(request)

        assert result.domain == 'example.com'
        assert result.success is True
        assert result.template == 'test_template'
        assert result.error is None

    @patch('app.services.domain_service.config_exists')
    @patch('app.services.domain_service.check_cname_a_record')
    @patch('app.services.domain_service.ConfigsManager')
    def test_validate_domain_dns_failed(self, mock_configs_manager_class, mock_check_dns, mock_config_exists):
        mock_config_exists.return_value = True
        mock_check_dns.return_value = (False, 'DNS validation failed')

        mock_configs_manager = Mock()
        mock_configs_manager.read_file.return_value = '# TEMPLATE_NAME: test_template\nhost: example.com'
        mock_configs_manager_class.return_value = mock_configs_manager

        request = DomainRegisterRequest(domain='example.com')

        result = validate_domain(request)

        assert result.domain == 'example.com'
        assert result.success is False
        assert result.error == 'DNS validation failed'
        assert result.template == 'test_template'

    @patch('app.services.domain_service.config_exists')
    @patch('app.services.domain_service.check_cname_a_record')
    @patch('app.services.domain_service.ConfigsManager')
    def test_validate_domain_config_read_error(self, mock_configs_manager_class, mock_check_dns, mock_config_exists):
        mock_config_exists.return_value = True
        mock_check_dns.return_value = (True, 'DNS OK')

        mock_configs_manager = Mock()
        mock_configs_manager.read_file.side_effect = Exception('Read error')
        mock_configs_manager_class.return_value = mock_configs_manager

        request = DomainRegisterRequest(domain='example.com')

        result = validate_domain(request)

        assert result.domain == 'example.com'
        assert result.success is True
        assert result.template is None
        assert result.error is None


class TestListConfigs:
    @patch('app.services.domain_service.list_traefik_configs')
    def test_list_configs(self, mock_list_traefik):
        expected_configs = ['example.com.yaml', 'test.com.yaml']
        mock_list_traefik.return_value = expected_configs

        result = list_configs()

        assert result == expected_configs
        mock_list_traefik.assert_called_once()


class TestRegenerateConfigs:
    @patch('app.services.domain_service.ConfigsManager')
    @patch('app.services.domain_service.TemplateService')
    def test_regenerate_configs_all_success(self, mock_template_service_class, mock_configs_manager_class):
        mock_configs_manager = Mock()
        mock_configs_manager.list_files.return_value = ['example.com.yaml', 'test.com.yaml']
        mock_configs_manager.read_file.side_effect = [
            '# TEMPLATE_NAME: template1\nhost: example.com',
            '# TEMPLATE_NAME: template2\nhost: test.com',
        ]
        mock_configs_manager_class.return_value = mock_configs_manager

        mock_template_service = Mock()
        mock_template_service.template_exists.return_value = True
        mock_template_service.create_config_from_template.return_value = (True, 'Success')
        mock_template_service_class.return_value = mock_template_service

        request = RegenerateRequest()

        result = regenerate_configs(request)

        assert result.total_processed == 2
        assert result.successful == 2
        assert result.failed == 0
        assert len(result.results) == 2

        assert result.results[0].domain == 'example.com'
        assert result.results[0].success is True
        assert result.results[0].template == 'template1'

        assert result.results[1].domain == 'test.com'
        assert result.results[1].success is True
        assert result.results[1].template == 'template2'

    @patch('app.services.domain_service.ConfigsManager')
    @patch('app.services.domain_service.TemplateService')
    def test_regenerate_configs_specific_template(self, mock_template_service_class, mock_configs_manager_class):
        mock_configs_manager = Mock()
        mock_configs_manager.list_files.return_value = ['example.com.yaml', 'test.com.yaml']
        mock_configs_manager.read_file.side_effect = [
            '# TEMPLATE_NAME: template1\nhost: example.com',
            '# TEMPLATE_NAME: template2\nhost: test.com',
        ]
        mock_configs_manager_class.return_value = mock_configs_manager

        mock_template_service = Mock()
        mock_template_service.template_exists.return_value = True
        mock_template_service.create_config_from_template.return_value = (True, 'Success')
        mock_template_service_class.return_value = mock_template_service

        request = RegenerateRequest(template='template1')

        result = regenerate_configs(request)

        assert result.total_processed == 1
        assert result.successful == 1
        assert result.failed == 0
        assert len(result.results) == 1
        assert result.results[0].domain == 'example.com'
        assert result.results[0].template == 'template1'

    @patch('app.services.domain_service.ConfigsManager')
    @patch('app.services.domain_service.TemplateService')
    def test_regenerate_configs_no_template_in_config(self, mock_template_service_class, mock_configs_manager_class):
        mock_configs_manager = Mock()
        mock_configs_manager.list_files.return_value = ['example.com.yaml']
        mock_configs_manager.read_file.return_value = 'host: example.com\nport: 80'
        mock_configs_manager_class.return_value = mock_configs_manager

        mock_template_service = Mock()
        mock_template_service_class.return_value = mock_template_service

        request = RegenerateRequest()

        result = regenerate_configs(request)

        assert result.total_processed == 1
        assert result.successful == 0
        assert result.failed == 1
        assert result.results[0].domain == 'example.com'
        assert result.results[0].success is False
        assert result.results[0].error == 'Template name not found in config'
        assert result.results[0].template is None

    @patch('app.services.domain_service.ConfigsManager')
    @patch('app.services.domain_service.TemplateService')
    def test_regenerate_configs_template_not_exists(self, mock_template_service_class, mock_configs_manager_class):
        mock_configs_manager = Mock()
        mock_configs_manager.list_files.return_value = ['example.com.yaml']
        mock_configs_manager.read_file.return_value = '# TEMPLATE_NAME: nonexistent_template\nhost: example.com'
        mock_configs_manager_class.return_value = mock_configs_manager

        mock_template_service = Mock()
        mock_template_service.template_exists.return_value = False
        mock_template_service_class.return_value = mock_template_service

        request = RegenerateRequest()

        result = regenerate_configs(request)

        assert result.total_processed == 1
        assert result.successful == 0
        assert result.failed == 1
        assert result.results[0].domain == 'example.com'
        assert result.results[0].success is False
        assert result.results[0].error == "Template 'nonexistent_template' not found"
        assert result.results[0].template == 'nonexistent_template'

    @patch('app.services.domain_service.ConfigsManager')
    @patch('app.services.domain_service.TemplateService')
    def test_regenerate_configs_creation_failed(self, mock_template_service_class, mock_configs_manager_class):
        mock_configs_manager = Mock()
        mock_configs_manager.list_files.return_value = ['example.com.yaml']
        mock_configs_manager.read_file.return_value = '# TEMPLATE_NAME: test_template\nhost: example.com'
        mock_configs_manager_class.return_value = mock_configs_manager

        mock_template_service = Mock()
        mock_template_service.template_exists.return_value = True
        mock_template_service.create_config_from_template.return_value = (False, 'Creation failed')
        mock_template_service_class.return_value = mock_template_service

        request = RegenerateRequest()

        result = regenerate_configs(request)

        assert result.total_processed == 1
        assert result.successful == 0
        assert result.failed == 1
        assert result.results[0].domain == 'example.com'
        assert result.results[0].success is False
        assert result.results[0].error == 'Creation failed'
        assert result.results[0].template == 'test_template'

    @patch('app.services.domain_service.ConfigsManager')
    @patch('app.services.domain_service.TemplateService')
    def test_regenerate_configs_exception_handling(self, mock_template_service_class, mock_configs_manager_class):
        mock_configs_manager = Mock()
        mock_configs_manager.list_files.return_value = ['example.com.yaml']
        mock_configs_manager.read_file.side_effect = Exception('Read error')
        mock_configs_manager_class.return_value = mock_configs_manager

        mock_template_service = Mock()
        mock_template_service_class.return_value = mock_template_service

        request = RegenerateRequest()

        result = regenerate_configs(request)

        assert result.total_processed == 1
        assert result.successful == 0
        assert result.failed == 1
        assert result.results[0].domain == 'example.com'
        assert result.results[0].success is False
        assert 'Error processing config: Read error' in result.results[0].error
        assert result.results[0].template is None
