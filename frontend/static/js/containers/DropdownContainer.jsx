import { connect } from 'react-redux'
import { tableSelect } from '../actions/actions.jsx'
import React from 'react'
import Select from 'react-select'

//will use backend validation as windows has a borked interpretation of the csv mimetype
const DropdownContainer = (props) => (
	<Select 
		placeholder = 'Select Table...'
		value = {props.selectedOption}
		onChange = {props.onChange}
		options = {[
          { value: 'Images', label: 'Images' },
          { value: 'Amazon', label: 'Amazon' },
        ]}
    />
)

const mapStateToProps = state => {
	return {selectedOption :  state.apiRequest.table}
}

const mapDispatchToProps = (dispatch) => ({
  onChange: (table) => {
  	dispatch(tableSelect(table))  
  }
})

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(DropdownContainer)