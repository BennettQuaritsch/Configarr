# Configarr

Configuration-as-code for the *arr suite (Sonarr, Radarr, Prowlarr, etc.)

Configarr manages your *arr application configurations using declarative YAML files. It's built with extensibility in mind, using a plugin architecture that makes it easy to add support for new applications.

## Features

- **Declarative configuration**: Define your *arr stack in version-controlled YAML
- **Plugin architecture**: Easily extensible to support new *arr applications
- **Multi-instance support**: Manage multiple instances of the same application
- **Dry-run mode**: Preview changes before applying them
- **Environment variable interpolation**: Keep secrets secure

## Currently Supported

- **Sonarr**: Custom formats, quality profiles, tags, indexers, download clients, and more

## Quick Start

### Requirements

- Python 3.13+
- A running Sonarr instance (v3 or v4)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/configarr.git
cd configarr

# Install dependencies
pip install PyYAML python-dotenv pydantic

# Install Sonarr API client
pip install -e src/plugins/sonarr/generated
```

### Configuration

1. Create a `.env` file with your credentials:
```bash
SONARR_MAIN_URL=http://localhost:8989
SONARR_MAIN_API_KEY=your_api_key_here
```

2. Create a `config/sonarr.yaml` file:
```yaml
sonarr:
  - name: "main-sonarr"
    base_url: "${SONARR_MAIN_URL}"
    api_key: "${SONARR_MAIN_API_KEY}"
    
    tags:
      delete_unmanaged: false
      definitions:
        - "anime"
        - "tv-shows"
```

### Usage

```bash
# Validate your configuration
python -m src.main validate -c config/sonarr.yaml

# Preview changes (dry-run)
python -m src.main sync --dry-run -c config/sonarr.yaml

# Apply configuration
python -m src.main sync -c config/sonarr.yaml
```

## License

MIT License - see LICENSE file for details
