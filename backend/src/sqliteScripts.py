import sqlite3
from schemas import User, Game, Question
from typing import List

class user_db(object):

	def __init__(self, user: User):
		self.username = user.username
		self.password = user.password
		self.total_winned_points = user.total_winned_points
		self.played_games = user.played_games
		self.user_type = user.user_type

		
	def clear_users():
		stackpath = "clear_users"
		print('\x1b[6;30;42m' + "sql---->" + '\x1b[0m', stackpath )

		conn = sqlite3.connect('quiz.db')
		c = conn.cursor()
		c.execute("DELETE FROM users")

		conn.commit()
		conn.close()

		print("all is cleared")
		print('\x1b[6;30;42m' + "<----sql" + '\x1b[0m', stackpath )


	def createUser_returnId(self):
		stackpath = "createUser_returnId"
		print('\x1b[6;30;42m' + "sql---->" + '\x1b[0m', stackpath )

		conn = sqlite3.connect('quiz.db')
		c = conn.cursor()
		userid = 0

		c.execute("""INSERT INTO users (
			username,
			password,
			played_games,
			total_winned_points,
			user_type
			) VALUES (?,?,?,?,?);""", (
				self.username,
				self.password,
				self.played_games,
				self.total_winned_points,
				self.user_type
				))

		userid =  c.lastrowid

		conn.commit()
		conn.close()
		print("new user created")

		print('\x1b[6;30;42m' + "<----sql" + '\x1b[0m', stackpath )
		return userid


	def get_user_by_username(username: str):
		stackpath = "get_user_by_username"
		print('\x1b[6;30;42m' + "sql---->" + '\x1b[0m', stackpath )

		conn = sqlite3.connect('quiz.db')
		c = conn.cursor()
		userid = 0

		c.execute("SELECT * FROM users WHERE username = '{username}' LIMIT 1".format(username=username))
		items = c.fetchone()

		if(items is None):
			print("no item match from query")
			print("<----sql", stackpath)
			return False

		items = (c.lastrowid,) + items

		conn.commit()
		conn.close()

		print("user extracted")
		print('\x1b[6;30;42m' + "<----sql" + '\x1b[0m', stackpath )
		return items


	def get_user_by_id(rowid: int):
		stackpath = "get_user_by_id"
		print('\x1b[6;30;42m' + "sql---->" + '\x1b[0m', stackpath )

		conn = sqlite3.connect('quiz.db')
		c = conn.cursor()
		userid = 0

		c.execute("SELECT * FROM users WHERE rowid={rowid};".format(rowid=rowid+1))

		items = c.fetchone()
			
		if(items is None):
			print("no item match from query")
			print("<----sql", stackpath)
			return False

		items = (c.lastrowid,) + items
			
		conn.commit()
		conn.close()

		print("user extracted")
		print('\x1b[6;30;42m' + "<----sql" + '\x1b[0m', stackpath )
		return items


