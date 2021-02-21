from fastapi import APIRouter, Depends, HTTPException
from sqliteScripts import games_db, questions_db
from schemas import User, Game, Question, Responses, PlayedStats, Game_To_Answer, Question_To_Answer
from typing import List
from .usersApi import get_current_user, is_logged_user_admin
import random

router = APIRouter()


def get_questions_as_list_by_gameid(gameId: int):
    stackpath = "get_questions_as_list_by_gameid"
    print('\x1b[0;33;44m' + "def----->" + '\x1b[0m', stackpath )

    db_extracted_questions = questions_db.get_questions_by_gameid(gameId)

    questions: List[Question] = []
    for question in db_extracted_questions:
        item = Question.to_Question_model(question)
        questions.append(item)

    print('\x1b[0;33;44m' + "<-----def" + '\x1b[0m', stackpath)
    return questions

def get_game_as_gamemodel_by_id(gameId: int):
    stackpath = "get_game_as_gamemodel_by_id"
    print('\x1b[0;33;44m' + "def----->" + '\x1b[0m', stackpath )

    db_extracted_game = games_db.get_game_by_id(gameId)

    if (False == db_extracted_game):
        return False

    game = Game.to_Game_model(db_extracted_game)
    game.id = gameId

    print('\x1b[0;33;44m' + "<-----def" + '\x1b[0m', stackpath)
    return game


@router.post("/new_game")
def new_game(game: Game, questions: List[Question], isAdmin=Depends(is_logged_user_admin)):
    stackpath = "new_game"
    print('\x1b[0;30;44m' + "post------>" + '\x1b[0m', stackpath )
    
    game.questions_number = len(questions)

    db_game = games_db(game)
    new_game_id = db_game.createGame_returnId()
    
    db_questions = questions_db(questions)
    db_questions.create_questions(new_game_id)

    game.id = new_game_id

    print('\x1b[0;30;44m' + "<------post" + '\x1b[0m', stackpath )
    return {"game": game, "question": questions}


@router.get("/get_full_game_by_id")
def get_full_game_by_id(gameId: int, isAdmin=Depends(is_logged_user_admin)):
    stackpath = "get_full_game_by_id"
    print('\x1b[0;30;44m' + "get------>" + '\x1b[0m', stackpath )
    
    if (False == isAdmin):
        return {"restricted" : "just admins can get full game"}

    game = get_game_as_gamemodel_by_id(gameId)
    if (False == game):
        return {"No exist game with that id"}

    questions_list = get_questions_as_list_by_gameid(gameId)
    
    print('\x1b[0;30;44m' + "<------get" + '\x1b[0m', stackpath)
    return {"extracted_game": game, "extracted_questions" : questions_list}


@router.get("/get_game_to_play_by_id")
def get_game_to_play_by_id(gameId: int,  user: User=Depends(get_current_user)):
    stackpath = "get_game_to_play_by_id"
    print('\x1b[0;30;44m' + "get------>" + '\x1b[0m', stackpath )
    
    game = get_game_as_gamemodel_by_id(gameId)
    if (False == game):
        return {"No exist game with that id"}

    questions_list = get_questions_as_list_by_gameid(gameId)
    
    ready_game = Game_To_Answer()
    ready_game.game_id = game.id
    ready_game.game_name = game.game_name
    ready_game.questions_number = game.questions_number
    ready_game.questions = []

    for question in questions_list:
        ready_question = Question_To_Answer()
        ready_question.question_type = question.question_type
        ready_question.question = question.question
        ready_question.answers = question.correct_resp + question.other_variants
        random.shuffle(ready_question.answers)

        ready_game.questions.append(ready_question)


    print('\x1b[0;30;44m' + "<------get" + '\x1b[0m', stackpath)
    return ready_game


@router.post("/post_edit_game")
def post_edit_game_by_id(game: Game, questions: List[Question], isAdmin=Depends(is_logged_user_admin)):
    stackpath = "post_edit_game_by_id"
    print('\x1b[0;30;44m' + "post------>" + '\x1b[0m', stackpath )
    
    game.questions_number = len(questions)

    if not game.id:
        return {"error":"game to edit must have id"}
    
    for question in questions:
        if not question.id:
            return {"error":"all questions to edit must have id"}

    db_game = games_db(game)
    edittedgameid = db_game.edit_game(game.id)
    
    db_questions = questions_db(questions)
    db_questions.edit_questions_by_questionId()

    result = get_full_game_by_id(game.id)

    print('\x1b[0;30;44m' + "<------post" + '\x1b[0m', stackpath)
    return {"success":"game {gameId} editted".format(gameId=game.id)}


@router.post("/answer_game")
def answer_game(gameId: int, responses: List[Responses], user: User=Depends(get_current_user)):
    stackpath = "answer_game"
    print('\x1b[0;30;44m' + "post------>" + '\x1b[0m', stackpath )


    game_model = get_game_as_gamemodel_by_id(gameId)
    questions_list = get_questions_as_list_by_gameid(gameId)

    if (False == game_model):
        return {"No exist game with that id"}

    winned_points = 0

    #loop responses
    for response in responses:
        response.question_id

        for question in questions_list:
            some_wrong = False
            correct_answers = []

            #compare answer with response from necesary question
            if (question.id == response.question_id):
                correct_answers = question.correct_resp

                for answer in response.responses:
                    if not answer in correct_answers:
                        some_wrong = True
                        break

                if not some_wrong:
                    winned_points += question.winning_points

    played_statistic = PlayedStats(username=user.username,points=winned_points)
    games_db.update_game_played_statistics(gameId, played_statistic)
    
    print('\x1b[0;30;44m' + "<------post" + '\x1b[0m', stackpath)
    return {"winned_points" : winned_points}


@router.get("/clear-games")
def clear_games_table(isAdmin=Depends(is_logged_user_admin)):
	stackpath = "clear_games_table"
	print('\x1b[0;30;44m' + "get------>" + '\x1b[0m', stackpath)

	games_db.clear_games()
	
	print('\x1b[0;30;44m' + "<------get" + '\x1b[0m', stackpath)
	return True
