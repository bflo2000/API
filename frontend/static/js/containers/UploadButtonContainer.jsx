import { connect } from 'react-redux'
import { uploadCSV } from '../actions/actions.jsx'
import React from 'react'

const UploadButtonContainer = ({ onClick, file, children }) => {
	if(file){
		return(
		<div id='upload_area'>
			<button onClick={() => onClick()}>
				UPLOAD
			</button>
		</div>
		)
	}
	else{
		return(<div id='upload_area'></div>)
	}
}

const mapStateToProps = state => ({
	file : state.apiRequest.file
})

const mapDispatchToProps = dispatch => ({
  onClick: () => {
  	dispatch(uploadCSV())
  }
})

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(UploadButtonContainer)