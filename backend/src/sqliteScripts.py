import sqlite3
from schemas import User  

# c.execute("""CREATE TABLE games (
# 		game_name text,
# 		questions_number int,
# 		played_statistics text
# 	)""")


# c.execute("""CREATE TABLE questions (
# 		game_id text,
# 		question_type text,
# 		question_order int,
# 		question text,
# 		correct_resp text,
# 		other_variants text,
# 		winning_points int
# 	)""")



# c.execute("""CREATE TABLE users (
# 		username text,
# 		password text,
# 		played_games int,
# 		total_winned_points int,
# 		user_type int
# 	)""")
	

class user_db(object):

	def __init__(self, user: User):
			self.username = user.username
			self.password = user.password
			self.total_winned_points = user.total_winned_points
			self.played_games = user.played_games
			self.user_type = user.user_type

		
	def clear_users():
		stackpath = "clear_users"
		print("sql---->", stackpath)

		conn = sqlite3.connect('quiz.db')
		c = conn.cursor()
		c.execute("DELETE FROM users")

		conn.commit()
		conn.close()
		print("all is cleared")
		print("<----sql", stackpath)


	def createUser_returnId(self):
		stackpath = "createUser_returnId"
		print("sql---->", stackpath)

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

		print("<----sql", stackpath)
		return userid


	def get_user_by_username(username: str):
			stackpath = "get_user_by_username"
			print("sql---->", stackpath)

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
			print("<----sql", stackpath)
			return items


	def get_user_by_id(rowid: int):
			stackpath = "get_user_by_id"
			print("sql---->", stackpath)

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
			print("<----sql", stackpath)
			return items

