from datetime import datetime as dt

def test_new_entry(new_entry):
    """
    GIVEN an Entry model
    WHEN a new Entry is created
    THEN check that the id, title, body, and created_at fields are created
    """

    assert new_entry.title == 'Laptops'
    assert new_entry.body == 'Because they are portable'
    assert isinstance(new_entry.created_at, dt)
