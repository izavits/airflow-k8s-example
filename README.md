# airflow-k8s-example

> An example using Apache Airflow with Kubernetes. It provides some very simple tasks that just print a string and runs them in kubernetes PODs using the Kubernetes POD Operator of airflow.


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

## Run
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
Unit tests are included. Run `pytest` to execute them. 

## Support
If you're having any problem, please raise an issue on GitHub


## License
The project is licensed under the Apache 2.0 license.
