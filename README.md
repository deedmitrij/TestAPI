# TestAPI

**Table of contents**

- [Description](#description)
- [Getting started](#getting-started)
- [Dependencies](#dependencies)
- [Installing](#installing)
- [Run tests](#run-tests)

## Description

Fake API server for testing purposes.

## Getting Started

### Dependencies

* Windows OS
* Python 3.10

### Installing

1. Clone the project
```
git clone git@github.com:deedmitrij/TestAPI.git
```
2. Create a virtual environment inside the cloned project
```
py -3.10 -m venv .\venv
```
3. Activate the created virtual environment
* for PowerShell
```
.\venv\Scripts\Activate.ps1
```
* for CMD
```
.\venv\Scripts\activate.bat
```
4. Install all required packages
```
pip install -r requirements.txt
```

### Run tests

```
pytest -v .\tests\
```
