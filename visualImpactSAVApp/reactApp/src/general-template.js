import React, { Component } from "react"
import withStyles from 'react-jss'

import Grid from '@material-ui/core/Grid'

import Header from './containers/header'

const styles = {
  mainBody: {
      backgroundColor: '#a9aaff'
  }
}


const generalTemplate = (ComponentToWrap) => {

  @withStyles(styles)
  class ThemeComponent extends Component {

    render() {
      const { classes } = this.props
      return (
        <Grid 
          container
          direction="column"
          justify="space-between"
          alignItems="center"
        >
          <Header/>
          <Grid 
              item
              className={ classes.mainBody }
            >
            <ComponentToWrap {...this.props} />
          </Grid>            
        </Grid>
      )
    }
  }

  return ThemeComponent
}
export default generalTemplate