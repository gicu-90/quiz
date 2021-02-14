import {useState, useCallback, useEffect} from 'react'

const storageName = "userData"

export const useAuth = () => {
    const [token, setToken] = useState(null)
    const [userType, setUserType] = useState(null)
    
    const login = useCallback( (jwtToken, user_type) => {
        setToken(jwtToken)
        setUserType(user_type)

        localStorage.setItem(storageName, JSON.stringify({
            userType:user_type, token:jwtToken
        }))
    }, [])
    
    const logout = useCallback( () => {
        setToken(null)
        setUserType(null)
        localStorage.removeItem(storageName)
    }, [])

    useEffect(() => {
        const data = JSON.parse(localStorage.getItem(storageName))

        if (data && data.token) {
            login(data.token, data.userType)
        }
    }, [login])
    return { login, logout, token, userType }
}