class games_db(object):
	def __init__(self, game: Game):
		self.game_name = game.game_name
		self.questions_number = game.questions_number
		self.played_statistics = game.played_statistics

	def createGame_returnId(self):
		stackpath = "createGame_returnId"
		print('\x1b[6;30;42m' + "sql---->" + '\x1b[0m', stackpath )

		conn = sqlite3.connect('quiz.db')
		c = conn.cursor()
		userid = 0

		c.execute("""INSERT INTO games (
			game_name,
			questions_number,
			played_statistics
			) VALUES (?,?,?);""", (
				self.game_name,
				self.questions_number,
				self.played_statistics,
				))

		gameid =  c.lastrowid

		conn.commit()
		conn.close()
		print("new game created")

		print('\x1b[6;30;42m' + "<----sql" + '\x1b[0m', stackpath )
		return gameid

	def get_game_by_id(gameId: int):
		stackpath = "get_game_by_id"
		print('\x1b[6;30;42m' + "sql---->" + '\x1b[0m', stackpath )

		conn = sqlite3.connect('quiz.db')
		c = conn.cursor()
		userid = 0

		c.execute("SELECT * FROM games WHERE rowid = '{gameId}' LIMIT 1".format(gameId=gameId))
		items = c.fetchone()

		if(items is None):
			print("no item match from query")
			print("<----sql", stackpath)
			return False

		items = (c.lastrowid,) + items

		conn.commit()
		conn.close()

		print('\x1b[6;30;42m' + "<----sql" + '\x1b[0m', stackpath )
		return items

	def edit_game(self, gameId: int):
		stackpath = "edit_game"
		print('\x1b[6;30;42m' + "sql---->" + '\x1b[0m', stackpath )

		conn = sqlite3.connect('quiz.db')
		c = conn.cursor()
		userid = 0

		c.execute("""UPDATE games SET 
				game_name='{game_name}', 
				questions_number={questions_number}, 
				played_statistics='{played_statistics}' 
			WHERE rowid={gameId} """.format(
				game_name=self.game_name,
				questions_number=self.questions_number,
				played_statistics=self.played_statistics,
				gameId=gameId
			))

		conn.commit()
		conn.close()
		print("game editted")

		print('\x1b[6;30;42m' + "<----sql" + '\x1b[0m', stackpath )


class questions_db(object):
	def __init__(self, questions: List[Question]):
		self.questions = questions

	def create_questions(self, gameId: int):
		stackpath = "create_questions"
		print('\x1b[6;30;42m' + "sql---->" + '\x1b[0m', stackpath )

		conn = sqlite3.connect('quiz.db')
		c = conn.cursor()
		userid = 0

		for question in self.questions:
			c.execute("""INSERT INTO questions (
				game_id,
				question_type,
				question,
				correct_resp,
				other_variants,
				winning_points
				) VALUES (?,?,?,?,?,?);""", (
					gameId,
					question.question_type,
					question.question,
					question.correct_resp,
					question.other_variants,
					question.winning_points,
					))

		conn.commit()
		conn.close()
		print("new questions created")
		print('\x1b[6;30;42m' + "<----sql" + '\x1b[0m', stackpath )

	def get_questions_by_gameid(gameId: int):
		stackpath = "get_questions_by_gameid"
		print('\x1b[6;30;42m' + "sql---->" + '\x1b[0m', stackpath )

		conn = sqlite3.connect('quiz.db')
		c = conn.cursor()
		userid = 0

		c.execute("SELECT rowid, * FROM questions WHERE game_id = '{gameId}' ".format(gameId=gameId))
		items = c.fetchall()

		if(items is None):
			print("no item match from query")
			print("<----sql", stackpath)
			return False

		conn.commit()
		conn.close()

		print('\x1b[6;30;42m' + "<----sql" + '\x1b[0m', stackpath )
		return items
	
	def edit_questions_by_questionId(self):
		stackpath = "edit_questions_by_gameid"
		print('\x1b[6;30;42m' + "sql---->" + '\x1b[0m', stackpath )

		conn = sqlite3.connect('quiz.db')
		c = conn.cursor()
		userid = 0

		for question in self.questions:

			print(
					question.id,
					question.question_type,
					question.question,
					question.correct_resp,
					question.other_variants,
					question.winning_points
				)

			c.execute("""UPDATE questions SET 
					question_type='{question_type}',
					question='{question}',
					correct_resp='{correct_resp}',
					other_variants='{other_variants}',
					winning_points='{winning_points}'
				
				WHERE rowid={rowid} """.format(
					rowid=question.id,
					question_type=question.question_type,
					question=question.question,
					correct_resp=question.correct_resp,
					other_variants=question.other_variants,
					winning_points=question.winning_points
				))

		conn.commit()
		conn.close()
		print("new questions created")
		print('\x1b[6;30;42m' + "<----sql" + '\x1b[0m', stackpath )
