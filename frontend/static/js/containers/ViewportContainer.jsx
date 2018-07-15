import { connect } from 'react-redux'
import Viewport from './../components/Viewport.jsx'

const mapStateToProps = state => {
	return {currentScreen : state.screenDisplay}
}

/*
const mapDispatchToProps = (dispatch, ownProps) => ({
  onClick: () => dispatch(changeScreen(ownProps.screen))
})*/

const ViewportContainer = connect(
  mapStateToProps,
  null
)(Viewport)

export default ViewportContainer