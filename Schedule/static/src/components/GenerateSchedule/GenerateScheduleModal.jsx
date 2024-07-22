import React, { useState, useEffect } from 'react';
import { Table, Button, Row, Col, Modal,Container,Form } from 'react-bootstrap';
import { Link,useNavigate } from 'react-router-dom';
import FetchComponent from '../FetchComponent/FetchComponent';
import '../BaseEmployeeDataTable/BaseEmployeeDataTable.css';

const GenerateScheduleModal = ({show,handleClose}) => {

    return (
        <Modal show={show} onClose={handleClose}>
            <Modal.Header>
                <Modal.Title>
                    Generate New Schedule
                </Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form>
                    <Form.Group controlId="date">
                        <Form.Label>Week Ending Date:</Form.Label>
                        <Form.Control type="fullDate" placeholder="MM/DD/YYYY" autoFocus />                        
                    </Form.Group>
                    <Form.Group controlId="seconds">
                        <Form.Label>How long are you willing to wait for your schedule to be optimized? (In seconds)</Form.Label>
                        <Form.Control type="int" />
                    </Form.Group>
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <Button onClick={() => SubmitData(handleClose)}>Generate Schedule Now</Button>
                <Button onClick={handleClose}>Cancel</Button>
            </Modal.Footer>
        </Modal>
    );
};

export default GenerateScheduleModal;

const ValidateData = () => {
    const dateRegExp = /[0-3]\d\/[0-3]\d\/\d\d\d\d/;
    var dateVal = document.getElementById("date").value;

    if (!dateVal.match(dateRegExp)) {
        alert("Date Entered Not Valid, Format Must Be DD/MM/YYYY or MM/DD/YYYY");
        return null;
    };
    // alert("test");
    
    return true;
};

const SubmitData = (handleClose) => {
    ValidateData() ? FetchComponent({ "date": document.getElementById("date").value, "seconds": document.getElementById("seconds").value }, "POST", "/writeSchedule", null) :
        console.log("Date not valid");
    { handleClose() }
    
};