import { combineReducers } from 'redux';
import SAVFilesListReducer from './SAVFiles/savfiles-list'

const rootReducer = combineReducers(
  {
    savFiles: SAVFilesListReducer
  }
);

export default rootReducer;