import React from 'react'

export const CreatePage = () => {
    return (
        <div className="row">
            <div className="col s6 offset-s3">
                <h1>Create new Game</h1>
                <div className="card blue darken-1">
                    <form action="...">
                        <div className="card-content white-text">

                            <div>
                                <div className="input-field">
                                    <span className="card-title">Game name</span>
                                    <input
                                        placeholder="Enter game name"
                                        id="username"
                                        type="text"
                                        name="username"
                                    />
                                </div>

                                <div className="question-container blue darken-2">
                                    <div className="input-field">
                                        <span className="card-title">Question</span>
                                        <input
                                            placeholder="Enter question"
                                            id="question"
                                            type="text"
                                            name="question"
                                        />
                                    </div>
                                    <div className="input-field">
                                        <span className="card-title">Correct answer</span>
                                        <input
                                            placeholder="Enter correct answer"
                                            id="answer"
                                            type="text"
                                            name="answer"
                                        />
                                    </div>
                                    <div className="input-field">
                                        <span className="card-title">Other variant</span>
                                        <input
                                            placeholder="Enter other variant"
                                            id="variant"
                                            type="text"
                                            name="variant"
                                        />
                                    </div>
                                </div>

                            </div>
                        </div>


                        <div className="card-action">

                            <button
                                className="btn yellow darken-4"
                                style={{ marginRight: 10 }}
                            >
                                Login
                        </button>

                            <button
                                className="btn grey lighten-1 black-text"
                            >
                                Register
                        </button>

                        </div>
                    </form>
                </div>
            </div>
        </div>
    )
}