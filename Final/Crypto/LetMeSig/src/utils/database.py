import sqlite3
from os.path import abspath, dirname, exists
from os import makedirs, remove


class Database:
	def __init__(self, db_path):
		self.db_path = db_path
		self.init_path(db_path)
		self.cli = sqlite3.connect(db_path, check_same_thread=False)
		self.init_db()

	def init_path(self, db_path):
		if exists(db_path):
			remove(db_path)
		p = dirname(abspath(db_path))
		if not exists(p):
			makedirs(p)

	def init_db(self):
		cursor = self.cli.cursor()
		cursor.executescript("CREATE TABLE IF NOT EXISTS users (user TEXT NOT NULL, sig TEXT NOT NULL);")
		cursor.executescript("CREATE TABLE IF NOT EXISTS notes (user TEXT NOT NULL, content TEXT NOT NULL);")
		self.cli.commit()

	def add_user(self, username, sig):
		cursor = self.cli.cursor()
		cursor.execute("INSERT INTO users VALUES(:user,:sig)", {
			'user': username,
			'sig': sig
			})
		self.cli.commit()

	def fetch_user(self, user):
		res = self.cli.cursor().execute("SELECT * from users WHERE user=:user", {
			'user': user
			}).fetchone()
		self.cli.commit
		return res

	def fetch_user_by_sig(self, sig):
		res = self.cli.cursor().execute("SELECT user from users WHERE sig=:sig", {
			'sig': sig
			}).fetchone()
		self.cli.commit
		return res

	def login_by_sig(self, user, sig):
		res = self.cli.cursor().execute("SELECT user from users WHERE sig=:sig and user=:user", {
			'user': user,
			'sig': sig
			}).fetchone()
		self.cli.commit
		return res

	def add_note(self, username, content):
		cursor = self.cli.cursor()
		cursor.execute("INSERT INTO notes VALUES(:user,:content)", {
			'user': username,
			'content': content
			})
		self.cli.commit()

	def fetch_notes(self, user):
		res = self.cli.cursor().execute("SELECT content from notes WHERE user=:user", {
			'user': user
			}).fetchall()
		self.cli.commit
		return res

database = Database(db_path='users.db')
