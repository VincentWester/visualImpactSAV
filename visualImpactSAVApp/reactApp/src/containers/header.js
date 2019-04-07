import React, { Component } from 'react'
import { connect } from 'react-redux'

import Grid from '@material-ui/core/Grid'

import { login } from '../actions'

import Logo from '../../static/images/logoVisual.png'

class Header extends Component {
    displayCurrentUserAndLogoutButton(user){
        if (user != null){
            return (
                <div>                    
                    { user.username }
                    (<a onClick={this.props.logout}>logout</a>)
                </div>
            )
        }
    }

    render() {
        const { login } = this.props
        return (
            <Grid 
                container
                direction="row"
                justify="space-between"
                alignItems="center"
                className=""
            >
                <Grid 
                    item
                    direction="row"
                    justify="center"
                    alignItems="center"
                    className=""
                >
                    <img src={ Logo } />
                </Grid>
                <Grid 
                    item
                    direction="row"
                    justify="center"
                    alignItems="center"
                    className=""
                >
                    { this.displayCurrentUserAndLogoutButton(login.user) }
                </Grid>
            </Grid>
        )
    }
}

const mapStateToProps = (state) => {
    return {
        login: state.login,
    }
}
 
const mapDispatchToProps = (dispatch) => {
    return {
        logout: () => {
            return dispatch(login.logout())
        }
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(Header)