import React from 'react'
import {Switch, Route, Redirect} from 'react-router-dom'
import {LinksPage} from './pages/LinksPage'
import {CreatePage} from './pages/CreatePage'
import {DetailPage} from './pages/DetailPage'
import {AuthPage} from './pages/AuthPage'
import {HomePage} from './pages/HomePage'

export const useRoutes = (isAuthenticated, userType) => {
    const public_routes = [
        {
            path: '/home',
            component: HomePage
        },
        {
            path: '/links',
            component: LinksPage,
        }
    ]

    const admin_routes = [
            {
                path: '/create',
                component: CreatePage
            },
            {
                path: '/detail/:id',
                component: DetailPage,
            }
        ].concat(public_routes)

    if (!!userType) {
        return (
            <Switch>
                {admin_routes.map((route) => (
                <Route
                    key={route.path}
                    path={route.path}
                    component={route.component}
                />
                    ))}   
                
                <Redirect to="/home" />
            </Switch>
        )
    }

    if (isAuthenticated) {
        return (
            <Switch>
                {public_routes.map((route) => (
                    <Route
                        key={route.path}
                        path={route.path}
                        component={route.component}
                    />
                ))}

                <Redirect to="/home" />
            </Switch>
        )
    }

    return (
        <Switch>
            <Route path="/" exact>
                <AuthPage />   
            </Route>
            <Redirect to="/" />
        </Switch>
    )
}