from pathlib import Path
from typing import List


class ConfigsManager:
    def __init__(self, folder_name: str = 'configs'):
        self.root_path = Path(__file__).parent.parent.parent.resolve()
        self.folder_path = self.root_path / folder_name

    def list_files(self) -> List[str]:
        return [f.name for f in self.folder_path.iterdir() if f.is_file()]

    def file_exists(self, filename: str) -> bool:
        return (self.folder_path / filename).is_file()

    def read_file(self, filename: str) -> str:
        file_path = self.folder_path / filename
        if not file_path.is_file():
            raise FileNotFoundError(f"File '{filename}' not found in folder '{self.folder_path.name}'")
        return file_path.read_text(encoding='utf-8')

    def write_file(self, filename: str, content: str) -> None:
        file_path = self.folder_path / filename
        file_path.write_text(content, encoding='utf-8')

    def remove_file(self, filename: str) -> None:
        file_path = self.folder_path / filename
        if file_path.is_file():
            file_path.unlink()

    @property
    def folder_exists(self) -> bool:
        return self.folder_path.is_dir()
