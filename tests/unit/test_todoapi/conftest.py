import pytest

from todoapi import create_app
from todoapi.models.todo import TodoModel


def setup_ddb():
    TodoModel.create_table(wait=True, read_capacity_units=5, write_capacity_units=5)
    TodoModel("1", task="Make up your mind!").save()


def teardown_ddb():
    TodoModel.delete_table()


@pytest.fixture
def client():
    """Create and configure a new app instance for each test."""
    app = create_app({"TESTING": False})

    with app.test_client() as client:
        with app.app_context():
            setup_ddb()
            yield client
            teardown_ddb()
