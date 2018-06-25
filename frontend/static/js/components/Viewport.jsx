require('../styles.less')
import React from 'react'
import { Screens } from '../actions/actions.jsx'
import Operations from './../components/Operations.jsx'

const getScreen = screen => {
	switch (screen.currentScreen){
		case Screens.SCREEN1:
			return <div id='viewport'><Operations/></div>
		case Screens.SCREEN2:
			return <div id='viewport'>test2</div>
		case Screens.SCREEN3:
			return <div id='viewport'>test3</div>
	}	
}

const Viewport = (currentScreen) => {
	return getScreen(currentScreen)
}

export default Viewport