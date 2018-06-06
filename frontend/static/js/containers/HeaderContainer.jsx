import { connect } from 'react-redux'
import { helloWorld, reset } from './../actions'
import Header from './../components/Header'

const mapStateToProps = (state, ownProps) => {
  return {
    message: state.helloWorld.message
  }
}

const mapDispatchToProps = (dispatch, ownProps) => {
  return {
    onClick: () => dispatch(helloWorld()),
    reset: () => dispatch(reset())
  }
}

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Header)