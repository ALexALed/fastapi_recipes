import csv
import os

import pytest

from todo_app import operations


@pytest.fixture(autouse=True)
def create_file(tmp_path_factory):
    with open('test_tasks.csv', 'w+') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(operations.column_fields)
    yield
    os.remove('test_tasks.csv')
