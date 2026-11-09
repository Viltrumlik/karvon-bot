"""SQLite storage: player sessions round-trip, runs and the leaderboard."""
from __future__ import annotations

from datetime import datetime

from karvon.storage import Storage


def test_player_round_trip(tmp_path):
    db = Storage(str(tmp_path / "s.db"))
    assert db.load_player(1) is None
    db.save_player(1, "uz", {"screen": "hub", "game": None, "name": "Ali «x»"}, 1001)
    rec = db.load_player(1)
    assert rec["lang"] == "uz" and rec["msg_id"] == 1001 and rec["state"]["name"] == "Ali «x»"
    assert datetime.fromisoformat(rec["updated_at"]).tzinfo is not None  # ISO-8601 UTC
    db.save_player(1, "ru", {"screen": "menu"}, 1002)
    rec = db.load_player(1)
    assert rec["lang"] == "ru" and rec["msg_id"] == 1002 and rec["state"] == {"screen": "menu"}
    db.close()


def test_leaderboard_best_run_per_player(tmp_path):
    db = Storage(str(tmp_path / "s.db"))
    db.add_run(1, "Ali", "E5", 100, 101, "hard")
    db.add_run(1, "Ali", "E2", 9000, 80, "hard")
    db.add_run(2, "Vera", "E1", 20000, 150, "legendary")
    db.add_run(3, "Tom", "E6", 50, 30, "normal")
    top = db.top(10)
    assert [r["name"] for r in top] == ["Vera", "Ali", "Tom"]
    assert top[1]["score"] == 9000 and db.runs_count() == 4
    assert len(db.top(2)) == 2
    db.close()


def test_database_survives_reopen(tmp_path):
    path = str(tmp_path / "s.db")
    db = Storage(path)
    db.add_run(5, "Zed", "E3", 10, 99, "hard")
    db.close()
    db = Storage(path)
    assert db.runs_count() == 1
    db.close()
