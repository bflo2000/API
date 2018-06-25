import React from 'react'
import ReactDOM  from 'react-dom'
import App from './App.jsx';
import { Provider } from 'react-redux'
import { createStore } from 'redux'
import screenDisplay from './reducers/MainApp.jsx'

const store = createStore(screenDisplay)

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
	document.getElementById('react')
);