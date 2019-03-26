import React, { Component, PropTypes } from "react"

const generalTemplate = (ComponentToWrap) => {
  class ThemeComponent extends Component {
    render() {
      return (
        <div>
            <p>Header</p>
            <ComponentToWrap {...this.props} />
            <p>Footer</p>
        </div>
      )
    }
  }

  // on retourne notre wrapper
  return ThemeComponent
}
export default generalTemplate