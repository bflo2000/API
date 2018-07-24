import { connect } from 'react-redux'
import { tableSelect } from '../actions/actions.jsx'
import React from 'react'
import Select from 'react-select'

// textarea for server feedback. Can be very long. But that's what we want.

// will use backend validation as windows has a borked interpretation of the csv mimetype
const ServerFeedbackContainer = (props) => (
  <textarea id= "feedback_area" readOnly={true} value={props.feedback}/>
)

const mapStateToProps = state => {
	return {feedback :  state.apiRequest.feedback}
}

const mapDispatchToProps = (dispatch) => ({
  onChange: (table) => {
  	dispatch(tableSelect(table))  
  }
})

export default connect(
  mapStateToProps,
  null
)(ServerFeedbackContainer)