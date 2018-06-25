import { connect } from 'react-redux'
import { changeScreen } from '../actions/actions.jsx'
import Link from './../components/Link.jsx'

/*
const mapStateToProps = (state, ownProps) => ({
  active: ownProps.screen === state.visibilityFilter
})*/

const mapDispatchToProps = (dispatch, ownProps) => ({
  onClick: () => dispatch(changeScreen(ownProps.screen))
})

const LinkContainer = connect(
  null,
  mapDispatchToProps
)(Link)

export default LinkContainer