from flask import Flask, request, jsonify
import sqlite3
import time

app = Flask(__name__)
DB_PATH = "online_ranking.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rankings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            highest_floor INTEGER NOT NULL,
            clear_time REAL,
            created_at REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()


@app.route("/submit", methods=["POST"])
def submit_score():
    data = request.get_json()

    player_name = str(data.get("player_name", "NO NAME"))[:12]
    highest_floor = int(data.get("highest_floor", 1))
    clear_time = data.get("clear_time")

    if highest_floor < 1:
        highest_floor = 1

    if highest_floor > 999:
        highest_floor = 999

    if clear_time is not None:
        clear_time = float(clear_time)

        if clear_time <= 0:
            clear_time = None

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO rankings (
            player_name,
            highest_floor,
            clear_time,
            created_at
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            player_name,
            highest_floor,
            clear_time,
            time.time(),
        ),
    )

    conn.commit()
    conn.close()

    return jsonify({"ok": True})


@app.route("/rankings/floor", methods=["GET"])
def get_floor_ranking():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT player_name, MAX(highest_floor)
        FROM rankings
        GROUP BY player_name
        ORDER BY MAX(highest_floor) DESC
        LIMIT 10
    """)

    rows = cur.fetchall()
    conn.close()

    return jsonify([
        {
            "player_name": row[0],
            "highest_floor": row[1],
        }
        for row in rows
    ])


@app.route("/rankings/time", methods=["GET"])
def get_time_ranking():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT player_name, MIN(clear_time)
        FROM rankings
        WHERE clear_time IS NOT NULL
        GROUP BY player_name
        ORDER BY MIN(clear_time) ASC
        LIMIT 10
    """)

    rows = cur.fetchall()
    conn.close()

    return jsonify([
        {
            "player_name": row[0],
            "clear_time": row[1],
        }
        for row in rows
    ])


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)