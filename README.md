
<a  href="https://www.buymeacoffee.com/ajayagrawal">![PagerDuty](https://github.com/ajayagrawalgit/PagerCuty/assets/94609372/9dc4c5c9-cfa2-4aac-8d12-5846a5607cac) </a>
 
<p align="center">
<a href="https://github.com/ajayagrawalgit/PagerCuty/blob/main/LICENSE" title="License">
<img src="https://img.shields.io/github/license/ajayagrawalgit/PagerCuty?label=License&logo=Github&style=flat-square" alt="PagerCuty License"/>
</a>
<a href="https://github.com/ajayagrawalgit/PagerCuty/fork" title="Forks">
<img src="https://img.shields.io/github/forks/ajayagrawalgit/PagerCuty?label=Forks&logo=Github&style=flat-square" alt="ScareCrypt Forks"/>
</a>
<a href="https://github.com/ajayagrawalgit/PagerCuty/stargazers" title="Stars">
<img src="https://img.shields.io/github/stars/ajayagrawalgit/PagerCuty?label=Stars&logo=Github&style=flat-square" alt="ScareCrypt Stars"/>
</a>
<a href="https://github.com/ajayagrawalgit/PagerCuty/issues" title="Issues">
<img src="https://img.shields.io/github/issues/ajayagrawalgit/PagerCuty?label=Issues&logo=Github&style=flat-square" alt="ScareCrypt Issues"/>
</a>
<a href="https://github.com/ajayagrawalgit/PagerCuty/pulls" title="Pull Requests">
<img src="https://img.shields.io/github/issues-pr/ajayagrawalgit/PagerCuty?label=Pull%20Requests&logo=Github&style=flat-square" alt="ScareCrypt Pull Requests"/>
</a>
<a href="https://github.com/ajayagrawalgit/PagerCuty" title="Repo Size">
<img src="https://img.shields.io/github/repo-size/ajayagrawalgit/PagerCuty?label=Repo%20Size&logo=Github&style=flat-square" alt="ScareCrypt Repo Size"/>
</a>

<br>

# PagerCuty - A Command-Line Utility for Managing Incidents in PagerDuty :pager:


PagerCuty is a versatile command-line tool built on Python that simplifies incident management on PagerDuty. With PagerCuty, you can perform various actions, from checking PagerDuty's status to creating and managing incidents, all from the command line. This README.md file will guide you through the prerequisites, installation, configuration, and usage of PagerCuty, making your incident management process efficient and hassle-free. :rocket:

## Table of Contents
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#usage)
  - [Check PagerDuty Status](#check-pagerduty-status)
  - [Create an Incident](#create-an-incident)
  - [List Incidents](#list-incidents)
  - [Acknowledge Incidents](#acknowledge-incidents)
  - [Acknowledge Incidents in a Loop](#acknowledge-incidents-in-a-loop)
  - [Resolve Incidents](#resolve-incidents)
  - [Add Note to Incident](#add-note-to-incident)
  - [List Service and Schedule IDs](#list-service-and-schedule-ids)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

### Prerequisites
Welcome to PagerCuty :sparkles:
Before getting started, please review the following prerequisites to ensure a smooth experience with the tool. 

### Compatibility
PagerCuty can be fully utilized on Linux and MacOS machines. On Windows, while most functionalities work seamlessly, there may be limitations for tasks involving multiline string descriptions. Efforts are being made to enhance OS independence in future updates. If Windows is your preferred choice, the complete potential of PagerCuty can be harnessed through WSL (Windows Subsystem for Linux). 

### Prerequisites for Linux and MacOS Users
For a hassle-free experience with PagerCuty on Linux or MacOS, you'll need the following:

1. **Text Editor**: Ensure that you have the versatile Vi or Vim editor installed. You can install it using your package manager or download it from [vim.org](https://www.vim.org/download.php). 🔍

2. **Python Version**: A minimum of Python 3.11.x or a higher version is required for error-free functionality. You can download Python from [python.org](https://www.python.org/downloads/). 🐍

That's all you need! The remaining dependencies will be automatically installed as Python packages, conveniently listed in the `requirements.txt` file. 

PagerCuty is designed with your needs in mind, and I'm excited to have you on board for this journey 😊🚀


<br>

### Installation
To begin using PagerCuty, follow these simple installation steps:

1. Clone the PagerCuty repository to your local machine.
   ```bash
   git clone https://github.com/ajayagrawalgit/PagerCuty.git
   ```

2. Change your working directory to the PagerCuty folder.
   ```bash
   cd pagercuty
   ```

3. Install the required dependencies using `pip`.
   ```bash
   pip install -r requirements.txt
   ```

4. Make the `pagercuty.py` file executable.
   ```bash
   chmod +x pagercuty.py
   ```

Now you're ready to configure PagerCuty and start managing your PagerDuty incidents.

### Configuration
Before using PagerCuty, you need to configure it with your PagerDuty account details. Open the `config.yaml`  file and find the following lines:

```python
pagerduty:
  api_token:	# Create this from the pagerduty website
  service_id:	# Service IDs which you want to see and manage incidents for (You can find it using this tool itself if you don't know yet)
  email:	# Your Registered E-mail ID with PagerDuty
  script_name: pagercuty
  time_interval: 30	# This is the time interval at which the auto acknowledge function works. The unit is in seconds. (Default is set to 30 seconds)
  company_pd_url:	# Here, you have to put the the url which your comapny uses to login to pagerduty. Example: https://ajayagrawal.pagerduty.com/sign_in/
  company_domain:	# Here, you have to put the the url which your comapny uses to login to pagerduty. Example: https://ajayagrawal.pagerduty.com (Make sure there's no '/' at the end here)
```

<br>

## Usage

PagerCuty provides various commands to interact with PagerDuty. Here's how you can use each command:


### Get the Help Menu
Use `--help` or `-h` to get the help menu which will be somewhat like below:
```bash
ajayagrawal@hack_the_box:~/pagercuty $ python3 pagercuty.py -h
usage: pagercuty.py [-h] [--check_pd_status] [--create_an_incident] [-list {all,user}] [-ack {all,user,id}] [-ackloop {all,user}] [--resolve {all,user,id,like}] [--add_note] [-get_service_ids] [-get_schedule_ids]

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

## Contributing
Contributions to PagerCuty are welcome! If you have ideas for improvements, bug fixes, or new features, please submit an issue or create a pull request.

## License
PagerCuty is released under the [MIT License](LICENSE). Feel free to use, modify, and distribute it as needed.

Happy incident management with PagerCuty! 🎉


<br>
<br>

 ## 🧑🏻 Know Me More
Developer - <b> Ajay Agrawal </b>
<br>
- 🌌 [Profile](https://github.com/ajayagrawalgit "Ajay Agrawal")
- 🏮 [Email](mailto:ajayagrawalhere@gmail.com?subject=Hi%20from%20<repo-email> "Hi!")
- 🐦 [Twitter Bot (@mickbotsays)](https://twitter.com/mickbotsays)

<br>
<br>
<h2 align="center"> 🤝 Support Me 🤝 <h2>
<p align="center">
<a href="https://www.buymeacoffee.com/ajayagrawal" title="Buy me a Coffee"><img src="https://user-images.githubusercontent.com/94609372/232127833-d03502af-baf2-46e3-a045-0f7c84531a61.png" alt="Buy me a Coffee"/></a>
</p>
<br><br>
<h4>
<br>
<p align="center"> Made with ♥️ in India </p>
<br>
