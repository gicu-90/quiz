import React, { useState } from 'react'
import { useHttp } from '../hooks/http.hook'

export const AuthPage = () => {
    const {loading, request} = useHttp()
    const [form, setForm] = useState({
        username: '', password: ''
    })

    const changeHandler = event => {
        setForm({ ...form, [event.target.name]: event.target.value })
    }

    const registerHandler = async () => {
        try {
            let jsonFormData = JSON.stringify(form)
            const data = await request('/create-user', "POST", jsonFormData, {"Content-Type":"application/json"})
            console.log('Data', data)
        } catch (e) {}
    }

    return (
        <div className="row">
                <div className="col s6 offset-s3">
                    <h1>Login / Auth</h1>
                <div className="card blue darken-1">
                    <div className="card-content white-text">
                        <span className="card-title">Authorization</span>
                        <div>
                            <div className="input-field">
                                <input 
                                    placeholder="Enter username" 
                                    id="username" 
                                    type="text" 
                                    name="username"
                                    className="yellow-input" 
                                    onChange={changeHandler}
                                />
                                <label htmlFor="username">First Name</label>
                            </div>
                            <div className="input-field">
                                <input 
                                    placeholder="Enter password" 
                                    id="password" 
                                    type="password" 
                                    name="password"
                                    className="yellow-input" 
                                    onChange={changeHandler}
                                />
                                <label htmlFor="password">First Name</label>
                            </div>
                        </div>
                    </div>
                    <div className="card-action">

                        <button 
                            className="btn yellow darken-4" 
                            style={{marginRight: 10}}
                            disabled={loading}
                        >
                            Login
                        </button>
                        
                        <button 
                            className="btn grey lighten-1 black-text" 
                            onClick={registerHandler}
                            disabled={loading}
                        >
                            Register
                        </button>

                    </div>
                </div>   
                </div>    
        </div>
    )
}