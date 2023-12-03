# Obris CLI
![Obris logo](./assets/images/obris-logo.svg)

The Obris CLI is used to manage Obris apps from the command line. 
It is built using [click](https://click.palletsprojects.com/en/8.1.x/) 
as the underlying cli framework.  

Learn more about Obris @[obris.io](https://obris.io).

Use our [quickstart guide](https://www.obris.io/docs/quickstart) to start building apps.

## Overview

This repo is in an Alpha release. 

This project aims to make managing your infrastructure independent from the cloud it's deployed on.  We want developers 
to be able to leverage the tools they need and not have to make compromises when choosing between a scoped, managed 
PaaS offering or a customizable, terse IaaS offering.

## Developing

### Install Dependencies

```bash
pyenv install 3.12.0
pyenv virtualenv 3.12.0 obris-cli

pyenv local obris-cli
pip install -r requirements.txt
```

### Entry Point

Start running Obris commands locally!

```bash
./main.py <command>
```

## Contributing

* [Branch Guidelines](docs/contributing/branch_guidelines.md)
* [Pull Request Guidelines](./.github/PULL_REQUEST_TEMPLATE.md)
