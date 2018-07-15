require('../styles.less')
import React from 'react'
import { Nav, NavItem } from 'react-bootstrap';
import LinkContainer from '../containers/LinkContainer.jsx'

const Navbar = () => (
  <Nav bsStyle="pills" stacked id='navbar'>
    <NavItem>
      <LinkContainer screen={'SCREEN1'}>Database Operations</LinkContainer>
    </NavItem>
    <NavItem>
      <LinkContainer screen={'SCREEN2'}>Database Queries</LinkContainer>
    </NavItem>
  </Nav>
)

export default Navbar