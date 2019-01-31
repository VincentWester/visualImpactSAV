import axios from 'axios'
import { ACTIONS_SAVFILES } from '../action-types'

export function listSAVFiles(){
    return function(dispatch){
        axios.get(
            `/visualImpactSAV/api/dossiers_sav/`
        ).then(
            (response) => {
                dispatch({
                    type: ACTIONS_SAVFILES.LIST,
                    payload: response.data
                })
            }
        )
    }
}