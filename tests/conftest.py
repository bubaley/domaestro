import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest


@pytest.fixture
def temp_directory():
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def sample_template_content():
    return """
http:
  routers:
    {{slug_domain}}-router:
      rule: "Host(`{{domain}}`)"
      service: {{slug_domain}}-service
      tls:
        certResolver: letsencrypt

  services:
    {{slug_domain}}-service:
      loadBalancer:
        servers:
          - url: "http://internal-service:8080"
"""


@pytest.fixture
def sample_config_content():
    return """# TEMPLATE_NAME: default
http:
  routers:
    example-com-router:
      rule: "Host(`example.com`)"
      service: example-com-service
      tls:
        certResolver: letsencrypt

  services:
    example-com-service:
      loadBalancer:
        servers:
          - url: "http://internal-service:8080"
"""


@pytest.fixture
def mock_dns_check():
    with patch('app.utils.dns.check_cname_a_record') as mock:
        mock.return_value = (True, 'DNS OK')
        yield mock


@pytest.fixture
def mock_traefik_utils():
    with (
        patch('app.utils.traefik.config_exists') as mock_exists,
        patch('app.utils.traefik.list_traefik_configs') as mock_list,
    ):
        mock_exists.return_value = True
        mock_list.return_value = ['example.com.yaml', 'test.com.yaml']
        yield {'config_exists': mock_exists, 'list_traefik_configs': mock_list}
