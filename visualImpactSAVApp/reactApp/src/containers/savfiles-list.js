import React, { Component } from 'react'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import { listSAVFiles } from '../actions/index'

class SAVFilesList extends Component {
    renderFiles(){
        const files = this.props.files
        if (files){
            return files.map(
                (file) => {
                    return (
                        <p>VIF-SAV-{file.id} + {file.name_customer} + {file.registred_by}</p>
                    )
                }
            )
        }
    }

    componentDidMount(){
        this.props.listSAVFiles()
    }

    render() {
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
        files: state.savFiles
    }
}
 
const mapDispatchToProps = (dispatch) => {
    return bindActionCreators({listSAVFiles}, dispatch)
}

export default connect(mapStateToProps, mapDispatchToProps)(SAVFilesList)