from tic_tac_toe.core.board import DEFAULT_BOARD


async def test_create_game_route(test_client):
    response = await test_client.get("game/create")
    assert response.json()["board"] == DEFAULT_BOARD


async def test_delete_game(test_client):
    create_response = await test_client.get("game/create")
    response = await test_client.delete(f"game/{create_response.json()['id']}")
    assert response.status_code == 202


async def test_delete_game_none_deleted(test_client):
    response = await test_client.delete("game/10")
    assert response.status_code == 400


async def test_get_all_games_route(test_client):
    await test_client.get("game/create")
    await test_client.get("game/create")
    response = await test_client.get("game/all")
    assert len(response.json()) == 2


async def test_get_all_games_route_none(test_client):
    response = await test_client.get("game/all")
    assert response.status_code == 404


async def test_get_game_route(test_client):
    create_response = await test_client.get("game/create")
    response = await test_client.get(f"game/{create_response.json()['id']}")
    assert response.json()["board"] == create_response.json()["board"]


async def test_get_game_route_none(test_client):
    response = await test_client.get("game/10")
    assert response.status_code == 404


async def test_make_move_route(test_client):
    create_response = await test_client.get("game/create")
    move = {"game_id": create_response.json()["id"], "row": 0, "col": 0}
    response = await test_client.post("game/move", json=move)
    board = response.json()["board"]
    assert board[0][0] == "X"
    assert "O" in [x for y in board for x in y]


async def test_make_move_route_game_not_found(test_client):
    move = {"game_id": 10, "row": 0, "col": 0}
    response = await test_client.post("game/move", json=move)
    assert response.status_code == 404


async def test_make_move_route_invalid_move(test_client):
    create_response = await test_client.get("game/create")
    move = {"game_id": create_response.json()["id"], "row": 0, "col": 0}
    await test_client.post("game/move", json=move)
    response = await test_client.post("game/move", json=move)
    assert response.status_code == 400
