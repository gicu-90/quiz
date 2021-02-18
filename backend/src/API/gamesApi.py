from fastapi import APIRouter, Depends, HTTPException
from sqliteScripts import games_db, questions_db
from schemas import Game, Question
from typing import List

router = APIRouter()

@router.post("/new_game")
async def new_game(game: Game, questions: List[Question]):
    stackpath = "new_game"
    print('\x1b[0;30;44m' + "post------>" + '\x1b[0m', stackpath )
    
    game.questions_number = len(questions)

    db_game = games_db(game)
    new_game_id = db_game.createGame_returnId()
    
    db_questions = questions_db(questions)
    db_questions.create_questions(new_game_id)


    print('\x1b[0;30;44m' + "<------post" + '\x1b[0m', stackpath )
    return {"game": game, "question": questions}


def get_questions_by_gameid(gameId: int):
    stackpath = "get_questions_by_gameid"
    print('\x1b[0;33;44m' + "def----->" + '\x1b[0m', stackpath )

    db_extracted_questions = questions_db.get_questions_by_gameid(gameId)

    print('\x1b[0;33;44m' + "<-----def" + '\x1b[0m', stackpath)
    return db_extracted_questions


@router.get("/get_edit_game_by_id")
async def get_edit_game_by_id(gameId: int):
    stackpath = "get_edit_game_by_id"
    print('\x1b[0;30;44m' + "get------>" + '\x1b[0m', stackpath )

    db_extracted_game = games_db.get_game_by_id(gameId)
    db_extracted_questions = get_questions_by_gameid(gameId)
    
    print('\x1b[0;30;44m' + "<------get" + '\x1b[0m', stackpath)
    return {"extracted_game": db_extracted_game, "extracted_questions" : db_extracted_questions}


@router.post("/post_edit_game_by_id")
async def post_edit_game_by_id(game: Game, questions: List[Question]):
    stackpath = "post_edit_game_by_id"
    print('\x1b[0;30;44m' + "post------>" + '\x1b[0m', stackpath )
    
    game.questions_number = len(questions)

    db_game = games_db(game)
    new_game_id = db_game.createGame_returnId()
    
    db_questions = questions_db(questions)
    db_questions.create_questions(new_game_id)


    print('\x1b[0;30;44m' + "<------post" + '\x1b[0m', stackpath)
    return {"game": game, "question": questions}

