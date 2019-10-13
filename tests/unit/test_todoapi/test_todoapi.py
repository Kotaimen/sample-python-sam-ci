def test_get_todo(client):
    rv = client.get("/api/v1/todos/todo/1")
    data = {"data": {"id": "1", "task": "Make up your mind!"}}
    assert rv.json == data
    assert rv.status_code == 200


def test_get_todo_mssing(client):
    rv = client.get("/api/v1/todos/todo/111")
    assert rv.status_code == 404


def test_put_todo(client):
    rv = client.put("/api/v1/todos/todo/2", json={"task": "BOB180"})
    data = {"data": {"id": "2", "task": "BOB180"}}
    assert rv.json == data
    assert rv.status_code == 200

    rv = client.get("/api/v1/todos/todo/2")
    assert rv.json == data


def test_put_todo_duplicate(client):
    rv = client.put("/api/v1/todos/todo/1", json={"task": "BOB180"})
    assert rv.status_code == 200


def test_delete_todo(client):
    rv = client.put("/api/v1/todos/todo/3", json={"task": "BOB180"})
    rv = client.get("/api/v1/todos/todo/3")
    assert rv.status_code == 200

    rv = client.delete("/api/v1/todos/todo/3")
    assert rv.status_code == 204

    rv = client.get("/api/v1/todos/todo/3")
    assert rv.status_code == 404

    # DeleteItem is an idempotent operation; running it multiple times on the same
    # item or attribute does not result in an error response.
    rv = client.delete("/api/v1/todos/todo/333")
    assert rv.status_code == 204
