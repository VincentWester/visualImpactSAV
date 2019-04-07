import React, { Component, PropTypes } from "react"
import Header from './containers/header'

const generalTemplate = (ComponentToWrap) => {
  class ThemeComponent extends Component {
    render() {
      return (
        <div>
            <Header/>
            <ComponentToWrap {...this.props} />
            <p>Footer</p>
        </div>
      )
    }
  }

  return ThemeComponent
}
export default generalTemplate