from dagster import job

from demo_dagster import my_op


@job
def my_job():
    """
    A job definition. This example job has a single op.

    For more hints on writing Dagster jobs, see our documentation overview on Jobs:
    https://docs.dagster.io/concepts/ops-jobs-graphs/jobs-graphs
    """
    my_op.my_op()

@job
def hello_op_job(
    dataset_url: str,
    dataset_name: str,
    db_conn_string: str,
):
    """The main ETL function"""
    df = my_op.fetch(dataset_url)
    df_clean = my_op.clean(df)
    my_op.write_db(df_clean, db_conn_string, dataset_name)