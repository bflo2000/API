import { connect } from 'react-redux'
//import { helloWorld, reset } from './../actions'
import Navbar from './../components/Navbar.jsx'

const NavbarContainer = connect(
  //mapStateToProps,
  //mapDispatchToProps
)(Navbar)

export default NavbarContainer