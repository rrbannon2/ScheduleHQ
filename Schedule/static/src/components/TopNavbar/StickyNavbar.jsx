import React from 'react';
import { Navbar, Nav, Container } from 'react-bootstrap';
import './StickyNavbar.css';

const StickyNavbar = () => {
  return (
    <Navbar expand="lg" className="topNavbar">
      <Container fluid style={{margin: '20px 80px'}}>
        <Navbar.Brand href="#home">Schedule HQ</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link href="#home">Employees</Nav.Link>
            <Nav.Link href="#link">Skills</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default StickyNavbar;