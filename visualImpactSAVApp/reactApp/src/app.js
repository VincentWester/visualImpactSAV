import React, { Component } from "react";
import { BrowserRouter as Router, Route } from 'react-router-dom'

import SAVFilesList from './components/savfiles-list'
import Login from './containers/login'

export default class App extends Component {
    render() { 
        return (
            <Router>  
                <div>                  
                    <Route path='/app/' component={Login} exact></Route>
                    <Route path='/app/dossiers-sav' component={SAVFilesList}></Route>  
                </div>
            </Router>
        )

    }
}
/*<DataProvider endpoint="/visualImpactSAV/api/dossiers_sav/" 
                render={data => <Table data={data} />} />*/