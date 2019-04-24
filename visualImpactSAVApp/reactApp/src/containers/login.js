import { Link } from "react-router-dom";
import React, { Component } from 'react'
import { Redirect } from 'react-router-dom';
import { connect } from 'react-redux'
import { Field, reduxForm } from 'redux-form'

import { login } from '../actions'


const formConfig = {
    form : 'loginForm'
}

class Login extends Component {

    login(values){
        this.props.login(values);
    }

    renderErrors(){
        const { loginState } = this.props
        if (loginState.errors){
            return(
                <p>{loginState.errors.message}</p>
            )
        }
    }

    render() {
        const {handleSubmit, loginState} = this.props

        if (loginState.isAuthenticated) {
            return <Redirect to="/" />
        }
        return (
            <form onSubmit={handleSubmit(this.login.bind(this))}>
                <div>
                    <label>Identifiant</label>
                    <Field name="username" component="input" type="text"/>
                </div>
                <div>
                    <label>Mot de passe</label>
                    <Field name="password" component="input" type="password"/>
                </div>
                <button type="submit">Login</button>

                <p>
                    Don't have an account? <Link to="/register">Register</Link>
                </p>
                {
                    this.renderErrors()
                }
        </form>
        )
    }
}

const mapStateToProps = state => {
    return {
        loginState: state.login
    };
}

const mapDispatchToProps = dispatch => {
    return {    
        login: (values) => {
            return dispatch(login.login(values));
        }        
    };
}

export default connect(mapStateToProps, mapDispatchToProps)(reduxForm(formConfig)(Login));