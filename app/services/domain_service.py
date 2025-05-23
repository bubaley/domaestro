import re

from app.core.config import CONFIGS_DIR
from app.schemas.domain import (
    DomainRegisterRequest,
    DomainResponse,
    RegenerateRequest,
    RegenerateResponse,
    RegenerateResult,
)
from app.services.configs_manager import ConfigsManager
from app.services.template_service import TemplateService
from app.utils.dns import check_cname_a_record
from app.utils.traefik import (
    config_exists,
    list_traefik_configs,
)


def extract_template_name_from_config(config_content: str) -> str | None:
    """
    Extracts template name from config content.
    Returns template name if found, None otherwise.
    """
    if not config_content:
        return None

    first_line = config_content.split('\n')[0].strip()
    template_match = re.match(r'^#\s*TEMPLATE_NAME:\s*(.+)$', first_line)
    if template_match:
        return template_match.group(1).strip()
    return None


def register_domain(request: DomainRegisterRequest) -> DomainResponse:
    domain = request.domain
    template_name = request.template

    valid, msg = check_cname_a_record(domain)
    if not valid:
        return DomainResponse(domain=domain, success=False, error=msg, template=template_name)
    template_service = TemplateService()
    success, message = template_service.create_config_from_template(template_name, domain)

    if not success:
        return DomainResponse(domain=domain, success=False, error=message, template=template_name)

    return DomainResponse(domain=domain, success=True, template=template_name)


def validate_domain(request: DomainRegisterRequest) -> DomainResponse:
    domain = request.domain

    # Check if config exists
    if not config_exists(domain):
        return DomainResponse(domain=domain, success=False, error='Config not found')

    template_name = None
    try:
        configs_manager = ConfigsManager(CONFIGS_DIR)
        config_filename = f'{domain}.yaml'
        config_content = configs_manager.read_file(config_filename)
        template_name = extract_template_name_from_config(config_content)
    except Exception:
        pass

    valid, msg = check_cname_a_record(domain)
    if not valid:
        return DomainResponse(domain=domain, success=False, error=msg, template=template_name)

    return DomainResponse(domain=domain, success=True, template=template_name)


def list_configs() -> list[str]:
    return list_traefik_configs()


def regenerate_configs(request: RegenerateRequest) -> RegenerateResponse:
    """
    Regenerates configs based on templates.
    If template is specified in request, regenerates only configs with that template.
    If template is not specified, regenerates all configs.
    """
    configs_manager = ConfigsManager(CONFIGS_DIR)
    template_service = TemplateService()

    # Get list of all configs
    config_files = configs_manager.list_files()
    yaml_configs = [f for f in config_files if f.endswith('.yaml')]

    results = []

    for config_file in yaml_configs:
        # Extract domain from filename
        domain = config_file.replace('.yaml', '')

        try:
            # Read config content
            config_content = configs_manager.read_file(config_file)

            # Extract template name from first line
            config_template = extract_template_name_from_config(config_content)
            if not config_template:
                # If no template information found, skip
                results.append(
                    RegenerateResult(
                        domain=domain, success=False, error='Template name not found in config', template=None
                    )
                )
                continue

            # If template is specified in request, check match
            if request.template and config_template != request.template:
                continue

            # Check if template exists
            if not template_service.template_exists(config_template):
                results.append(
                    RegenerateResult(
                        domain=domain,
                        success=False,
                        error=f"Template '{config_template}' not found",
                        template=config_template,
                    )
                )
                continue

            # Regenerate config
            success, message = template_service.create_config_from_template(config_template, domain)

            results.append(
                RegenerateResult(
                    domain=domain, success=success, error=None if success else message, template=config_template
                )
            )

        except Exception as e:
            results.append(
                RegenerateResult(
                    domain=domain, success=False, error=f'Error processing config: {str(e)}', template=None
                )
            )

    # Calculate statistics
    successful = sum(1 for result in results if result.success)
    failed = len(results) - successful

    return RegenerateResponse(results=results, total_processed=len(results), successful=successful, failed=failed)
