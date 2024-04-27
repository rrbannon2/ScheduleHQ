import React, { useState, useEffect } from 'react';
import { Table, Button, Row, Col } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import FetchComponent from '../FetchComponent/FetchComponent';
import '../BaseEmployeeDataTable/BaseEmployeeDataTable.css';

const GenerateSchedulePage = () => {


    return (
        <div className='tableContainer'>
            <div className='containerTitle'>
                <Row className='d-flex align-items-center pb-3 px-5 square border-bottom'>
                    <Col className='align-items-center'>
                        <h4>Schedule Generation Details</h4>
                    </Col>
                    <Col className='d-flex justify-content-end'>
                        <Button id='addNew'  onClick={() => FetchComponent({ "date": document.getElementById("date").value, "seconds":document.getElementById("seconds").value },"POST","/writeSchedule",null)}> {/* Should probably be using something like useState rather than DOM manipulation. FIX */}
                            <Link id='linkAddNew' to="/">Generate Schedule Now</Link>
                        </Button>
                    </Col>
                </Row>
                <Table striped hover>
                    <thead>
                        <tr>
                            <th>Week Ending Date:</th>
                            <td> <input id="date"></input></td>
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