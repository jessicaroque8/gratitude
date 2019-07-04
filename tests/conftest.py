import pytest
import os
import sys
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.realpath(__file__)
        )
    )
)  # pylint: disable=fixme

from src import create_app
from models import db, Entry

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('/Users/jessicaroque/PersonalProjects/gratitude/tests/test-config.cfg')

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


@pytest.fixture(scope='module')
def init_db():
    # Create the database and the database table
    db.create_all()

    # Insert user data
    entry1 = Entry(title='Kombucha',
                   body='Because its good for the tummy')
    entry2 = Entry(title='Lemon bars',
                   body='Because its good for the soul')
    db.session.add(entry1)
    db.session.add(entry2)

    # Commit the changes for the users
    db.session.commit()

    yield db  # this is where the testing happens!

    db.drop_all()


@pytest.fixture(scope='module')
def new_entry():
    entry = Entry(title='Laptops',
                  body='Because they are portable')
    return entry
