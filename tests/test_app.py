import pytest
from app import app


@pytest.fixture()
def client():
    with app.test_client() as client:
        yield client


def test_get_list_available_moves_invalid_figure(client):
    response = client.get("/api/v1/non_existing_figure/a4")
    data = response.json
    assert "invalid figure" in data["error"]
    assert "a4" in data["currentField"]
    assert data["availableMoves"] == []
    assert response.status_code == 404


def test_get_list_available_moves_invalid_field(client):
    response = client.get("/api/v1/pawn/a9")
    data = response.json
    assert "current field does not exist" in data["error"]
    assert data["availableMoves"] == []
    assert response.status_code == 409


def test_get_list_available_moves_valid_knight(client):
    response = client.get("/api/v1/knight/d4")
    data = response.json
    assert "B3" and "B5" and "C2" and "C6" and "E2" in data["availableMoves"]
    assert len(data["availableMoves"]) == 8
    assert "knight" in data["figure"]
    assert response.status_code == 200


def test_get_list_available_moves_valid_pawn_first_row(client):
    response = client.get("/api/v1/pawn/e1")
    data = response.json
    assert data["availableMoves"]["forBlacks"] == []
    assert data["availableMoves"]["forWhites"] == []
    assert "invalid field for figure" in data["error"]["forWhites"]
    assert data["error"]["forBlacks"] is None
    assert response.status_code == 200


def test_get_list_available_moves_valid_pawn_second_row(client):
    response = client.get("/api/v1/pawn/a2")
    data = response.json
    assert "A1" in data["availableMoves"]["forBlacks"]
    assert "A3" and "A4" in data["availableMoves"]["forWhites"]
    assert data["error"]["forWhites"] is None
    assert data["error"]["forBlacks"] is None
    assert "pawn" in data["figure"]
    assert response.status_code == 200


def test_get_list_available_moves_valid_pawn_sixth_row(client):
    response = client.get("/api/v1/pawn/g6")
    data = response.json
    assert "G5" in data["availableMoves"]["forBlacks"]
    assert len(data["availableMoves"]["forBlacks"]) == 1
    assert "G7" in data["availableMoves"]["forWhites"]
    assert len(data["availableMoves"]["forWhites"]) == 1
    assert data["error"]["forWhites"] is None
    assert data["error"]["forBlacks"] is None
    assert response.status_code == 200


def test_get_list_available_moves_valid_pawn_seventh_row(client):
    response = client.get("/api/v1/pawn/b7")
    data = response.json
    assert "B6" and "B5" in data["availableMoves"]["forBlacks"]
    assert len(data["availableMoves"]["forBlacks"]) == 2
    assert "B8" in data["availableMoves"]["forWhites"]
    assert len(data["availableMoves"]["forWhites"]) == 1
    assert data["error"]["forWhites"] is None
    assert data["error"]["forBlacks"] is None
    assert response.status_code == 200


def test_get_list_available_moves_valid_pawn_eighth_row(client):
    response = client.get("/api/v1/pawn/c8")
    data = response.json
    assert data["availableMoves"]["forBlacks"] == []
    assert data["availableMoves"]["forWhites"] == []
    assert data["error"]["forWhites"] is None
    assert "invalid field for figure" in data["error"]["forBlacks"]
    assert response.status_code == 200


def test_get_list_available_moves_valid_king(client):
    response = client.get("/api/v1/king/b1")
    data = response.json
    assert "A1" and "A2" and "B2" and "C1" and "C2" in data["availableMoves"]
    assert len(data["availableMoves"]) == 5
    assert data["error"] is None
    assert "king" in data["figure"]
    assert response.status_code == 200


def test_get_list_available_moves_valid_rook(client):
    response = client.get("/api/v1/rook/h4")
    data = response.json
    assert "A4" and "H8" and "H1" and "E4" in data["availableMoves"]
    assert len(data["availableMoves"]) == 14
    assert data["error"] is None
    assert "rook" in data["figure"]
    assert response.status_code == 200


def test_get_list_available_moves_valid_bishop(client):
    response = client.get("/api/v1/bishop/d6")
    data = response.json
    assert "C7" and "E7" and "H2" in data["availableMoves"]
    assert len(data["availableMoves"]) == 11
    assert data["error"] is None
    assert "bishop" in data["figure"]
    assert response.status_code == 200


def test_get_list_available_moves_valid_queen(client):
    response = client.get("/api/v1/queen/F8")
    data = response.json
    assert "H8" and "A8" and "F1" and "F4" in data["availableMoves"]
    assert len(data["availableMoves"]) == 21
    assert data["error"] is None
    assert "queen" in data["figure"]
    assert response.status_code == 200


def test_validate_move_invalid_figure(client):
    response = client.get("/api/v1/non_existing_figure/a4/b5")
    data = response.json
    assert "invalid figure" in data["error"]
    assert data["move"] == "invalid"
    assert response.status_code == 404


def test_validate_move_invalid_current_field(client):
    response = client.get("/api/v1/king/a9/b5")
    data = response.json
    assert "current field does not exist" in data["error"]
    assert data["move"] == "invalid"
    assert response.status_code == 409


def test_validate_move_invalid_dest_field(client):
    response = client.get("/api/v1/king/a4/b9")
    data = response.json
    assert "destination field does not exist" in data["error"]
    assert data["move"] == "invalid"
    assert response.status_code == 409


def test_validate_move_valid_figure_permitted_move(client):
    response = client.get("/api/v1/queen/d4/e5")
    data = response.json
    assert "valid" in data["move"]
    assert "queen" in data["figure"]
    assert "d4" in data["currentField"]
    assert "e5" in data["destField"]
    assert data["error"] is None
    assert response.status_code == 200


def test_validate_move_valid_figure_not_permitted_move(client):
    response = client.get("/api/v1/king/d4/h5")
    data = response.json
    assert "invalid" in data["move"]
    assert data["error"] == "current move is not permitted"
    assert response.status_code == 200


def test_validate_move_valid_for_white_pawn(client):
    response = client.get("/api/v1/pawn/a2/a4")
    data = response.json
    assert "invalid" in data["move"]["forBlacks"]
    assert "valid" in data["move"]["forWhites"]
    assert "current move is not permitted" in data["error"]["forBlacks"]
    assert data["error"]["forWhites"] is None
    assert response.status_code == 200


def test_validate_move_valid_for_black_pawn(client):
    response = client.get("/api/v1/pawn/c7/c6")
    data = response.json
    assert "valid" in data["move"]["forBlacks"]
    assert "invalid" in data["move"]["forWhites"]
    assert data["error"]["forBlacks"] is None
    assert "current move is not permitted" in data["error"]["forWhites"]
    assert response.status_code == 200


def test_validate_move_invalid_for_both_color_pawn(client):
    response = client.get("/api/v1/pawn/d4/e3")
    data = response.json
    assert "invalid" in data["move"]["forBlacks"]
    assert "invalid" in data["move"]["forWhites"]
    assert "current move is not permitted" in data["error"]["forBlacks"]
    assert "current move is not permitted" in data["error"]["forWhites"]
    assert response.status_code == 200
