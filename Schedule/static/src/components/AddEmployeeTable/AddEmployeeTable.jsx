import React, {useState} from 'react';
import { Table, Button, Row, Col } from 'react-bootstrap';
import './AddEmployeeTable.css';
import AddEmployeeModal from '../AddEmployeeModal/AddEmployeeModal';
import FetchComponent from '../FetchComponent/FetchComponent';

const AddEmployeeTable = () => {
    return (
        <div className='tableContainer'>
            <div className='containerTitle'>
                <Row className='d-flex align-items-center pb-3 px-5 square border-bottom'>
                    <Col className='align-items-center'>
                        <h4>Add New Employee</h4>
                    </Col>
                </Row>
                <Table striped hover>
                    <thead>
                        <tr>
                            <th>Employee ID</th>
                            <th>First Name</th>
                            <th>Last Name</th>
                            <th>Role</th>
                            <th>Wage</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><input id = "id"/></td>
                            <td><input id = "firstName" type = "text"/></td>
                            <td><input id = "lastName" type = "text"/></td>
                            <td><input id="role" /></td>
                            <td><input id = "wage"/></td>
                            {/* <td>
                                <Button variant='link' onClick={() => setShowModal(true)}>
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-three-dots" viewBox="0 0 16 16">
                                        <path d="M3 9.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3m5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3m5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3" />
                                    </svg>
                                </Button>
                            </td> */}
                        </tr>
                    </tbody>
                    <tbody>
                    <tr></tr>
                    </tbody>
                    <thead>
                        <tr>
                            <th>Minimum Shift Length</th>
                            <th>Maximum Shift Length</th>
                            <th>Minimum Hours Per Week</th>
                            <th>Maximum Hours Per Week</th>
                            <th>Minimum Days Per Week</th>
                            <th>Maximum Days Per Week</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><input id="short_shift" type="text"/></td>
                            <td><input id="long_shift" type="text"/></td>
                            <td><input id="min_weekly_hours" type="text"/></td>
                            <td><input id="max_weekly_hours" type="text"/></td>
                            <td><input id="min_days" type="text"/></td>
                            <td><input id="max_days" type="text"/></td>
                        </tr>
                    </tbody>
                </Table>
                <Row className='d-flex align-items-center pb-3 px-5 square border-bottom'>
                    <Col className='align-items-center'>
                        <h4>Enter Employee Availability Below</h4>
                    </Col>
                </Row>
                <Table striped hover>
                    <thead>
                        <tr>
                            <th>Day</th>
                            <th>Sunday</th>
                            <th>Monday</th>
                            <th>Tuesday</th>
                            <th>Wednesday</th>
                            <th>Thursday</th>
                            <th>Friday</th>
                            <th>Saturday</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><text>Start Time of Availability</text></td>
                            <td><input id="sunday_1" type="text"/></td>
                            <td><input id="monday_1" type="text"/></td>
                            <td><input id="tuesday_1" type="text"/></td>
                            <td><input id="wednesday_1" type="text"/></td>
                            <td><input id="thursday_1" type="text"/></td>
                            <td><input id="friday_1" type="text"/></td>
                            <td><input id="saturday_1" type="text"/></td>
                        </tr>

                        <tr>
                            <td><text>End Time of Availability</text></td>
                            <td><input id="sunday_2" type="text"/></td>
                            <td><input id="monday_2" type="text"/></td>
                            <td><input id="tuesday_2" type="text"/></td>
                            <td><input id="wednesday_2" type="text"/></td>
                            <td><input id="thursday_2" type="text"/></td>
                            <td><input id="friday_2" type="text"/></td>
                            <td><input id="saturday_2" type="text"/></td>
                        </tr>
                    </tbody>
                </Table>
                <Row className='d-flex align-items-center pb-3 px-5 square border-bottom'>
                    <Col className='d-flex justify-content-end'>
                        <Button id='addEmployee' onClick={() =>PrepEmployeeData()}>
                            Add Employee
                        </Button>
                    </Col>
                </Row>
            </div>
        </div>
    );
};

function PrepEmployeeData() {
    var basicInfoCells = ['id', 'firstName', 'lastName', 'role', 'wage', 'short_shift', 'long_shift', 'min_weekly_hours',
        'max_weekly_hours', 'min_days', 'max_days', 'sunday_1', 'monday_1', 'tuesday_1', 'wednesday_1', 'thursday_1', 'friday_1',
        'saturday_1', 'sunday_2', 'monday_2', 'tuesday_2', 'wednesday_2', 'thursday_2', 'friday_2', 'saturday_2'];
    
    var basicJsonDict = {};
   

    for (let basicCell of basicInfoCells) {
        console.log(basicCell)
        var cell = document.getElementById(basicCell).value;
        if (cell !== '') {
            basicJsonDict[basicCell] = cell;
        };
    };
    

    FetchComponent(basicJsonDict, "POST", "/addEmployee");
};
export default AddEmployeeTable;