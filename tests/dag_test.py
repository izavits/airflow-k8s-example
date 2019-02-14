"""DAG Unit Tests"""

import unittest
from airflow.models import DagBag

class TestDagIntegrity(unittest.TestCase):
    """Generic and DAG integrity tests."""

    LOAD_SECOND_THRESHOLD = 2

    VALID_DAG_OWNERS = set([
        'airflow',
        ])

    VALID_DAG_EMAILS = set([
        'airflow@example.com',
        ])
    

    def setUp(self):
        self.dagbag = DagBag()

    def test_import_dags(self):
        """Verify that Airflow will be abl to import the DAG."""
        self.assertFalse(
            len(self.dagbag.import_errors),
            'DAG import failures. Errors: {}'.format(
                self.dagbag.import_errors
            )
        )

    def test_alert_email_present(self):
        """Verify that an alert email is present."""
        for dag_id, dag in self.dagbag.dags.iteritems():
            emails = dag.default_args.get('email', [])
            msg = 'Alert email not set for DAG {id}'.format(id=dag_id)
            self.assertIn('airflow@example.com', emails, msg)

    def test_dag_emails(self):
        """Check that the DAG has a know email in the email list and a valid owner."""
        for dag_id, dag in self.dagbag.dags.iteritems():
            tasks_with_email_cnt = 0
            for task in dag.tasks:
                self._check_owner(task.owner, dag_id, task.task_id)
                if task.email:
                    self._check_email(task.email, dag_id, task.task_id)
                    tasks_with_email_cnt += 1

            if 'owner' in dag.default_args:
                self._check_owner(dag.default_args.get('owner', False), dag_id)
            if 'email' in dag.default_args:
                self._check_email(dag.default_args.get('email', False), dag_id)

            self.assertTrue(tasks_with_email_cnt == len(dag.tasks) or dag.default_args.get('email', False), \
                'Either all tasks or default_args must have email set: {}'.format(dag_id))


    def _check_owner(self, owner, dag_id, task_id=False):
        # Check owner against valid owner list.
        error_msg = 'DAG must have a valid owner ({}) defined: dag_id={}, task_id={}' \
            .format(self.VALID_DAG_OWNERS, dag_id, task_id)
        self.assertTrue(owner in self.VALID_DAG_OWNERS, error_msg)

    def _check_email(self, email, dag_id, task_id=False):
        # Airflow allows both a single email, as well as a list.
        emails = email if isinstance(email, list) else [email]
        error_msg = 'DAG must have a valid email ({}) defined: dag_id={}, task_id={}' \
            .format(self.VALID_DAG_EMAILS, dag_id, task_id)
        self.assertEqual(len(self.VALID_DAG_EMAILS.intersection(emails)), len(emails), error_msg)
        

            
class TestDAG(unittest.TestCase):
    """Check the k8s-sample DAG expectation."""

    def setUp(self):
        self.dagbag = DagBag()

    def test_task_count(self):
        """Check task count of k8s-sample dag"""
        dag_id='k8s-sample'
        dag = self.dagbag.get_dag(dag_id)
        self.assertEqual(len(dag.tasks), 4)

    def test_contain_tasks(self):
        """Check task contains in k8s-sample dag"""
        dag_id='k8s-sample'
        dag = self.dagbag.get_dag(dag_id)
        tasks = dag.tasks
        task_ids = list(map(lambda task: task.task_id, tasks))
        self.assertListEqual(task_ids, ['bash-task', 'first-task', 'nodejs-task', 'python-task'])

    def test_dependencies_of_first_task(self):
        """Check the task dependencies of first_task in k8s-sample dag"""
        dag_id='k8s-sample'
        dag = self.dagbag.get_dag(dag_id)
        first_task = dag.get_task('first-task')

        upstream_task_ids = list(map(lambda task: task.task_id, first_task.upstream_list))
        self.assertListEqual(upstream_task_ids, [])
        downstream_task_ids = list(map(lambda task: task.task_id, first_task.downstream_list))
        self.assertListEqual(downstream_task_ids, ['bash-task', 'nodejs-task', 'python-task'])

    def test_dependencies_of_bash_task(self):
        """Check the task dependencies of bash_task in k8s-sample dag"""
        dag_id='k8s-sample'
        dag = self.dagbag.get_dag(dag_id)
        bash_task = dag.get_task('bash-task')

        upstream_task_ids = list(map(lambda task: task.task_id, bash_task.upstream_list))
        self.assertListEqual(upstream_task_ids, ['first-task'])
        downstream_task_ids = list(map(lambda task: task.task_id, bash_task.downstream_list))
        self.assertListEqual(downstream_task_ids, [])


    def test_dependencies_of_nodejs_task(self):
        """Check the task dependencies of nodejs_task in k8s-sample dag"""
        dag_id='k8s-sample'
        dag = self.dagbag.get_dag(dag_id)
        nodejs_task = dag.get_task('nodejs-task')

        upstream_task_ids = list(map(lambda task: task.task_id, nodejs_task.upstream_list))
        self.assertListEqual(upstream_task_ids, ['first-task'])
        downstream_task_ids = list(map(lambda task: task.task_id, nodejs_task.downstream_list))
        self.assertListEqual(downstream_task_ids, [])

    def test_dependencies_of_python_task(self):
        """Check the task dependencies of python_task in k8s-sample dag"""
        dag_id='k8s-sample'
        dag = self.dagbag.get_dag(dag_id)
        python_task = dag.get_task('python-task')

        upstream_task_ids = list(map(lambda task: task.task_id, python_task.upstream_list))
        self.assertListEqual(upstream_task_ids, ['first-task'])
        downstream_task_ids = list(map(lambda task: task.task_id, python_task.downstream_list))
        self.assertListEqual(downstream_task_ids, [])

        
suite = unittest.TestLoader().loadTestsFromTestCase(TestDagIntegrity)
unittest.TextTestRunner(verbosity=2).run(suite)

suite2 = unittest.TestLoader().loadTestsFromTestCase(TestDAG)
unittest.TextTestRunner(verbosity=2).run(suite2)
