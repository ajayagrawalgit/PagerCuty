
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
# Display help information
python pagercuty.py --help

# Check PagerDuty status
python pagercuty.py --check_pd_status

# List service IDs
python pagercuty.py -get_service_ids

# List schedule IDs
python pagercuty.py -get_schedule_ids
```

### Incident Management

```bash
# Create new incident
python pagercuty.py --create_an_incident

# List all incidents
python pagercuty.py -list all

# List user's incidents
python pagercuty.py -list user
```

PagerCuty - A Command-Line Utility for PagerDuty.

options:
  -h, --help            show this help message and exit
  --check_pd_status, -pds
                        Checks the Status of PagerDuty from both, Manual hit to Company's URL and from the Official PagerDuty Status Page
  --create_an_incident, -crin
                        Lets you Create a PagerDuty Incident
  -list {all,user}      all - Lists all Non-Resolved Incidents on PagerDuty, user - Lists all Incidents on PagerDuty assigned to the Ajay Agrawal
  -ack {all,user,id}    all - Acknowledges all [Triggered] Incidents on PagerDuty, user - Acknowledges all [Triggered] Incidents on PagerDuty assigned to the Ajay Agrawal, id - Acknowledges a Specific Incident from Pagerduty (List will be
                        Provided)
  -ackloop {all,user}   all - Acknowledges all [Triggered] Incidents on PagerDuty every 30 seconds, user - Acknowledges all [Triggered] Incidents on PagerDuty assigned to Ajay Agrawal every 30 seconds
  --resolve {all,user,id,like}, -res {all,user,id,like}
                        all - Resolves all Incidents from PagerDuty, user - Resolves all Incidents from PagerDuty assigned to Ajay Agrawal, id - Resolves a Specific Incident from Pagerduty (List will be Provided), like - Resolves all the
                        Incidents from Pagerduty containing a certain keyword
  --add_note, -an       Use this to add note to an Incident (List will be Provided)
  -get_service_ids      This lists all the Service IDs and their Names
  -get_schedule_ids     This lists all the Schedule IDs and their Names
```
Of course, the username which you can see above i.e. `Ajay Agrawal` will be different in your case. You'll get the name which is registered with the e-mail id provided in `config.yaml`
Also, here you can see that you'll have some short-hand commands as well for some functionalities to save some of your key-strokes :wink:

### Check PagerDuty Status
Use this command to check the status of PagerDuty. It can retrieve status from both the company's URL and the official PagerDuty Status Page

```python
python3 pagercuty.py --check_pd_status
or
python3 pagercuty.py --pds
```

### Create an Incident
You can use this command to create a PagerDuty incident.

```python
python3 pagercuty.py --create_an_incident
or
python3 pagercuty.py --crin
```

### List Incidents
List all non-resolved incidents on PagerDuty or filter by the user.

```python
python3 pagercuty.py -list all
```

```python
python3 pagercuty.py -list user
```

### Acknowledge Incidents
Acknowledge incidents on PagerDuty. You can acknowledge all triggered incidents, all assigned to a specific user, or a specific incident by ID.

```python
python3 pagercuty.py -ack all
```

```python
python3 pagercuty.py -ack user
```

```python
.python3 pagercuty.py -ack id
```

### Acknowledge Incidents in a Loop
Acknowledge triggered incidents in a loop, either all or those assigned to a specific user.

```python
python3 pagercuty.py -ackloop all
```

```python
python3 pagercuty.py -ackloop user
```

### Resolve Incidents
Resolve incidents on PagerDuty. You can resolve all incidents, those assigned to a specific user, a specific incident by ID, or those containing a keyword.

```python
python3 pagercuty.py --resolve all
or
python3 pagercuty.py -res all
```

```python
python3 pagercuty.py --resolve user
or
python3 pagercuty.py --res user
```

```python
python3 pagercuty.py --resolve id
or
python3 pagercuty.py -res id
```

```python
python3 pagercuty.py --resolve like
or
python3 pagercuty.py -res like
```

### Add Note to Incident
Use this command to add a note to a specific incident.

```python
python3 pagercuty.py --add_note
or
python3 pagercuty.py -an
```

### List Service and Schedule IDs
List all the Service and schedule IDs along with their names.

```python
python3 pagercuty.py -get_service_ids
```

```python
python3 pagercuty.py -get_schedule_ids
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
