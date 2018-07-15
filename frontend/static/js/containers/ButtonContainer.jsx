import { connect } from 'react-redux'
import { Button } from 'react-bootstrap';
import React from 'react'

const ButtonContainer = ({ bsStyle, id, children }) => (
  <Button
    bsStyle= {bsStyle} id={id}> {children} </Button>
)

const mapStateToProps = (state, ownProps) => ({
    bsStyle: ownProps.bsStyle,
    id:ownProps.id
})

const mapDispatchToProps = (dispatch, ownProps) => ({
  onClick: () => dispatch(changeScreen(ownProps.screen))
})

export default connect(
  mapStateToProps,
  null
)(ButtonContainer)

