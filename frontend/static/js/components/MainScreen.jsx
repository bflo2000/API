require('../styles.less')
import React from 'react'
import NavbarContainer from '../containers/NavbarContainer.jsx'
import ViewPortContainer from '../containers/ViewPortContainer.jsx'

const MainScreen = () => (
	 <div id='api_mainscreen'>
	 	<NavbarContainer />
	 	<ViewPortContainer/>
	 </div>
)

export default MainScreen