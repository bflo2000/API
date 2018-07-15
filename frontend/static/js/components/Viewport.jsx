require('../styles.less')
import React from 'react'
import { screens } from '../actions/actions.jsx'
import Operations from './../components/Operations.jsx'

const getScreen = screen => {
	switch (screen){
		case screens.SCREEN1:
			return <div id='viewport'><Operations/></div>
		case screens.SCREEN2:
			return <div id='viewport'>test2</div>
		case screens.SCREEN3:
			return <div id='viewport'>test3</div>
	}	
}

const Viewport = (screen) => {
	return getScreen(screen.currentScreen)
}

export default Viewport