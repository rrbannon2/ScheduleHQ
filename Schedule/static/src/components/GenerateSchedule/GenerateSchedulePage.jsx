import React, { useState, useEffect } from 'react';
import { Table, Button, Row, Col } from 'react-bootstrap';
import { Link,useNavigate } from 'react-router-dom';
import FetchComponent from '../FetchComponent/FetchComponent';
import '../BaseEmployeeDataTable/BaseEmployeeDataTable.css';
// TODO: Make this component a modal on the display schedule page,
// would avoid needing to navigate and the clunky name in navbar.
const GenerateSchedulePage = () => {

    return (
        <div className='tableContainer'>
            <div className='containerTitle'>
                <Row className='d-flex align-items-center pb-3 px-5 square border-bottom'>
                    <Col className='align-items-center'>
                        <h4>Schedule Generation Details</h4>
                    </Col>
                    <Col className='d-flex justify-content-end'>
                        <Button id='addNew' onClick={() => SubmitData()}>
                            Generate Schedule Now
                        </Button>
                    </Col>
                </Row>
                <Table striped hover>
                    <thead>
                        <tr>
                            <th>Week Ending Date:</th>
                            <td> <input onBlur={() => ValidateData()} id="date"></input></td>
                        </tr>

                        <tr>
                            <th>How long are you willing to wait for your schedule to be optimized? (In seconds)</th>
                            <td><input id="seconds"></input></td>
                        </tr>
                    </thead>
               </Table>
            </div>
        </div>
    );
};

export default GenerateSchedulePage;

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

const SubmitData = () => {
    ValidateData() ? FetchComponent({ "date": document.getElementById("date").value, "seconds": document.getElementById("seconds").value }, "POST", "/writeSchedule", null) :
        console.log("Date not valid");
    
};