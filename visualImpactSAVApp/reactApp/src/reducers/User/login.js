import { ACTIONS_LOGIN, ACTIONS_USER, ACTIONS_LOGOUT } from '../../actions/action-types'

const initialState = {
    token: localStorage.getItem("token"),
    isAuthenticated: false,
    isLoading: true,
    user: null,
    errors: {},
};

export default function LoginReducer(state=initialState, action) {  
    switch (action.type) {
        case ACTIONS_USER.LOADING:
            return {
                ...state, 
                isLoading: true
            };
        case ACTIONS_USER.ERROR:
            return {
                ...state, 
                isAuthenticated: false, 
                isLoading: false,
            };
        case ACTIONS_USER.LOADED:
            return {
                ...state, 
                isAuthenticated: true, 
                isLoading: false,
                user: action.user
            };

        case ACTIONS_LOGIN.SUCCESS:
            localStorage.setItem("token", action.data.token);
            return {
                ...state, 
                ...action.data, 
                isAuthenticated: true, 
                isLoading: false,
                errors: {}
            };
        case ACTIONS_LOGIN.FAILED:
            return {
                ...state, 
                token: null, 
                user: null,
                isAuthenticated: false, 
                isLoading: false,
                errors: { 
                    status: action.status, 
                    message: "Votre Id ou votre mot de passe est incorect"
                }
            };
        case ACTIONS_LOGOUT.SUCCESS:
            localStorage.removeItem("token");
            return {
                ...state, 
                token: null, 
                user: null,
                isAuthenticated: false, 
                isLoading: false,
                errors: action.data
            };

        default:
            return state;
    }
}