import React from 'react'
import ReactDOM from 'react-dom'
import App from './App';
import { Provider } from 'react-redux'
import { createStore } from 'redux'
import helloReducer from './reducers'

function Welcome(props) {
  return <h1>Hello, {props.name}</h1>;
}

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
	document.getElementById('react')
);