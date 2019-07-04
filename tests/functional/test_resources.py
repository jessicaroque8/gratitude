import pytest
from flask import json
from datetime import datetime as dt
from resources import get_entry
from models import Entry
from exceptions import NotFoundError

def test_get_entry(test_client, init_db):
    entry = get_entry(1)
    assert isinstance(entry[0], Entry)
    assert entry[0].title == 'Kombucha'
    assert entry[1] == None

    invalid_id = 5
    not_found_entry = get_entry(invalid_id)
    expected_error = {
        'error': {
            'message': f'Entry with ID {invalid_id} was not found.',
            'type': 'not_found'
        }
    }
    assert not_found_entry[0] == None
    assert isinstance(not_found_entry[1], dict)
    assert list(not_found_entry[1].keys())[0] == 'error'
    for x in not_found_entry[1]['error']:
        assert not_found_entry[1]['error'][x] == expected_error['error'][x]

def test_entryitem_get(test_client, init_db):
    response = test_client.get('/entries/1')
    loaded_response = json.loads(response.data)
    expected_response = {
        "id": 1,
        "title": "Kombucha",
        "body": "Because its good for the tummy"
    }
    assert response.status_code == 200
    for x in loaded_response:
        if not x == 'created_at':
            assert loaded_response[x] == expected_response[x]
        else:
            created_at = dt.fromisoformat(loaded_response[x])
            assert created_at.date() == dt.today().date()

def get_entryitem_put(test_client, init_db):
    json_body = json.dumps({
        "title": "Maize"
    })
    response = test_client.put('/entries/1', json_body)
    loaded_response = json.loads(response)
    assert response.status_code == 201
    assert loaded_response['title'] == "Maize"
