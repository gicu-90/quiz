from pydantic import BaseModel, validator, Field
from datetime import date
from typing import List, Optional
from enum import Enum
import bcrypt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

class User_Type(Enum):
	User = 0
	Admin = 1

class User(BaseModel):
	id: int = 0
	username: str = Field(..., max_length=100)
	password: str = Field(..., min_length=3)
	total_winned_points: int = 0
	played_games: int = 0

	user_type: int = User_Type.User.value
	
	def to_User_model(db_model):
		stackpath = "to_User_model"
		print("def-model---->", stackpath)

		(id, username, password_hash, total_winned_points, played_games, user_type) = db_model

		usermodel = User(
			id=id, 
			username=username, 
			password=password_hash, 
			total_winned_points=total_winned_points, 
			played_games=played_games, 
			user_type=user_type
		) 
		
		print("<----def-model", stackpath)
		return usermodel


	
class Question_Type(Enum):
	RADIOBTN = 0
	CHECKBOX = 1
	
class Game(BaseModel):
	id: int = None
	game_name: str = Field(..., max_length=100)
	questions_number: int = None
	played_statistics: str = None
	
	def to_Game_model(db_model):
		stackpath = "to_Game_model"
		print("def-model---->", stackpath)

		(id, game_name, questions_number, played_statistics) = db_model

		gamemodel = Game(
			id=id, 
			game_name=game_name, 
			questions_number=questions_number, 
			played_statistics=played_statistics 
		) 
		
		print("<----def-model", stackpath)
		return gamemodel

class Question(BaseModel):
	id: int = None
	game_id: int = None
	question_type: str 
	question: str = Field(...)
	correct_resp: str = Field(...)
	other_variants: str = Field(...)
	winning_points: int = Field(...)
	
	def to_Question_model(db_model):
		stackpath = "to_Question_model"
		print("def-model---->", stackpath)

		(id, game_id, question_type, question, correct_resp, other_variants, winning_points) = db_model

		questionmodel = Question(
			id=id,
			game_id=game_id, 
			question_type=question_type, 
			question=question,
			correct_resp=correct_resp,
			other_variants=other_variants,
			winning_points=winning_points 
		) 
		
		print("<----def-model", stackpath)
		return questionmodel
