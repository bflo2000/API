import { connect } from 'react-redux'
//import { helloWorld, reset } from './../actions'
import Header from './../components/Header.jsx'

const HeaderContainer = connect(
  //mapStateToProps,
  //mapDispatchToProps
)(Header)

export default HeaderContainer