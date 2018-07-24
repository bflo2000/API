import React, { Component } from 'react';
import HeaderContainer from './containers/HeaderContainer.jsx'
import MainScreenContainer from './containers/MainScreenContainer.jsx'
import Footer from './components/Footer.jsx'

const App = () => (
    	<div id='react_container'>
    		<HeaderContainer />
      		<MainScreenContainer />
      		<Footer />
      	</div>
    )

export default App;