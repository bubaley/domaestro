# CHANGELOG

<!-- version list -->

## v1.0.1 (2025-05-25)

### Bug Fixes

- Update dependencies in pyproject.toml and uv.lock for python-semantic-release and related
  packages.
  ([`556dbab`](https://github.com/bubaley/domaestro/commit/556dbabac9adfbd819e716a366d290485cc1d46b))


## v1.0.0 (2025-05-25)

### Chores

- Add write permissions for contents in release workflow
  ([`361cf45`](https://github.com/bubaley/domaestro/commit/361cf45a24a66061b00cb57a41997bd197d405ba))

- Fix indentation in release workflow for checkout step
  ([`1e62601`](https://github.com/bubaley/domaestro/commit/1e62601c72d922371b860b41b768d7b4954fb35c))

- Refactor release workflow to streamline semantic release process and remove unnecessary steps
  ([`042a0d8`](https://github.com/bubaley/domaestro/commit/042a0d82b063c8c1ee6d8b8162476529fc9d9ccf))

- Release debug
  ([`53c75b6`](https://github.com/bubaley/domaestro/commit/53c75b6eeb84e1630811c787bf8e321d6c827d61))

- Remove Docker build and publish workflow file
  ([`3da454c`](https://github.com/bubaley/domaestro/commit/3da454c82f33aa4b5a624a7147dadcc471d0dd1e))

- Update release configuration and remove unused dependencies from pyproject.toml and uv.lock
  ([`4276163`](https://github.com/bubaley/domaestro/commit/4276163093a4e4d2334c2adfd1d7bfdfd6014827))

- Update release configuration to change branch from 'master' to 'main'
  ([`e4841c6`](https://github.com/bubaley/domaestro/commit/e4841c6e8293a428d3d186d8bc4fa9163a70dc1a))


## v0.2.0 (2025-05-25)

### Chores

- Add package installation step to release workflow
  ([`84da02b`](https://github.com/bubaley/domaestro/commit/84da02bc0c235a7d7460d99eb87d75b6ce295ccf))

- Increase coverage report fail threshold from 30 to 50
  ([`aed2b89`](https://github.com/bubaley/domaestro/commit/aed2b89d1d15355ab8d47a4173e15e161651b528))

- Update dependencies in pyproject.toml and uv.lock files, adding python-semantic-release and other
  packages
  ([`331273e`](https://github.com/bubaley/domaestro/commit/331273e8b86601a42b54547f0f7e36fb9e4c9253))

- Update release workflow to use 'uv run' for semantic release execution
  ([`a673a9c`](https://github.com/bubaley/domaestro/commit/a673a9cebddc4594e43bc6d27f18018419ba7dfd))


## v0.1.0 (2025-05-25)

### Chores

- Add AUTH_TOKEN environment variable to CI workflow for testing
  ([`2feee82`](https://github.com/bubaley/domaestro/commit/2feee82e80a45e6eb73daaf944bd89c502a452c1))

- Clean up whitespace in Docker workflow file
  ([`6fb22f8`](https://github.com/bubaley/domaestro/commit/6fb22f85b63f22f043a3c741417edcaba31927d6))

- Remove obsolete GitHub Actions workflow files for backend setup and Docker image publishing
  ([`3aa1180`](https://github.com/bubaley/domaestro/commit/3aa118036c48395575219d29c6c542aa991a7892))

- Remove obsolete publish Docker image workflow file
  ([`f877c66`](https://github.com/bubaley/domaestro/commit/f877c6615780a1ebca6c8e76aef7012d71856bd3))

- Simplify Docker Hub login condition in workflow file
  ([`a4e7f93`](https://github.com/bubaley/domaestro/commit/a4e7f930dc23718a8dcd2131b537ea3c10d56b71))

- Update Docker workflow to adjust tag pattern by adding prefix and suffix options
  ([`2fb3eff`](https://github.com/bubaley/domaestro/commit/2fb3eff62e967b0fe15eb1d3466b0d057e8a5944))

- Update Docker workflow to refine tag pattern and simplify image push conditions
  ([`d8835d9`](https://github.com/bubaley/domaestro/commit/d8835d929aed8b1cc7a864931866dd3be09eef41))

- Update pre-commit configuration and remove .releaserc.json file
  ([`f30fe3c`](https://github.com/bubaley/domaestro/commit/f30fe3c78b39058416e97de2da2e9c5a888dadd8))

### Features

- Add testing capabilities with pytest and update Makefile for test command
  ([`bb8a822`](https://github.com/bubaley/domaestro/commit/bb8a82207e02859a2e6c6fd5d44203c92b4ffce0))


## v0.0.6 (2025-05-24)

### Bug Fixes

- Optimize directory creation and permission settings in Dockerfile
  ([`78edceb`](https://github.com/bubaley/domaestro/commit/78edceb0603cf472ce4087c34972f24bb44c777e))


## v0.0.5 (2025-05-24)

### Features

- Create necessary directories and set permissions in Dockerfile
  ([`bc8cd91`](https://github.com/bubaley/domaestro/commit/bc8cd91a17c13c54f8bc630f1c90acd1edbd1c46))


## v0.0.4 (2025-05-24)

### Bug Fixes

- Enclose slug domain and service names in quotes for proper YAML formatting in default.yaml
  ([`30fafc9`](https://github.com/bubaley/domaestro/commit/30fafc97e8819e17fe6591d849b3f7456bf80851))

- Remove unnecessary directory creation and permission setting in Dockerfile
  ([`865b14b`](https://github.com/bubaley/domaestro/commit/865b14b7bd7ca9515705238c4577dce1417517ee))


## v0.0.3 (2025-05-24)

### Bug Fixes

- Update example environment files and README for consistency, ensuring proper formatting and
  clarity
  ([`32ac4cc`](https://github.com/bubaley/domaestro/commit/32ac4cc514f66cf90ffd25724977193626849c7c))

### Features

- Add example environment files, update .gitignore, and create README documentation for Domaestro
  ([`c7c8dd3`](https://github.com/bubaley/domaestro/commit/c7c8dd358a61ae6417e76a3a1fa0d8f1ba2142d0))


## v0.0.2 (2025-05-24)


## v0.0.1 (2025-05-24)

- Initial Release
