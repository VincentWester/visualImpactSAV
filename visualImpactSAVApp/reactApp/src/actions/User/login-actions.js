import axios from 'axios'

import { ACTIONS_LOGIN, ACTIONS_USER, ACTIONS_REGISTER, ACTIONS_LOGOUT } from '../action-types'

export const loadUser = () => {
    return (dispatch, getState) => {
        dispatch(
            {
                type: ACTIONS_USER.LOADING
            }
        );
    
        const token = getState().login.token;
    
        let headers = {
            "Content-Type": "application/json",
        };
    
        if (token) {
            headers["Authorization"] = `Token ${token}`;
        }

        return axios.get(
            "/visualImpactSAV/api/auth/user/",
            {
                headers: headers,
            }
        ).then(
            response => {           
                dispatch({
                    type: ACTIONS_USER.LOADED, 
                    user: response.data 
                });
            }
        ).catch(
            error => {    
                const response = error.response
                dispatch({
                    type: ACTIONS_USER.ERROR,
                    status: response.status
                });
            }
        )
    }
}

export const login = (values) => {
    return (dispatch) => {
        const headers = {"Content-Type": "application/json"};

        return axios.post(
            "/visualImpactSAV/api/auth/login/",
            {
                username: values.username, 
                password: values.password,
            },
            {
                headers: headers,
            }
        ).then(
            response => {               
                dispatch({
                    type: ACTIONS_LOGIN.SUCCESS, 
                    data: response.data 
                });
            }
        ).catch(
            error => {
                const response = error.response
                dispatch({
                    type: ACTIONS_LOGIN.FAILED,
                    status: response.status,
                });
            }
        )
    }
}

export const logout = () => {
    return (dispatch, getState) => {
    
        const token = getState().login.token;
    
        let headers = {
            "Content-Type": "application/json",
        };
    
        if (token) {
            headers["Authorization"] = `Token ${token}`;
        }
    
        return axios.post(
            "/visualImpactSAV/api/auth/logout/",
            {},
            {
                headers: headers,
            }
        ).then(
            (response) => {                   
                dispatch({
                    type: ACTIONS_LOGOUT.SUCCESS,
                    data: response.data
                });
            }
        ).catch(            
            error => {
                const response = error.response
                if (response.status == 401 || response.status == 403){
                    dispatch({
                        type: ACTIONS_LOGIN.FAILED,
                        status: response.status,
                    });
                }
                else{
                    dispatch({
                        type: ACTIONS_USER.ERROR,
                        status: response.status,
                    });                   
                }
            }
        )
    }
  }


export const register = (values) => {
    return (dispatch) => {
        const headers = {"Content-Type": "application/json"};

        return axios.post(
            "/visualImpactSAV/api/auth/register/",
            {
                username: values.username, 
                password: values.password,
            },
            {
                headers: headers,
            }
        ).then(
            response => {              
                dispatch({
                    type: ACTIONS_REGISTER.SUCCESS, 
                    data: response.data 
                });
            }
        ).catch(
            error => {
                const response = error.response
                if (response.status == 401 || response.status == 403){
                    dispatch({
                        type: ACTIONS_REGISTER.FAILED,
                        status: response.status,
                    });
                }
                else{
                    dispatch({
                        type: ACTIONS_USER.ERROR,
                        status: response.status,
                    });                   
                }
            }
        )
    }
}
