import React, { useContext, useEffect, useState } from 'react'
import { AuthContext } from '../context/AuthContext'
import { useHttp } from '../hooks/http.hook'

export const CreatePage = () => {
    const auth = useContext(AuthContext)
    const { loading, request, error, clearError } = useHttp()


    const addquestion = async () => {

        var question_container = document.querySelectorAll(".question-container")
        var cloned = question_container[question_container.length - 1].cloneNode(true)

        var cloned_inputs = cloned.querySelectorAll("input")
        cloned_inputs.forEach(element => {
            element.id = element.getAttribute("data-use") + "_" + question_container.length
            element.name = element.getAttribute("data-use") + "_" + question_container.length
            element.value = ""
        })


        var cloned_question = cloned.querySelector(".question-input") 
        var icon = cloned_question.querySelector(".material-icons") 
        icon.innerText = "close"


        function insertAfter(newNode, referenceNode) {
            referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
        }

        insertAfter(cloned, question_container[question_container.length - 1])
    }

    const addanswer =  event => {
        //setForm({ ...form, [event.target.name]: event.target.value })
    }

    const createHandler = async () => {

        function Question(
            question_type,
            question,
            correct_resp,
            other_variants,
            winning_points) {

            this.question_type = question_type;
            this.question = question;
            this.correct_resp = correct_resp;
            this.other_variants = other_variants;
            this.winning_points = winning_points;
        }

        var Game = {
            game_name: ""
        }

        var questions = []
        var game1 = Game

        game1.game_name = document.querySelector("#game_name").value

        var question_container = document.querySelectorAll(".question-container")
        question_container.forEach(element => {

            var thisQuestion = new Question(0, "", [], [], 0);

            var inputs = element.querySelectorAll("input")
            inputs.forEach(element => {
                var data_use = element.getAttribute("data-use");

                switch (data_use) {
                    case "correct_resp":
                        thisQuestion[data_use].push(element.value)
                        break;
                    case "other_variants":
                        thisQuestion[data_use].push(element.value)
                        break;
                    default:
                        thisQuestion[data_use] = element.value
                }
            })

            questions.push(thisQuestion)
        })


        try {
            const data = await request('/new_game', "POST", { game: game1, questions: questions }, { Authorization: "Bearer " + auth.token })
            console.log("data", data)
        } catch (e) { }
    }

    return (
        <div className="row">
            <div className="col s6 offset-s3">
                <h1>Create new Game</h1>
                <div className="card blue darken-1">
                    <div className="card-content white-text">

                        <div>
                            <div className="input-field">
                                <span className="card-title">Game name</span>
                                <input
                                    placeholder="Enter game name"
                                    id="game_name"
                                    type="text"
                                    name="game_name"
                                />
                            </div>

                            <div className="question-container card blue darken-2">
                                <div className="input-field question-input">
                                    <div className="input-title">
                                        <h5 className="card-title left-align">Question</h5>
                                        <i 
                                            className="material-icons right-align z-depth-2"
                                            onClick={createHandler}
                                            >
                                            add
                                        </i>
                                    </div>
                                    <input
                                        placeholder="Enter question"
                                        id="question_0"
                                        type="text"
                                        name="question_0"
                                        data-use="question"
                                    />
                                </div>
                                <div className="answers-inputs">
                                    <div className="input-field">
                                        <div className="input-title">
                                            <h5 className="left-align">Correct answer</h5>
                                            <i className="material-icons right-align z-depth-2">add</i>
                                        </div>
                                        <input
                                            placeholder="Enter correct answer"
                                            id="correct_resp_0"
                                            type="text"
                                            name="correct_resp_0"
                                            data-use="correct_resp"
                                        />
                                    </div>
                                    <div className="input-field">
                                        <div className="input-title">
                                            <h5 className="left-align">Other variant</h5>
                                            <i className="material-icons right-align z-depth-2">add</i>
                                        </div>
                                        <input
                                            placeholder="Enter other variant"
                                            id="other_variants_0"
                                            type="text"
                                            name="other_variants_0"
                                            data-use="other_variants"
                                        />
                                    </div>
                                    <div className="input-field">
                                        <span className="card-title">Winning Points</span>
                                        <input
                                            placeholder="Enter winning points"
                                            id="winning_points_0"
                                            type="text"
                                            name="winning_points_0"
                                            data-use="winning_points"
                                        />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <button
                        className="btn blue darken-2"
                        style={{ 
                            marginBottom: 24,
                            marginLeft: 24
                            }}
                        onClick={addquestion}
                    >
                        Add Question
                    </button>
                    <div className="card-action">

                        <button
                            className="btn yellow darken-4"
                            style={{ marginRight: 10 }}
                            onClick={createHandler}
                        >
                            Create
                        </button>

                    </div>
                </div>
            </div>
        </div>
    )
}