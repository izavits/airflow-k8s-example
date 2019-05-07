# airflow-k8s-example

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

> Apache Airflow with Kubernetes example.

This is an example using Apache Airflow with Kubernetes. It provides some very basic tasks that just pring a string and runs them in kubernetes PODs using the kubernetes POD Operator of Apache Airflow.

## Table of Contents

- [Install](#install)
- [Usage](#usage)
- [Tests](#tests)
- [Support](#support)
- [Contributing](#contributing)
- [License](#license)

## Install
- Clone the repository and enter the project directory.

- Create your virtual environment, export the necessary variables and install the required dependencies:

```
virtualenv -p `which python` venv
source venv/bin/activate
mkdir airflow_home
export AIRFLOW_HOME=`pwd`/airflow_home
export SLUGIFY_USES_TEXT_UNIDECODE=yes
pip install apache-airflow
pip install kubernetes
``` 

- Make sure you have the project in your `PYTHONPATH`.

*Note: We assume that you have a local kubernetes cluster running locally, e.g. using `minikube`.*

## Usage
Create the airflow database:

```
airflow initdb
```

Start the airflow webserver:

```
airflow webserver
```

Start the airflow scheduler in another terminal:

```
airflow scheduler
```

Start your minikube kubernetes cluster. From its web UI you will be able to see the PODs that are created for the tasks of the example.

Go to your local airflow UI (`localhost:8080`), toggle the DAG and trigger it. You will be able to see the tasks running in the Graph view and from your kubernetes cluster web UI you will be able to see the corresponding containers created in your kubernetes cluster.

## Tests
Unit tests are included. Install `pytest` if needed and run it to execute them:

```
pip install pytest
pytest
```

## Support
If you're having any problem, please raise an issue on GitHub.

## Contributing
PRs accepted. Some general guidelines:

- Write a concise commit message explaining your changes.
- If applies, write more descriptive information in the commit body.
- Refer to the issue/s your pull request fixes (if there are issues in the github repo).
- Write a descriptive pull request title.
- Squash commits when possible.

Before your pull request can be merged, the following conditions must hold:

- All the tests passes (if any).
- The coding style aligns with the project's convention.
- Your changes are confirmed to be working.

Small note: If editing the Readme, please conform to the [standard-readme](https://github.com/RichardLitt/standard-readme) specification.

## License
The project is licensed under the Apache 2.0 license.
