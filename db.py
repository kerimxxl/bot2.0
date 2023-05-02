import sqlite3
from sqlite3 import Error
from typing import List


class Database:
    def __init__(self):
        self.conn = self.create_connection("team_management.db")
        self.create_tables()

    def create_connection(self, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)

        return conn

    def create_tables(self):
        tasks_sql = """CREATE TABLE IF NOT EXISTS tasks (
                            user_id INTEGER NOT NULL,
                            task_name TEXT NOT NULL,
                            deadline TEXT NOT NULL
                        );"""

        events_sql = """CREATE TABLE IF NOT EXISTS events (
                            user_id INTEGER NOT NULL,
                            event_name TEXT NOT NULL,
                            event_date TEXT NOT NULL
                        );"""

        files_sql = """CREATE TABLE IF NOT EXISTS files (
                            user_id INTEGER NOT NULL,
                            file_id TEXT NOT NULL,
                            file_name TEXT NOT NULL
                        );"""

        self.conn.execute(tasks_sql)
        self.conn.execute(events_sql)
        self.conn.execute(files_sql)
        self.conn.commit()

def add_task_to_db(user_id: int, title: str, due_date: str):
    conn = sqlite3.connect("team_management.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (user_id, title, due_date) VALUES (?, ?, ?)", (user_id, title, due_date))
    conn.commit()
    conn.close()

def delete_task_from_db(task_id: int):
    conn = sqlite3.connect("team_management.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def add_event_to_db(user_id: int, name: str, date_time: str):
    conn = sqlite3.connect("team_management.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO events (user_id, name, date_time) VALUES (?, ?, ?)", (user_id, name, date_time))
    conn.commit()
    conn.close()

def delete_event_from_db(event_id: int):
    conn = sqlite3.connect("team_management.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM events WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()

def upload_file_to_db(user_id: int, file_id: str):
    conn = sqlite3.connect("team_management.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO files (user_id, file_id) VALUES (?, ?)", (user_id, file_id))
    conn.commit()
    conn.close()

def delete_file_from_db(file_id: int):
    conn = sqlite3.connect("team_management.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM files WHERE id = ?", (file_id,))
    conn.commit()
    conn.close()

def get_tasks_by_user_id(user_id: int) -> List[dict]:
    conn = sqlite3.connect("team_management.db")
    cur = conn.cursor()
    cur.execute("SELECT id, title, due_date FROM tasks WHERE user_id = ?", (user_id,))
    tasks = [{"id": row[0], "title": row[1], "due_date": row[2]} for row in cur.fetchall()]
    conn.close()
    return tasks

def get_events_by_user_id(user_id: int) -> List[dict]:
    conn = sqlite3.connect("team_management.db")
    cur = conn.cursor()
    cur.execute("SELECT id, name, date_time FROM events WHERE user_id = ?", (user_id,))
    events = [{"id": row[0], "name": row[1], "date_time": row[2]} for row in cur.fetchall()]
    conn.close()
    return events

def get_files_by_user_id(user_id: int) -> List[dict]:
    conn = sqlite3.connect("team_management.db")
    cur = conn.cursor()
    cur.execute("SELECT id, file_id FROM files WHERE user_id = ?", (user_id,))
    files = [{"id": row[0], "file_id": row[1]} for row in cur.fetchall()]
    conn.close()
    return files
