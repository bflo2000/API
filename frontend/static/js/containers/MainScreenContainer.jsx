import { connect } from 'react-redux'
//import { helloWorld, reset } from './../actions'
import MainScreen from './../components/MainScreen.jsx'

/*
const mapStateToProps = (state, ownProps) => {
  return {
    //message: state.helloWorld.message
  }
}

const mapDispatchToProps = (dispatch, ownProps) => {
  return {
    //onClick: () => dispatch(helloWorld()),
    //reset: () => dispatch(reset())
  }
}*/

const MainScreenContainer = connect(
  //mapStateToProps,
  //mapDispatchToProps
)(MainScreen)

export default MainScreenContainer