import { ACTIONS_SAVFILES } from '../../actions/action-types'

export default function SAVFilesListReducer(state=[], action){
    switch(action.type){
        case ACTIONS_SAVFILES.LIST:
            return action.payload
        default:
            return state
    }
}