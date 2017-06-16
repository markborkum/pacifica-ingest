#!/usr/bin/python
"""ORM for index server."""
import os
import time
import peewee

DATABASE_CONNECT_ATTEMPTS = 20
DATABASE_WAIT = 5
DB = peewee.MySQLDatabase(os.getenv('MYSQL_ENV_MYSQL_DATABASE', 'pacifica_ingest'),
                          host=os.getenv('MYSQL_PORT_3306_TCP_ADDR', '127.0.0.1'),
                          port=int(os.getenv('MYSQL_PORT_3306_TCP_PORT', 3306)),
                          user=os.getenv('MYSQL_ENV_MYSQL_USER', 'ingest'),
                          passwd=os.getenv('MYSQL_ENV_MYSQL_PASSWORD', 'ingest'))


def create_tables(attempts=0):
    """Attempt to connect to the database."""
    try:
        if not IngestState.table_exists():
            IngestState.create_table()
    except peewee.OperationalError:
        if attempts < DATABASE_CONNECT_ATTEMPTS:
            time.sleep(DATABASE_WAIT)
            attempts += 1
            create_tables(attempts)
        else:
            raise peewee.OperationalError


# pylint: disable=too-few-public-methods
class BaseModel(peewee.Model):
    """Auto-generated by pwiz."""

    class Meta(object):
        """Map to the database connected above."""

        database = DB


class IngestState(BaseModel):
    """Map a python record to a mysql table."""

    job_id = peewee.BigIntegerField(primary_key=True, db_column='id')
    state = peewee.CharField()
    task = peewee.CharField()
    task_percent = peewee.DecimalField()

    @classmethod
    def database_connect(cls):
        """
        Make sure database is connected.

        Trying to connect a second
        time *does* cause problems.
        """
        # pylint: disable=no-member
        if cls._meta.database.is_closed():
            cls._meta.database.connect()
        # pylint: enable=no-member

    @classmethod
    def database_close(cls):
        """
        Close the database connection.

        Closing already closed database
        is not a problem, so continue on.
        """
        try:
            # pylint: disable=no-member
            cls._meta.database.close()
            # pylint: enable=no-member
        except peewee.ProgrammingError:  # pragma: no cover
            # error for closing an already closed database so continue on
            return

    class Meta(object):
        """Map to uniqueindex table."""

        db_table = 'ingeststate'
# pylint: enable=too-few-public-methods


def update_state(job_id, state, task, task_percent):
    """Update the state of an ingest job."""
    if job_id and job_id >= 0:
        IngestState.database_connect()
        record = IngestState.get_or_create(job_id=job_id,
                                           defaults={'task': '', 'task_percent': 0, 'state': ''})[0]

        record.state = state
        record.task = task
        record.task_percent = task_percent
        record.save()
        IngestState.database_close()


def read_state(job_id):
    """Return the state of an ingest job as a json object."""
    IngestState.database_connect()
    if job_id and job_id >= 0:
        record = IngestState.get(job_id=job_id)
    else:
        record = IngestState()
        record.state = 'DATA_ACCESS_ERROR'
        record.task = 'read_state'
        record.task_percent = 0
    IngestState.database_close()
    return record
