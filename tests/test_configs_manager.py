import tempfile
from pathlib import Path

import pytest

from app.services.configs_manager import ConfigsManager


class TestConfigsManager:
    @pytest.fixture
    def temp_configs_manager(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            configs_dir = Path(temp_dir) / 'test_configs'
            configs_dir.mkdir()

            manager = ConfigsManager()
            manager.folder_path = configs_dir
            yield manager

    def test_folder_exists_true(self, temp_configs_manager):
        assert temp_configs_manager.folder_exists is True

    def test_folder_exists_false(self):
        manager = ConfigsManager()
        manager.folder_path = Path('/non/existent/path')
        assert manager.folder_exists is False

    def test_list_files_empty_directory(self, temp_configs_manager):
        files = temp_configs_manager.list_files()
        assert files == []

    def test_list_files_with_files(self, temp_configs_manager):
        (temp_configs_manager.folder_path / 'test1.yaml').write_text('content1')
        (temp_configs_manager.folder_path / 'test2.yaml').write_text('content2')
        (temp_configs_manager.folder_path / 'subdir').mkdir()

        files = temp_configs_manager.list_files()
        assert sorted(files) == ['test1.yaml', 'test2.yaml']

    def test_file_exists_true(self, temp_configs_manager):
        filename = 'test.yaml'
        (temp_configs_manager.folder_path / filename).write_text('content')

        assert temp_configs_manager.file_exists(filename) is True

    def test_file_exists_false(self, temp_configs_manager):
        assert temp_configs_manager.file_exists('nonexistent.yaml') is False

    def test_read_file_success(self, temp_configs_manager):
        filename = 'test.yaml'
        content = 'test content\nwith multiple lines'
        (temp_configs_manager.folder_path / filename).write_text(content, encoding='utf-8')

        result = temp_configs_manager.read_file(filename)
        assert result == content

    def test_read_file_not_found(self, temp_configs_manager):
        with pytest.raises(FileNotFoundError) as exc_info:
            temp_configs_manager.read_file('nonexistent.yaml')

        assert "File 'nonexistent.yaml' not found" in str(exc_info.value)

    def test_write_file_success(self, temp_configs_manager):
        filename = 'new_file.yaml'
        content = 'new content\nwith special symbols: ñ, ü, 中文'

        temp_configs_manager.write_file(filename, content)

        assert temp_configs_manager.file_exists(filename)
        assert temp_configs_manager.read_file(filename) == content

    def test_write_file_overwrite(self, temp_configs_manager):
        filename = 'existing_file.yaml'
        old_content = 'old content'
        new_content = 'new content'

        temp_configs_manager.write_file(filename, old_content)
        assert temp_configs_manager.read_file(filename) == old_content

        temp_configs_manager.write_file(filename, new_content)
        assert temp_configs_manager.read_file(filename) == new_content

    def test_remove_file_success(self, temp_configs_manager):
        filename = 'to_delete.yaml'
        (temp_configs_manager.folder_path / filename).write_text('content')

        assert temp_configs_manager.file_exists(filename)

        temp_configs_manager.remove_file(filename)

        assert not temp_configs_manager.file_exists(filename)

    def test_remove_file_not_exists(self, temp_configs_manager):
        temp_configs_manager.remove_file('nonexistent.yaml')
