require('../styles.less')
import React from 'react'
import { ButtonToolbar } from 'react-bootstrap';
import ToggleContainer from '../containers/ToggleContainer.jsx'
import DropzoneContainer from '../containers/DropzoneContainer.jsx'

const Operations = (currentScreen) => {
	return (
		<div id='operations'>
			<div id='request_buttons'>
				<ButtonToolbar>
					<ToggleContainer/>
				</ButtonToolbar>
			</div>
			<div id='dropzone_container'>
				<DropzoneContainer/>
			</div>
		</div>
	)
}

export default Operations