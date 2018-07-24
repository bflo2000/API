import React from 'react'
import ReactDOM  from 'react-dom'
import App from './App.jsx';
import { Provider } from 'react-redux'
import { createStore, applyMiddleware } from 'redux'
import thunk from 'redux-thunk'
import MainApp from './reducers/MainApp.jsx'
import './styles.less'
import './react-select.css'

const store = createStore(MainApp, applyMiddleware(thunk))

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
	document.getElementById('react')
);