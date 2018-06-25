import { connect } from 'react-redux'
import { ToggleButton } from 'react-bootstrap';
import React from 'react'

const ButtonContainer = ({ bsStyle, value, children }) => (
  <ToggleButton value={value}> {children} </ToggleButton>
)

const mapStateToProps = (state, ownProps) => ({
    bsStyle: ownProps.bsStyle,
    value:ownProps.value
})

const mapDispatchToProps = (dispatch, ownProps) => ({
  onClick: () => dispatch(changeScreen(ownProps.screen))
})

export default connect(
  mapStateToProps,
  null
)(ButtonContainer)

