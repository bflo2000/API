const initialState = {}
import { Screens } from '../actions/actions.jsx'

/*
function MainApp(state = initialState, action) {
  return state
}*/

const screenDisplay = (state = Screens.SCREEN1, action) => {
  switch (action.type) {
    case 'CHANGE_SCREEN':
      return action.screen
    default:
      return state
  }
}

export default screenDisplay

