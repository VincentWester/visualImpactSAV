import React, { Component } from "react";
import { Router, Route, browserHistory, IndexRoute } from 'react-router'

import SAVFilesList from './components/savfiles-list'
import Login from './containers/login'

export default class App extends Component {
    render() { 
        return (
            <div>
               <Router history={browserHistory}>                    
                   <Route path='/app/' component={Login}></Route>
                   <Route path='/app/dossiers-sav' component={SAVFilesList}></Route>        
                   <Route path='*' component={Login}></Route>
               </Router>
            </div>
        )

    }
}
/*<DataProvider endpoint="/visualImpactSAV/api/dossiers_sav/" 
                render={data => <Table data={data} />} />*/