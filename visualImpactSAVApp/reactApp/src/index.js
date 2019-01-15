import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { createStore, applyMiddleware } from 'redux';

import App from './components/App';

const createStoreWithMiddleware = applyMiddleware()(createStore);

ReactDOM.render(<App />, document.getElementById('app'))
// to put a composant in a class of index.html, write the function `document.querySelector('.app')`