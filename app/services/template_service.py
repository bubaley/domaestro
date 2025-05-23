import re
from typing import Tuple

from app.core.config import CONFIGS_DIR, TEMPLATES_DIR
from app.services.configs_manager import ConfigsManager


class TemplateService:
    def __init__(self):
        self.templates_manager = ConfigsManager(TEMPLATES_DIR)
        self.configs_manager = ConfigsManager(CONFIGS_DIR)

    def template_exists(self, template_name: str) -> bool:
        return self.templates_manager.file_exists(f'{template_name}.yaml')

    def load_template(self, template_name: str) -> str:
        filename = f'{template_name}.yaml'
        if not self.template_exists(template_name):
            raise FileNotFoundError(f"Template '{template_name}' not found")
        return self.templates_manager.read_file(filename)

    def generate_slug_domain(self, domain: str) -> str:
        """Генерирует slug из домена (заменяет . и - на _)"""
        return re.sub(r'[._]', '-', domain)

    def process_template(self, template_name: str, domain: str) -> str:
        template_content = self.load_template(template_name)
        slug_domain = self.generate_slug_domain(domain)

        header_comment = f'# TEMPLATE_NAME: {template_name}\n'

        processed_content = template_content.replace('{{domain}}', domain)
        processed_content = processed_content.replace('{{slug_domain}}', slug_domain)

        return header_comment + processed_content

    def create_config_from_template(self, template_name: str, domain: str) -> Tuple[bool, str]:
        try:
            if not self.template_exists(template_name):
                return False, f"Template '{template_name}' not found"

            processed_content = self.process_template(template_name, domain)
            config_filename = f'{domain}.yaml'

            self.configs_manager.write_file(config_filename, processed_content)
            return True, f"Config created successfully for domain '{domain}'"

        except Exception as e:
            return False, f'Error creating config: {str(e)}'
