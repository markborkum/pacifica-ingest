#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Create the database for ingest state."""
from ingest.orm import create_tables


if __name__ == '__main__':
    create_tables()
