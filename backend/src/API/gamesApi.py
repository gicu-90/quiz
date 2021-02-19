from fastapi import APIRouter, Depends, HTTPException
from sqliteScripts import games_db, questions_db
from schemas import Game, Question
from typing import List

router = APIRouter()


def get_questions_by_gameid(gameId: int):
    stackpath = "get_questions_by_gameid"
    print('\x1b[0;33;44m' + "def----->" + '\x1b[0m', stackpath )

    db_extracted_questions = questions_db.get_questions_by_gameid(gameId)

    print('\x1b[0;33;44m' + "<-----def" + '\x1b[0m', stackpath)
    return db_extracted_questions


@router.post("/new_game")
async def new_game(game: Game, questions: List[Question]):
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
async def get_full_game_by_id(gameId: int):
    stackpath = "get_full_game_by_id"
    print('\x1b[0;30;44m' + "get------>" + '\x1b[0m', stackpath )

    db_extracted_game = games_db.get_game_by_id(gameId)

    if (False == db_extracted_game):
        return {"No exist game with that id"}

    db_extracted_questions = get_questions_by_gameid(gameId)

    game = Game.to_Game_model(db_extracted_game)

    questions: List[Question] = []
    for question in db_extracted_questions:
        print(question)
        item = Question.to_Question_model(question)
        questions.append(item)
    
    print('\x1b[0;30;44m' + "<------get" + '\x1b[0m', stackpath)
    return {"extracted_game": game, "extracted_questions" : questions}


@router.post("/post_edit_game_by_id")
async def post_edit_game_by_id(game: Game, questions: List[Question]):
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

    print(result)

    print('\x1b[0;30;44m' + "<------post" + '\x1b[0m', stackpath)
    return 

