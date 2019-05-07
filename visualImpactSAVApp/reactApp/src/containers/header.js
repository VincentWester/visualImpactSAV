import React, { Component } from 'react'
import { connect } from 'react-redux'
import withStyles from 'react-jss'

import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';

import { login } from '../actions'

import Logo from '../../static/images/logoVisual.png'
import { Grid } from '@material-ui/core';

const styles = {
    header: {
        backgroundColor: '#e2eae9',
    },
    mainBody: {
        backgroundColor: '#a9aaff'
    },
    logoPart: {
      alignContent: "flex-start"  
    },
    logoutPart: {
      alignContent: "flex-end"
    }
}

@withStyles(styles)
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
        const { login, classes } = this.props
        return (
          <AppBar position="static" className={classes.header}>
            <Toolbar>
                <Grid item xs={11}>
                    <IconButton aria-label="Logo" className={classes.logoPart}>
                        <img src={ Logo } />
                    </IconButton>
                </Grid> 
                <Grid item xs={1}>
                    <Typography variant="h6" color="black" className={classes.logoutPart}>
                        { this.displayCurrentUserAndLogoutButton(login.user) }
                    </Typography>
                </Grid>
            </Toolbar>
            </AppBar>
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