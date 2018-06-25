import { connect } from 'react-redux'
import { ToggleButton, ToggleButtonGroup } from 'react-bootstrap';
import React from 'react'

const ToggleContainer = ({ bsStyle, value, children }) => (
	<ToggleButtonGroup type="radio" name='options' defaultValue={1}>
	  	<ToggleButton value={1}> INSERT </ToggleButton>
	  	<ToggleButton value={2}> UPDATE </ToggleButton>
	  	<ToggleButton value={3}> DELETE </ToggleButton>
	</ToggleButtonGroup>
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
)(ToggleContainer)
