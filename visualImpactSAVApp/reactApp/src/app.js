import React, { Component } from 'react';
import { Route, Switch, BrowserRouter as Router, Redirect } from 'react-router-dom';
import { connect } from "react-redux";

import { login } from "./actions";
import generalTemplate from "./general-template";

import SAVFilesList from './containers/savfiles-list'
import Login from './containers/login'
import Register from './containers/register'
import NotFound from "./components/not-found";

class RootContainerComponent extends Component {

    componentDidMount() {
        this.props.loadUser();
    }

    PrivateRoute = ({component: ChildComponent, ...rest}) => {
        return <Route {...rest} render={props => {
            if (this.props.login.isLoading) {
                return <em>Loading...</em>;
            } else if (!this.props.login.isAuthenticated) {
                return <Redirect to="/login" />;
            } else {
                return <ChildComponent {...props} />
            }
        }} />
    }

    render() {
        let { PrivateRoute } = this;
        return (
            <Router>
                <Switch>
                    <PrivateRoute exact path="/" component={SAVFilesList} />
                    <Route exact path="/register" component={Register} />
                    <Route exact path="/login" component={Login} />
                    <Route component={NotFound} />
                </Switch>
            </Router>
        );
    }
}

const mapStateToProps = state => {
    return {
        login: state.login,
    }
}

const mapDispatchToProps = dispatch => {
    return {
        loadUser: () => {
            return dispatch(login.loadUser());
        }
    }
}

let RootContainer = connect(mapStateToProps, mapDispatchToProps)(generalTemplate(RootContainerComponent));

export default class App extends Component {
    render() {
        return (
            <RootContainer />
        )
    }
}