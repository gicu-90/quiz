from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from sqliteScripts import user_db
from schemas import User 
import bcrypt
import jwt

JWT_SECRET = "somekindofsecret"

oauth2scheme = OAuth2PasswordBearer(tokenUrl="login")


router = APIRouter()


def get_user_by_username(username: str):
	stackpath = "get_user_by_username"
	print('\x1b[0;33;44m' + "def----->" + '\x1b[0m', stackpath )

	user = user_db.get_user_by_username(username)
	
	if (False == user):
		return False

	print('\x1b[0;33;44m' + "<-----def" + '\x1b[0m', stackpath)
	return user

def authenticate_user(username: str, password: str):
	stackpath = "authenticate_user"
	print('\x1b[0;33;44m' + "def----->" + '\x1b[0m', stackpath )

	user = get_user_by_username(username=username)
	if (False == user):
		return False

	if not bcrypt.checkpw(password.encode('UTF-8'), user[2]):
		return False

	print('\x1b[0;33;44m' + "<-----def" + '\x1b[0m', stackpath)
	return user

def get_current_user(token: str = Depends(oauth2scheme)):
	stackpath = "get_current_user"
	print('\x1b[0;33;44m' + "def----->" + '\x1b[0m', stackpath )

	try:
		payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])

		user = user_db.get_user_by_id(payload["id"])
		user = User.to_User_model(user)
	except:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail='Invalid username or password'
		)

	print('\x1b[0;33;44m' + "<-----def" + '\x1b[0m', stackpath)
	return user
		
def create_user(user: User):
	stackpath = "create_user"
	print('\x1b[0;33;44m' + "def----->" + '\x1b[0m', stackpath )
	
	user.password = bcrypt.hashpw(user.password.encode('UTF-8'), bcrypt.gensalt(14))
	db_user = user_db(user)
	user.id = db_user.createUser_returnId()

	user = get_user_by_username(username=user.username)

	print("user created")
	print('\x1b[0;33;44m' + "<-----def" + '\x1b[0m', stackpath)
	return user



@router.post("/register")
def register_user(user: User):
	stackpath = "register_user"
	print('\x1b[0;30;44m' + "post------>" + '\x1b[0m', stackpath )
	
	exist_user = get_user_by_username(user.username)
	if (exist_user):
		raise HTTPException(
			status_code=400,
			detail='Username already taken'
		)

	new_user = create_user(user)

	usermodel = User.to_User_model(new_user)
	token = jwt.encode(usermodel.dict(), JWT_SECRET)
	
	print('\x1b[0;30;44m' + "<------post" + '\x1b[0m', stackpath )
	return {'access_token' : token, 'user_type' : usermodel.user_type}



@router.post("/login")
def login_generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
	stackpath = "login_generate_token"
	print('\x1b[0;30;44m' + "post------>" + '\x1b[0m', stackpath )

	user = authenticate_user(form_data.username, form_data.password)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail='Invalid username or password'
		)

	usermodel = User.to_User_model(user)
	token = jwt.encode(usermodel.dict(), JWT_SECRET)
	
	print('\x1b[0;30;44m' + "<------post" + '\x1b[0m', stackpath )
	return {'access_token' : token, 'user_type' : usermodel.user_type}



@router.get("/user/me", response_model=User)
def get_user(user: User = Depends(get_current_user)):
	stackpath = "get_user"
	print("get---->", stackpath)

	print("<----get", stackpath)
	return user



@router.get("/clear-users")
def clear_users_table():
	stackpath = "clear_users_table"
	print("get---->", stackpath)

	user_db.clear_users()
	
	print("<----get", stackpath)
	return True



@router.get("/get-user-by-id")
def get_user_by_id(userid: int):
	stackpath = "get_user_by_id"
	print("get---->", stackpath)	
	
	user = user_db.get_user_by_id(userid)
	
	if not user:
		return {"error" : "user not found"}
	
	print("<----get", stackpath)
	return user

