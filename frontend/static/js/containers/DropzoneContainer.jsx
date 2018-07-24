import { connect } from 'react-redux'
import { updateFile } from '../actions/actions.jsx'
import React from 'react'
import Dropzone from 'react-dropzone';

//will use backend validation as windows has a borked interpretation of the csv mimetype
const DropzoneContainer = ({ onDrop }) => (
		<Dropzone className='dropzone' onDrop={onDrop}>
			<p id='dropzone_message'>Click or drop CSV here.</p>
		</Dropzone>
	)

const mapDispatchToProps = (dispatch) => ({
  onDrop: (file) => {
  	dispatch(updateFile(file))
  }
})

export default connect(
  null,
  mapDispatchToProps
)(DropzoneContainer)