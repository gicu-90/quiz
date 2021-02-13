from pydantic import BaseModel, validator, Field
from datetime import date
from typing import List
from enum import Enum
import bcrypt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

class User_Type(Enum):
	User = 0
	Admin = 1

class User(BaseModel):
	id: int
	username: str = Field(..., max_length=100)
	password_hash: str = Field(..., min_length=3)
	total_winned_points: int = 0
	played_games: int = 0

	user_type: int = User_Type.User.value
	
	def to_User_model(db_model):
		(id, username, password_hash, total_winned_points, played_games, user_type) = db_model

		usermodel = User(
			id=id, 
			username=username, 
			password_hash=password_hash, 
			total_winned_points=total_winned_points, 
			played_games=played_games, 
			user_type=user_type
		) 
		
		return usermodel





