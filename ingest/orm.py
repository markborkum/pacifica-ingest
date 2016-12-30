#!/usr/bin/python
"""ORM for index server."""
import os
import peewee

DB = peewee.MySQLDatabase(os.getenv('MYSQL_ENV_MYSQL_DATABASE', 'pacifica_ingest'),
                          host=os.getenv('MYSQL_PORT_3306_TCP_ADDR', '127.0.0.1'),
                          port=int(os.getenv('MYSQL_PORT_3306_TCP_PORT', 3306)),
                          user=os.getenv('MYSQL_ENV_MYSQL_USER', 'ingest'),
                          passwd=os.getenv('MYSQL_ENV_MYSQL_PASSWORD', 'ingest'))


# pylint: disable=too-few-public-methods
class BaseModel(peewee.Model):
    """Auto-generated by pwiz."""

    class Meta(object):
        """Map to the database connected above."""

        database = DB


class IngestState(BaseModel):
    """Map a python record to a mysql table."""

    job_id = peewee.BigIntegerField(primary_key=True, db_column='id')
    state = peewee.CharField(db_column='state')
    task = peewee.CharField(db_column='task')
    task_percent = peewee.DecimalField(db_column='task_percent')

    class Meta(object):
        """Map to uniqueindex table."""

        db_table = 'ingeststate'
# pylint: enable=too-few-public-methods


def update_state(job_id, state, task, task_percent):
    """Update the state of an ingest job."""
    if job_id and job_id >= 0:
        record = IngestState.get_or_create(job_id=job_id,
                                           defaults={'task': '', 'task_percent': 0, 'state': ''})[0]

        record.state = state
        record.task = task
        record.task_percent = task_percent
        record.save()


def read_state(job_id):
    """Return the state of an ingest job as a json object."""
    if job_id and job_id >= 0:
        record = IngestState.get(job_id=job_id)
    else:
        record = IngestState()
        record.state = 'DATA_ACCESS_ERROR'
        record.task = 'read_state'
        record.task_percent = 0

    return record
