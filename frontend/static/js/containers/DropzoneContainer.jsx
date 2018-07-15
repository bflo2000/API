import { connect } from 'react-redux'
import { uploadCSV } from '../actions/actions.jsx'
import React from 'react'
import Dropzone from 'react-dropzone';


//will use backend validation as windows has a borked interpretation of the csv mimetype
const DropzoneContainer = ({ onDrop, children }) => (
		<Dropzone className='dropzone' onDrop={onDrop}>
			<p id='dropzone_message'>Click or drop CSV here.</p>
		</Dropzone>)

const mapStateToProps = (state, ownProps) => ({

})

const mapDispatchToProps = (dispatch) => ({
  onDrop: (file) => {
  	dispatch(uploadCSV(file))
  }
})

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(DropzoneContainer)