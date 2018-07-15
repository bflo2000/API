const initialState = {}
import { screens, requests } from '../actions/actions.jsx'
import { combineReducers } from 'redux'

const screenDisplay = (state = screens.SCREEN1, action) => {
  switch (action.type) {
    case 'CHANGE_SCREEN':
      return action.screen
    default:
      return state
  }
}

const apiRequest = (state = {request:requests.POST, file: "", status: 'Ready'}, action) => {
  switch (action.type) {
    case 'CHANGE_REQUEST':
      return {...state, request:action.request}
    case 'UPDATE_FILE':
      return {...state, file:action.file}
    case 'IS_UPDATING':
      return {...state, status:action.status}
    default:
      return state
  }
}

const MainApp = combineReducers({
	screenDisplay,
	apiRequest
})

export default MainApp