import { connect } from 'react-redux'
import { ToggleButton, ToggleButtonGroup } from 'react-bootstrap';
import { changeRequest } from '../actions/actions.jsx'
import React from 'react'

const ToggleContainer = ({ onChange, children }) => (
	<ToggleButtonGroup type="radio" name='options' onChange= {(e) => onChange(e)} defaultValue={'POST'}>
	  	<ToggleButton value={'POST'}> INSERT </ToggleButton>
	  	<ToggleButton value={'PUT'}> UPDATE </ToggleButton>
	  	<ToggleButton value={'DELETE'}> DELETE </ToggleButton>
	</ToggleButtonGroup>
)

const mapStateToProps = (state, ownProps) => ({
    bsStyle: ownProps.bsStyle,
    value:ownProps.value
})

const mapDispatchToProps = (dispatch) => ({
  onChange: (value) => dispatch(changeRequest(value))
})

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(ToggleContainer)
