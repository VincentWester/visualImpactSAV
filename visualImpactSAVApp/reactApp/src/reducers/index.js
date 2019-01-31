import { combineReducers } from 'redux';
import SAVFilesListReducer from './SAVFiles/savfiles-list'
import LoginReducer from './User/login'
import { reducer as reducerForm } from 'redux-form'

const rootReducer = combineReducers(
  {
    savFiles: SAVFilesListReducer,
    login: LoginReducer,
    form: reducerForm
  }
);

export default rootReducer;