import React from 'react';
import {Navbar, Nav, NavDropdown, Form} from 'react-bootstrap';

import OpenFile from './OpenFile';
import logo from './logo.png';


export default class NavigationBar extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      "classes": "navbar navbar-expand navbar-dark bg-dark flex-column flex-md-row w-100",
      "style": {"position": 'fixed', "top": 0, "zIndex": 999}
    }
  }

  render() {
    return (
      <header>

        <Navbar bg="dark" variant={"dark"} fixed="top" expand="xl">
          <Navbar.Brand href="#home">
            <img className={"d-inline-block align-top"} width={36} height={36} alt={"logo"} src={logo}/>
            <h3 className={"d-inline-block ml-2 my-1"}>
              {"PLT Editor"}
            </h3>
          </Navbar.Brand>

          <Navbar.Toggle aria-controls="basic-navbar-nav"/>

          <Navbar.Collapse id="basic-navbar-nav">

            <Nav className="ml-auto mr-2">
              <Nav.Link href="#home">Home</Nav.Link>
              <Nav.Link href="#link">Link</Nav.Link>
              <NavDropdown title="Dropdown" id="basic-nav-dropdown">
                <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
                <NavDropdown.Item href="#action/3.2">Another action</NavDropdown.Item>
                <NavDropdown.Item href="#action/3.3">Something</NavDropdown.Item>
                <NavDropdown.Divider/>
                <NavDropdown.Item href="#action/3.4">Separated link</NavDropdown.Item>
              </NavDropdown>
            </Nav>


            <OpenFile/>


          </Navbar.Collapse>
        </Navbar>

      </header>
    )
  }
}
