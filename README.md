
# PagerCuty

<div align="center">

[![License](https://img.shields.io/github/license/ajayagrawalgit/PagerCuty?style=flat-square)](LICENSE)
[![Stars](https://img.shields.io/github/stars/ajayagrawalgit/PagerCuty?style=flat-square)](https://github.com/ajayagrawalgit/PagerCuty/stargazers)
[![Forks](https://img.shields.io/github/forks/ajayagrawalgit/PagerCuty?style=flat-square)](https://github.com/ajayagrawalgit/PagerCuty/fork)
[![Issues](https://img.shields.io/github/issues/ajayagrawalgit/PagerCuty?style=flat-square)](https://github.com/ajayagrawalgit/PagerCuty/issues)
[![PRs](https://img.shields.io/github/issues-pr/ajayagrawalgit/PagerCuty?style=flat-square)](https://github.com/ajayagrawalgit/PagerCuty/pulls)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg?style=flat-square)](https://www.python.org/downloads/)

A professional command-line interface for efficient PagerDuty incident management.

[Getting Started](#getting-started) •
[Installation](#installation) •
[Documentation](#documentation) •
[Contributing](#contributing)

![PagerDuty](https://github.com/ajayagrawalgit/PagerCuty/assets/94609372/9dc4c5c9-cfa2-4aac-8d12-5846a5607cac)

</div>

## Overview

PagerCuty is a robust command-line interface (CLI) tool designed to streamline PagerDuty incident management. Built with Python, it offers a comprehensive set of features for incident handling, status monitoring, and team collaboration, all accessible through an intuitive command-line interface.

### Key Features

- **Real-time Status Monitoring**: Monitor PagerDuty service status and company-specific instances
- **Incident Management**: Create, acknowledge, and resolve incidents efficiently
- **Automated Acknowledgment**: Set up automatic acknowledgment of triggered incidents
- **Team Collaboration**: Add notes and manage incidents across team members
- **Service Integration**: List and manage service IDs and schedules
- **Cross-platform Support**: Full functionality on Linux and MacOS, with WSL support for Windows

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Basic Commands](#basic-commands)
  - [Incident Management](#incident-management)
  - [Advanced Features](#advanced-features)
- [Development](#development)
  - [Contributing](#contributing)
  - [Building from Source](#building-from-source)
- [Support](#support)
- [License](#license)

## Requirements

### System Requirements

- **Operating System**
  - Linux (Full Support)
  - macOS (Full Support)
  - Windows (via WSL recommended)

### Dependencies

- **Python**: Version 3.11 or higher
- **Vim/Vi**: Required for multi-line text input
- **Required Python Packages**:
  ```
  pdpyras>=5.1.2
  pytz>=2023.3
  PyYAML>=6.0.1
  requests>=2.31.0
  tabulate>=0.9.0
  ```

### Platform-Specific Notes

#### Linux and macOS
- Native support for all features
- Package management via apt/brew recommended

#### Windows
- WSL (Windows Subsystem for Linux) recommended for full functionality
- Some limitations with multi-line text input in native Windows
- PowerShell or Command Prompt supported for basic operations


<br>

## Installation

### From Source

1. Clone the repository
   ```bash
   git clone https://github.com/ajayagrawalgit/PagerCuty.git
   cd PagerCuty
   ```

2. Create and activate a virtual environment (optional but recommended)
   ```bash
   # Linux/macOS
   python -m venv venv
   source venv/bin/activate

   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Set up execution permissions (Linux/macOS)
   ```bash
   chmod +x pagercuty.py
   ```

### Via pip (Coming Soon)

```bash
pip install pagercuty
```

### Verification

Verify the installation by running:
```bash
python pagercuty.py --version
```

## Configuration

PagerCuty requires configuration through a YAML file. Create `config.yaml` in the root directory:

```yaml
pagerduty:
  # Required Configuration
  api_token: "your-api-token"    # PagerDuty API token
  service_id: "service-id"       # Comma-separated service IDs
  email: "user@example.com"      # Your PagerDuty email
  
  # Optional Configuration
  script_name: "pagercuty"       # Script name for logging
  time_interval: 30              # Auto-acknowledgment interval (seconds)
  company_pd_url: "https://company.pagerduty.com/sign_in"
  company_domain: "https://company.pagerduty.com"  # No trailing slash
```

### Configuration Details

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `api_token` | Yes | Your PagerDuty API token | `"p-1234abcd"` |
| `service_id` | Yes | Service IDs to monitor | `"PABC123,PDEF456"` |
| `email` | Yes | Registered email | `"user@example.com"` |
| `time_interval` | No | Auto-ack interval | `30` |
| `company_pd_url` | No | Company PD URL | `"https://company.pagerduty.com/sign_in"` |

### Obtaining Credentials

1. **API Token**: Generate from PagerDuty → User Settings → API Access
2. **Service IDs**: Available via `python pagercuty.py -get_service_ids`

<br>

## Usage

### Basic Commands

```bash
# Get help and version information
python pagercuty.py --help
python pagercuty.py --version

# Check service status
python pagercuty.py --check_pd_status     # Check PagerDuty status
python pagercuty.py -pds                  # Short form

# List resources
python pagercuty.py -get_service_ids      # List service IDs
python pagercuty.py -get_schedule_ids     # List schedule IDs
```

### Incident Management

#### Creating and Viewing Incidents
```bash
# Create new incident
python pagercuty.py --create_an_incident  # Full command
python pagercuty.py --crin               # Short form

# List incidents
python pagercuty.py -list all            # List all incidents
python pagercuty.py -list user           # List user's incidents
```

#### Acknowledging Incidents
```bash
# Acknowledge specific incidents
python pagercuty.py -ack all             # Acknowledge all incidents
python pagercuty.py -ack user            # Acknowledge user's incidents
python pagercuty.py -ack id              # Acknowledge by ID

# Auto-acknowledge loops
python pagercuty.py -ackloop all         # Auto-acknowledge all
python pagercuty.py -ackloop user        # Auto-acknowledge user's
```

#### Resolving Incidents
```bash
# Resolve by scope
python pagercuty.py --resolve all        # Resolve all incidents
python pagercuty.py --resolve user       # Resolve user's incidents
python pagercuty.py --resolve id         # Resolve by ID
python pagercuty.py --resolve like       # Resolve by keyword

# Short form alternatives
python pagercuty.py -res all            # Short form for resolve all
python pagercuty.py -res user           # Short form for resolve user
python pagercuty.py -res id             # Short form for resolve by ID
python pagercuty.py -res like           # Short form for resolve by keyword
```

#### Additional Features
```bash
# Add notes to incidents
python pagercuty.py --add_note           # Full command
python pagercuty.py -an                  # Short form

# Resource management
python pagercuty.py -get_service_ids     # List all services
python pagercuty.py -get_schedule_ids    # List all schedules
```

## Development

### Building from Source

1. Fork and clone the repository
2. Set up the development environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   pip install -r requirements.txt
   ```
3. Make your changes
4. Run tests:
   ```powershell
   python -m pytest
   ```

### Coding Standards

- Follow PEP 8 style guide
- Add type hints to all functions
- Include docstrings for modules and functions
- Maintain test coverage above 80%

### Contributing Guidelines

1. Create a new branch for your feature
2. Write clear commit messages
3. Include tests for new features
4. Update documentation
5. Submit a pull request

## Support

### Getting Help

- [Open an issue](https://github.com/ajayagrawalgit/PagerCuty/issues) for bug reports
- [Start a discussion](https://github.com/ajayagrawalgit/PagerCuty/discussions) for questions
- [Read the wiki](https://github.com/ajayagrawalgit/PagerCuty/wiki) for detailed guides

### Troubleshooting

Common issues and solutions are documented in our [FAQ](https://github.com/ajayagrawalgit/PagerCuty/wiki/FAQ).

## License

PagerCuty is released under the [MIT License](LICENSE).

## Author

Developed and maintained by [Ajay Agrawal](https://github.com/ajayagrawalgit)
---

<div align="center">

**Contact**

[GitHub](https://github.com/ajayagrawalgit) • 
[Email](mailto:ajayagrawalhere@gmail.com) • 
[Twitter Bot](https://twitter.com/mickbotsays)

**Support the Project**

[![Buy me a coffee](https://img.shields.io/badge/Buy%20me%20a%20coffee-Support-yellow.svg)](https://www.buymeacoffee.com/ajayagrawal)

Made with ♥️ in India

</div>
