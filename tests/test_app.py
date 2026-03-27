from pathlib import Path

from app.app import create_app


def test_home_page_loads(tmp_path: Path):
    db_path = tmp_path / "test_feedback.db"
    app = create_app(str(db_path))
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Student Feedback Portal" in response.data


def test_submit_feedback(tmp_path: Path):
    db_path = tmp_path / "test_feedback.db"
    app = create_app(str(db_path))
    client = app.test_client()

    response = client.post(
        "/submit",
        data={"name": "Rahul", "message": "DevOps lab was very useful."},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Rahul" in response.data
    assert b"DevOps lab was very useful." in response.data
