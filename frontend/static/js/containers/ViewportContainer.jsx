import { connect } from 'react-redux'
import Viewport from './../components/Viewport.jsx'

const mapStateToProps = state => {
	return {currentScreen : state.screenDisplay}
}
const ViewportContainer = connect(
  mapStateToProps,
  null
)(Viewport)

export default ViewportContainer