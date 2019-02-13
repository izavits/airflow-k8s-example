# Simple example showing how the kubernetes POD operator can be used with airflow.
# This example creates a DAG with four tasks: a dummy one, and  three more tasks
# running in three separate PODs in a local kubernetes cluster.

# import the necessary libraries
from airflow import DAG
from datetime import datetime, timedelta
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.operators.dummy_operator import DummyOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.utcnow(),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=3)
    }

dag = DAG('k8s-sample', default_args=default_args, schedule_interval=timedelta(minutes=5))

first_task = DummyOperator(task_id='first-task', dag=dag)

# Create the tasks using images from dockerhub
# Create a kubernetes pod using a python image
python_task = KubernetesPodOperator(namespace='default',
                                    image="python:3.6",
                                    cmds=["python","-c"],
                                    arguments=["print('[PYTHON TASK] Hello world!')"],
                                    labels={"foo": "bar"},
                                    name="python-k8s-task",
                                    task_id="python-task",
                                    get_logs=True,
                                    dag=dag
)

# Create a kubernetes pod using an ubuntu image
bash_task = KubernetesPodOperator(namespace='default',
                                  image="ubuntu:16.04",
                                  cmds=["echo"],
                                  arguments=["[BASH TASK] Hi world!"],
                                  labels={"foo": "bar"},
                                  name="bash-k8s-task",
                                  task_id="bash-task",
                                  get_logs=True,dag=dag
)

# Create a kubernetes pod using a nodejs image
node_task = KubernetesPodOperator(namespace='default',
                                  image="owncloudci/nodejs",
                                  cmds=["node", "-e"],
                                  arguments=["console.log('[NODEJS TASK] Hey world!')"],
                                  labels={"foo": "bar"},
                                  name="nodejs-k8s-task",
                                  task_id="nodejs-task",
                                  get_logs=True,
                                  dag=dag
)


# Define the order of the tasks in the DAG
python_task.set_upstream(first_task)
bash_task.set_upstream(first_task)
node_task.set_upstream(first_task)
