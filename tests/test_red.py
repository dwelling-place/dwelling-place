import pytest


@pytest.mark.skip(reason="How to juggle multiple apps?")
def test_list(client):
    assert client.get('/projects').status_code == 200


@pytest.mark.skip(reason="How to juggle multiple apps?")
def test_crud(client):
    resp = client.post('/projects', data={'name': 'spam'})
    assert resp.status_code == 201
    loc = resp.headers['Location']
    assert loc
    print(loc)

    resp = client.get(loc)
    assert resp.status_code == 200
    print(resp.json)
    assert resp.json['name'] == 'spam'

    resp = client.put(loc, data={'name': 'eggs'})
    assert resp.status_code in (200, 202, 204)

    resp = client.get(loc)
    assert resp.status_code == 200
    assert resp.json['name'] == 'eggs'

    resp = client.delete(loc)
    assert resp.status_code in (200, 202, 204)
