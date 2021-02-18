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


	
class Game(BaseModel):
	id: int = None
	game_name: str = Field(..., max_length=100)
	questions_number: int = None
	played_statistics: str = None

class Question(BaseModel):
	id: int = None
	game_id: int = None
	question_type: str = None
	question: str = None
	correct_resp: str = None
	other_variants: str = None
	winning_points: int = None

