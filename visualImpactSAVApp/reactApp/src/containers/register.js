import { Link } from "react-router-dom";
import React, { Component } from 'react'
import { Redirect } from 'react-router-dom';
import { connect } from 'react-redux'
import { Field, reduxForm } from 'redux-form'

import { login } from '../actions'


const formConfig = {
    form : 'registerForm'
}

class Register extends Component {

    register(values){
        this.props.register(values);
    }

    renderErrors(){
        const { registerState } = this.props
        if (registerState.errors){
            return(
                <p>{registerState.errors.message}</p>
            )
        }
    }

    render() {
        const { handleSubmit, registerState } = this.props
        if (registerState.isAuthenticated) {
            return <Redirect to="/" />
        }
        else {
            return (
                <form onSubmit={handleSubmit(this.register.bind(this))}>
                    <div>
                        <label>Identifiant</label>
                        <Field name="username" component="input" type="text"/>
                    </div>
                    <div>
                        <label>Mot de passe</label>
                        <Field name="password" component="input" type="password"/>
                    </div>
                    <button type="submit">Register</button>
                    {
                        this.renderErrors()
                    }
            </form>
            )
        }
    }
}

const mapStateToProps = state => {
    return {
        registerState: state.login
    };
}

const mapDispatchToProps = dispatch => {
    return {    
        register: (values) => {
            return dispatch(login.register(values));
        }        
    };
}

export default connect(mapStateToProps, mapDispatchToProps)(reduxForm(formConfig)(Register));