# db.py
import sqlite3
from contextlib import closing

class DatabaseManager:
    def __init__(self, db_path="game.db"):
        self.db_path = db_path
        self._init_schema()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_schema(self):
        with closing(self._connect()) as conn, conn, closing(conn.cursor()) as c:
            # users table
            c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                name         TEXT    UNIQUE NOT NULL,
                age          INTEGER NOT NULL,
                gender       TEXT    NOT NULL,
                health       INTEGER NOT NULL,
                speed        INTEGER NOT NULL,
                strength     INTEGER NOT NULL,
                durability   INTEGER NOT NULL
            );
            """)

            # items table: both moves (Punch, Steal) and abilities
            c.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                name             TEXT    UNIQUE NOT NULL,
                stat_target      TEXT,
                boost_value      INTEGER,
                penalty_value    INTEGER,
                active_duration  INTEGER,
                penalty_duration INTEGER,
                is_borrowed      INTEGER DEFAULT 0
            );
            """)

            # borrowings history table
            c.execute("""
            CREATE TABLE IF NOT EXISTS borrowings (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id      INTEGER NOT NULL,
                item_id      INTEGER NOT NULL,
                borrowed_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                returned_at  TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(item_id) REFERENCES items(id)
            );
            """)

    # User
    def add_user(self, name, age, gender, health, speed, strength, durability):
        with closing(self._connect()) as conn, conn, closing(conn.cursor()) as c:
            c.execute("""
                INSERT OR IGNORE INTO users (name, age, gender, health, speed, strength, durability)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ;""", (name, age, gender, health, speed, strength, durability))
            return c.lastrowid or self.get_user_by_name(name)["id"]

    def get_user_by_name(self, name):
        with closing(self._connect()) as conn, closing(conn.cursor()) as c:
            c.execute("SELECT * FROM users WHERE name = ?", (name,))
            row = c.fetchone()
            return dict(zip([col[0] for col in c.description], row)) if row else None

    #Item
    def add_item(self, name, stat_target=None, boost_value=None,
                 penalty_value=None, active_duration=None, penalty_duration=None):
        with closing(self._connect()) as conn, conn, closing(conn.cursor()) as c:
            c.execute("""
                INSERT OR IGNORE INTO items
                  (name, stat_target, boost_value, penalty_value, active_duration, penalty_duration)
                VALUES (?, ?, ?, ?, ?, ?)
            ;""", (name, stat_target, boost_value, penalty_value, active_duration, penalty_duration))
            return c.lastrowid or self.get_item_by_name(name)["id"]

    def get_item_by_name(self, name):
        with closing(self._connect()) as conn, closing(conn.cursor()) as c:
            c.execute("SELECT * FROM items WHERE name = ?", (name,))
            row = c.fetchone()
            return dict(zip([col[0] for col in c.description], row)) if row else None

    def list_available_items(self):
        with closing(self._connect()) as conn, closing(conn.cursor()) as c:
            c.execute("SELECT * FROM items WHERE is_borrowed = 0")
            rows = c.fetchall()
            return [dict(zip([col[0] for col in c.description], row)) for row in rows]

    #Borrowing 
    def borrow_item(self, user_id, item_id):
        with closing(self._connect()) as conn, conn, closing(conn.cursor()) as c:
            # ensure it's not already borrowed
            c.execute("SELECT is_borrowed FROM items WHERE id = ?", (item_id,))
            if c.fetchone()[0]:
                raise ValueError("Item is already borrowed.")
            # mark as borrowed
            c.execute("UPDATE items SET is_borrowed = 1 WHERE id = ?", (item_id,))
            # record history
            c.execute("""
                INSERT INTO borrowings (user_id, item_id)
                VALUES (?, ?)
            ;""", (user_id, item_id))

    def return_item(self, user_id, item_id):
        with closing(self._connect()) as conn, conn, closing(conn.cursor()) as c:
            # mark as returned
            c.execute("UPDATE items SET is_borrowed = 0 WHERE id = ?", (item_id,))
            # update history
            c.execute("""
                UPDATE borrowings
                   SET returned_at = CURRENT_TIMESTAMP
                 WHERE user_id = ? AND item_id = ? AND returned_at IS NULL
            ;""", (user_id, item_id))

    def get_borrow_history(self, user_id):
        with closing(self._connect()) as conn, closing(conn.cursor()) as c:
            c.execute("""
                SELECT b.id, i.name, b.borrowed_at, b.returned_at
                  FROM borrowings b
                  JOIN items i ON b.item_id = i.id
                 WHERE b.user_id = ?
                 ORDER BY b.borrowed_at DESC
            ;""", (user_id,))
            rows = c.fetchall()
            return [dict(zip([col[0] for col in c.description], row)) for row in rows]
