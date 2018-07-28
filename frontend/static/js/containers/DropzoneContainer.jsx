import { connect } from 'react-redux'
import { updateFile } from '../actions/actions.jsx'
import React from 'react'
import Dropzone from 'react-dropzone';
import { PropagateLoader } from 'react-spinners';

// will use backend validation as windows has a borked interpretation of the csv mimetype
const DropzoneContainer = ({ status, onDrop, file }) => (
		<Dropzone className='dropzone' onDrop={onDrop} disabled = {(status === 'Locked') ? true: false}>
			<div id='dropzone_message'>
			{(status === 'Ready') ?
				<p>Click or drop CSV here.</p>
			: (status === 'Loaded') ?
				file.map(f => <p key={f.name}>{f.name} - {Math.ceil(f.size/1000000)} mb </p>)
			: <PropagateLoader/>}
			</div>
		</Dropzone>
	)

const mapStateToProps = state => {
	return {
		status :  state.apiRequest.status,
		file: state.apiRequest.file
	}
}

const mapDispatchToProps = (dispatch) => ({
  onDrop: (file) => {
  	dispatch(updateFile(file))
  }
})

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(DropzoneContainer)