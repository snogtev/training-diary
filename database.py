import sqlite3
from constants import DB_NAME

connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS workouts (
id INTEGER PRIMARY KEY AUTOINCREMENT,
date TEXT UNIQUE
)         
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS exercises (
id INTEGER PRIMARY KEY AUTOINCREMENT,
workout_id INTEGER,
exercise TEXT,
weight REAL,
sets INTEGER,
reps INTEGER,
FOREIGN KEY (workout_id) REFERENCES workouts (id)
)         
''')

connection.commit()