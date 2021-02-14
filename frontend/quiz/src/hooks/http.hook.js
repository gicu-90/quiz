import {useState, useCallback} from 'react'

export const useHttp = () => {
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)

    const request = useCallback( async (url, method = 'GET', body = null, headers = {}, isOAuth = false) => {
        setLoading(true)

        try {

            if (isOAuth) {
                console.log("isoauth",isOAuth)
                let formdata = new FormData()
                for( let prop in body ){
                    formdata.append(prop, body[prop])
                }
                body = formdata
            }

            if (body && !isOAuth) {
                console.log("not isoauth")
                body = JSON.stringify(body)
                headers["Content-Type"] = "application/json"
            }

            const response = await fetch(url, {method, body, headers})
            console.log(response)
            const data = await response.json()

            if (!response.ok) {
                throw new Error(data.detail || 'Something went wrong')
            }
            setLoading(false)
            return data
        } catch (e) {
            setLoading(false)
            setError(e.message)
            throw e
        }
    }, [])

    const clearError = useCallback(() => setError(null), [])

    return { loading, request, error, clearError }
}