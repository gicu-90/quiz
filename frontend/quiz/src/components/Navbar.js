import React, { useContext } from 'react'
import {NavLink, useHistory} from 'react-router-dom'
import { AuthContext } from '../context/AuthContext'

export const Navbar = () => {
    const history = useHistory()
    const auth = useContext(AuthContext)
    const logoutHandler = event => {
        event.preventDefault()
        auth.logout()
        history.push('/')
    }
    return (
        <nav>
            <div className="nav-wrapper blue darken-1" style={{ padding: '0 2rem' }}>
                <a href="/" className="brand-logo">QUIZ</a>
                <ul id="nav-mobile" className="right">
                    { !!auth.userType && <li><NavLink to="/create">Create Game</NavLink></li>}
                    <li><NavLink to="/links">Games</NavLink></li>
                    <li><a href="/" onClick={logoutHandler}>Logout</a></li>
                </ul>
            </div>
        </nav>
    )
}