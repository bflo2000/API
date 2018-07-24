require('../styles.less')
import React from 'react'
import { ButtonToolbar } from 'react-bootstrap';
import ToggleContainer from '../containers/ToggleContainer.jsx'
import DropzoneContainer from '../containers/DropzoneContainer.jsx'
import UploadButtonContainer from '../containers/UploadButtonContainer.jsx'
import DropdownContainer from '../containers/DropdownContainer.jsx'
import ServerFeedbackContainer from '../containers/ServerFeedbackContainer.jsx'

const Operations = (currentScreen) => {
	return (
		<div id='operations'>
			<div id='request_buttons'>
				<ButtonToolbar>
					<ToggleContainer/>
				</ButtonToolbar>
			</div>
			<div id='dropdown_container'>
				<DropdownContainer/>
			</div>
			<div id='dropzone_container'>
				<DropzoneContainer/>
			</div>
			<div id='upload_button_container'>
				<UploadButtonContainer/>
			</div>
			<div id='server_feedback_container'>
				<ServerFeedbackContainer/>
			</div>
		</div>
	)
}

export default Operations