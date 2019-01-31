import {Link} from "react-router-dom";
import React, { Component } from 'react'
import ReactDOM from 'react-dom';
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import { Field, reduxForm } from 'redux-form'

import { login } from '../actions'



const formConfig = {
    form : 'loginForm'
}

class Login extends Component {

  login(values){
    this.props.login(values);
  }

  render() {
    const {handleSubmit} = this.props
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
      </form>
    )
  }
}

const mapStateToProps = state => {
    return {
        login: state.login
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