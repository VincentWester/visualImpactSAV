import React, { Component } from "react";
import PropTypes from "prop-types";
import axios from 'axios'

export default class DataProvider extends Component {
    constructor(props){
        super(props);
        this.state = {
            data: [],
            loaded: false,
            placeholder: "Loading..."
		}
    }

    componentDidMount() {
        axios.get(this.props.endpoint)
            .then(
                function(response){
                    if (response.status !== 200) {
                        return this.setState({ placeholder: "Something went wrong" });
                    }
                    else {
                        return this.setState({ data: response.data, loaded: true })
                    }

                }.bind(this)
            )
    }

    render() {
        const { data, loaded, placeholder } = this.state;
        console.log(this.state)
        return loaded ? this.props.render(data) : <p>{placeholder}</p>;
    }
}