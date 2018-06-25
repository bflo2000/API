require('../styles.less')
import React from 'react'
import { ButtonToolbar } from 'react-bootstrap';
import ToggleContainer from '../containers/ToggleContainer.jsx'

const Operations = (currentScreen) => {
	return (
		<div id='operations'>
			<div id='request_buttons'>
				<ButtonToolbar>
					<ToggleContainer/>
				</ButtonToolbar>;
			</div>
		</div>
	)
}

export default Operations