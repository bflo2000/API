import React from 'react'
import ReactDOM  from 'react-dom'
import App from './App.jsx';
import { Provider } from 'react-redux'
import { createStore, applyMiddleware } from 'redux'
import MainApp from './reducers/MainApp.jsx'
import img1 from './hypnotize1.jpg'
import thunk from 'redux-thunk'

const store = createStore(MainApp, applyMiddleware(thunk))

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
	document.getElementById('react')
);