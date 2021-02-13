from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqliteScripts import user_db
from schemas import User 
import bcrypt
import jwt

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


JWT_SECRET = "somekindofsecret"

oauth2scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate_user(username: str, password: str):
	user = user_db.get_user_by_username(username=username)
	if not user:
		return False

	if not bcrypt.checkpw(password.encode('UTF-8'), user[2]):
		return False

	return user

def get_current_user(token: str = Depends(oauth2scheme)):

	try:
		payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])

		user = user_db.get_user_by_id(payload["id"])
		user = User.to_User_model(user)
	except:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail='Invalid username or password'
		)


	return user
		

@app.get("/")
def home():
	return {"keyHello"}

@app.post("/create-user", response_model=User)
def create_user(user: User):
	user.password_hash = bcrypt.hashpw(user.password_hash.encode('UTF-8'), bcrypt.gensalt(14))
	db_user = user_db(user)
	user.id = db_user.createUser_returnId()
	print("user created")
	return user


@app.post("/token")
def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
	user = authenticate_user(form_data.username, form_data.password)

	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail='Invalid username or password'
		)

	usermodel = User.to_User_model(user)

	token = jwt.encode(usermodel.dict(), JWT_SECRET)

	return {'access_token' : token, 'token_type' : 'bearer'}



@app.get("/user/me", response_model=User)
def get_user(user: User = Depends(get_current_user)):
	return user



@app.get("/clear-users")
def clear_users_table():
	user_db.clear_users()
	return True


@app.get("/get-user-by-id")
def get_user_by_id(userid: int):
	user = user_db.get_user_by_id(userid)
	
	if not user:
		return {"error" : "user not found"}
	
	return user


