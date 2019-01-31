import axios from 'axios'
import { ACTIONS_LOGIN, ACTIONS_USER } from '../action-types'

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
            response => {
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