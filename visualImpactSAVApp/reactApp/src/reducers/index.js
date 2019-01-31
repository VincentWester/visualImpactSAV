import { combineReducers } from 'redux';
import { reducer as reducerForm } from 'redux-form'

import SAVFilesListReducer from './SAVFiles/savfiles-list'
import LoginReducer from './User/login'

const rootReducer = combineReducers(
    {
        savFiles: SAVFilesListReducer,
        login: LoginReducer,
        form: reducerForm
    }
);

export default rootReducer;