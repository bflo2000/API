import { screens, requests } from '../actions/actions.jsx'
import { combineReducers } from 'redux'

// state for basic nav
const screenDisplay = (state = screens.SCREEN1, action) => {
  switch (action.type) {
    case 'CHANGE_SCREEN':
      return action.screen
    default:
      return state
  }
}

//API request state here
let initialRequestState = {
  request: requests.POST,
  file: null,
  status: 'Ready',
  table: '',
  feedback: 'Server feedback here.'
}

const apiRequest = (state = initialRequestState, action) => {
  switch (action.type) {
    case 'CHANGE_REQUEST':
      return {...state, request:action.request}
    case 'UPDATE_FILE':
      return {...state, file:action.file}
    case 'SELECT_TABLE':
      return {...state, table:action.table}
    case 'IS_UPDATING':
      return {...state, status:'locked'}
    case 'UPDATE_FEEDBACK':
      return {...state, feedback: action.feedback}
    default:
      return state
  }
}

const MainApp = combineReducers({
	screenDisplay,
	apiRequest
})

export default MainApp