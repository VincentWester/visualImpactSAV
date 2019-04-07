import React, { Component } from 'react'
import { connect } from 'react-redux'

import { savfiles, login } from '../actions'

class SAVFilesList extends Component {
    renderFiles(){
        const files = this.props.files
        if (files){
            return files.map(
                (file) => {
                    return (
                        <p key={file.id}>VIF-SAV-{file.id} + {file.name_customer} + {file.registred_by}</p>
                    )
                }
            )
        }
    }

    componentDidMount(){
        this.props.listSAVFiles()
    }

    render() {
        const { login } = this.props
        return (
            <div>
                <h1>Liste des fichiers</h1>
                {
                    this.renderFiles()
                }
            </div>
        )
    }
}

const mapStateToProps = (state) => {
    return {
        files: state.savFiles,
        login: state.login,
    }
}
 
const mapDispatchToProps = (dispatch) => {
    return {
        listSAVFiles: () => {
            return dispatch(savfiles.listSAVFiles())
        },
        logout: () => {
            return dispatch(login.logout())
        }
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(SAVFilesList)