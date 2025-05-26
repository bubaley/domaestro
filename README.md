# Domaestro

A modern API service for managing Traefik configurations dynamically. Domaestro simplifies the process of creating and managing domain configurations for Traefik reverse proxy using templates and API calls.

## Features

- 🚀 **Template-based configuration**: Use YAML templates to generate Traefik configurations
- 🔧 **RESTful API**: Simple HTTP API for domain management
- 🐳 **Docker-ready**: Fully containerized with Docker support
- 🔒 **Secure**:  Token-based authentication with domain validation
- 📊 **Health checks**: Built-in health monitoring
- ⚡ **Fast**: Built with FastAPI for high performance

## How It Works

1. **Templates**: Define reusable Traefik configuration templates in `templates/` directory
2. **API**: Use the REST API to register domains with specific templates
3. **Configs**: Generated configurations are saved to `configs/` directory
4. **Traefik**: Point Traefik to load configurations from the `configs/` directory

## Quick Start

### Using Docker Compose (Recommended)

📦 **Ready to use**: The `example/` directory contains a complete working setup with all necessary files and structure.

1. **Copy the example structure**:
   ```bash
   cp -r example/ my-domaestro-setup/
   cd my-domaestro-setup/
   ```

2. **Set permissions for Let's Encrypt**:
   ```bash
   chmod 600 acme.json
   ```
   > ⚠️ **Important**: The `acme.json` file must have 600 permissions for Let's Encrypt to work properly.

3. **Create environment variables**:
   ```bash
   # Edit .env with your configuration (especially AUTH_TOKEN and TRAEFIK_LETSENCRYPT_EMAIL)
   ```

4. **Start the services**:
   ```bash
   docker compose up -d
   ```

### Manual Docker Compose Setup

If you prefer to create the structure manually:

1. Create a `docker-compose.yaml` file:

```yaml
services:
  traefik:
    container_name: "traefik"
    image: traefik:v3.4
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
      - "${TRAEFIK_DASHBOARD_PORT:-8080}:8080"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./acme.json:/acme.json
      - ./configs:/etc/traefik/dynamic:ro
    command:
      - "--api.dashboard=true"
      - "--api.insecure=${TRAEFIK_INSECURE:-false}"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--providers.docker=true"
      - "--providers.docker.exposedByDefault=false"
      - "--providers.docker.network=traefik"
      - "--providers.file.directory=/etc/traefik/dynamic"
      - "--providers.file.watch=true"
      - "--certificatesresolvers.letsencrypt.acme.storage=acme.json"
      - "--certificatesresolvers.letsencrypt.acme.httpchallenge.entrypoint=web"
      - "--certificatesresolvers.letsencrypt.acme.email=${TRAEFIK_LETSENCRYPT_EMAIL:-example@example.com}"
      - "--log.level=INFO"
      - "--log.filepath=/var/log/traefik.log"
      - "--accesslog.filepath=/var/log/access.log"
    networks:
      - traefik

  domaestro:
    container_name: domaestro
    image: bubaley/domaestro:latest
    restart: unless-stopped
    ports:
      - "${DOMAESTRO_PORT:-8000}:8000"
    volumes:
      - ./configs:/app/configs
      - ./templates:/app/templates
    env_file:
      - .env
    networks:
      - traefik

networks:
  traefik:
    external: false
```

2. Create the necessary directories and files:

```bash
mkdir -p configs templates
touch acme.json
chmod 600 acme.json
```

3. Copy your templates to the `templates/` directory

4. Create a `.env` file (see [Environment Variables](#environment-variables))

5. Start the services:

```bash
docker compose up -d
```

### Local Development

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd domaestro
   ```

2. **Install dependencies** (requires Python 3.13):
   ```bash
   uv sync
   ```

3. **Set up environment variables**:
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

4. **Create required directories**:
   ```bash
   mkdir -p configs templates
   ```

5. **Run the application**:
   ```bash
   make run
   ```

### Environment Variables Description

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `AUTH_TOKEN` | ✅ | - | Secret token for API authentication |
| `VALID_CNAMES` | ❌ | - | Comma-separated valid CNAME targets |
| `VALID_IPS` | ❌ | - | Comma-separated valid IP addresses |
| `TRAEFIK_DASHBOARD_PORT` | ❌ | 8080 | Port for Traefik dashboard |
| `TRAEFIK_INSECURE` | ❌ | false | Enable insecure dashboard access |
| `TRAEFIK_LETSENCRYPT_EMAIL` | ❌ | example@example.com | Email for Let's Encrypt certificates |
| `DOMAESTRO_PORT` | ❌ | 8000 | Port for Domaestro API |

## API Documentation

### Authentication

All API endpoints (except health check) require authentication using the `Authorization` header:

```bash
Authorization: Bearer your-secret-token-here
```

### Endpoints

#### Health Check
```http
GET /api/health
```

#### Register Domain
```http
POST /api/domains/register
Content-Type: application/json

{
  "domain": "example.com",
  "template": "default"
}
```

#### Validate Domain
```http
POST /api/domains/validate
Content-Type: application/json

{
  "domain": "example.com"
}
```

#### List Configurations
```http
GET /api/domains/configs
```

#### Regenerate Configurations
```http
POST /api/domains/regenerate
Content-Type: application/json

{
  "template": "default"  // Optional: specific template, or null for all
}
```

### Example API Usage

```bash
# Register a new domain
curl -X POST "http://localhost:8000/api/domains/register" \
  -H "Authorization: Bearer your-secret-token-here" \
  -H "Content-Type: application/json" \
  -d '{"domain": "mysite.com", "template": "default"}'

# List all configurations
curl -X GET "http://localhost:8000/api/domains/configs" \
  -H "Authorization: Bearer your-secret-token-here"
```

## Templates

Templates are YAML files stored in the `templates/` directory. They use Jinja2-style templating with the following variables:

- `{{domain}}`: The domain name (e.g., `example.com`)
- `{{slug_domain}}`: Domain with dots replaced by hyphens (e.g., `example-com`)

### Example Template (`templates/default.yaml`)

```yaml
http:
  middlewares:
    redirect-to-https:
      redirectScheme:
        scheme: https
        permanent: true
  routers:
    {{slug_domain}}-http:
      rule: "Host(`{{domain}}`)"
      entryPoints:
        - web
      middlewares:
        - redirect-to-https
      service: {{slug_domain}}-service

    {{slug_domain}}-https:
      rule: "Host(`{{domain}}`)"
      entryPoints:
        - websecure
      service: {{slug_domain}}-service
      tls:
        certResolver: letsencrypt
  services:
    {{slug_domain}}-service:
      loadBalancer:
        servers:
          - url: "http://your-backend-server:port"
```

## Configuration Output

Generated configurations are saved as `configs/{domain}.yaml` files. For example, registering `example.com` with the default template creates `configs/example.com.yaml`.

## Building Docker Image

```bash
# Build the image
docker build -t domaestro .

# Run the container
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/configs:/app/configs \
  -v $(pwd)/templates:/app/templates \
  -e AUTH_TOKEN=your-secret-token \
  domaestro
```

## Development

### Prerequisites

- Python 3.13
- UV package manager

### Setup Development Environment

```bash
# Install dependencies
uv sync
uv run pre-commit run --all-files
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support

For issues and questions, please open an issue on the GitHub repository.
