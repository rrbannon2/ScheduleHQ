import React,{useState, useEffect} from 'react';
import { Button, Modal, Container, Col, Row, Table } from 'react-bootstrap';
import FetchComponent  from '../FetchComponent/FetchComponent';


export const EmployeeSkillModal = ({ show, skillLevelInfo, handleClose }) => {
    
    console.log(skillLevelInfo);
    
    return (
        <Modal show={show} onClose={handleClose} >
            <Modal.Header closeButton onClick={handleClose}>
                <Modal.Title>Update Skill Levels</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Container>
                    {skillLevelInfo.map((value) => {
                        var splitVal = value;
                        return (
                            <Row key={splitVal[0]}>
                                <Col>{splitVal[0]}</Col>
                                <Col><input placeholder = {splitVal[1]}/></Col>
                                <Col><Button id={splitVal[0]+"SubmitBtn"}>Update Only This Skill Level</Button></Col>
                            </Row>
                        );
                    })}     
        </Container>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={handleClose}>
                    Cancel
                </Button>
                <Button id="updateSkillLevelBtn" onClick={handleClose}>
                    Update Skills
                </Button>
                {/* Additional buttons or actions can be placed here */}
            </Modal.Footer>
        </Modal>
    );
};