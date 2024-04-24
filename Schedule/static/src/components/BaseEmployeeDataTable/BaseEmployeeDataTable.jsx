import React,{useState, useEffect} from 'react';
import { Table, Button, Row, Col } from 'react-bootstrap';
import './BaseEmployeeDataTable.css';
import FetchComponent from '../FetchComponent/FetchComponent';
import { DeleteEmployeeModal } from '../DeleteModal/DeleteModal';


const BaseEmployeeDataTable = ({ addEmployee, employeeInfo }) => {
    const [showModal, setShowModal] = useState(false);
    const DeleteEmployee = (empToDelete) => {
        FetchComponent(empToDelete, "POST", "deleteEmployee"); 
        setShowModal(false);
    };
    
    return (
        <div className='tableContainer'>
            <div className='containerTitle'>
                <Row className='d-flex align-items-center pb-3 px-5 square border-bottom'>
                    <Col className='align-items-center'>
                        {addEmployee ? <h4>Add New Employee</h4> : <h4>Edit Employee</h4>}
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
                            <td> {addEmployee ? <input id="id" /> : <input defaultValue={employeeInfo[0]} id="id" />}</td>
                            <td> {addEmployee ? <input id="firstName" /> : <input defaultValue={employeeInfo[1]} id="firstName" />}</td>
                            <td> {addEmployee ? <input id="lastName" /> : <input defaultValue={employeeInfo[2]} id="lastName" />}</td>
                            <td> {addEmployee ? <input id="role" /> : <input defaultValue={employeeInfo[3]} id="role" />}</td>
                            <td> {addEmployee ? <input id="wage" /> : <input defaultValue={employeeInfo[4]} id="wage" />}</td>


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
                            <td> {addEmployee ? <input id="short_shift" /> : <input defaultValue={employeeInfo[5]} id="short_shift" />}</td>
                            <td> {addEmployee ? <input id="long_shift" /> : <input defaultValue={employeeInfo[6]} id="long_shift" />}</td>
                            <td> {addEmployee ? <input id="min_weekly_hours" /> : <input defaultValue={employeeInfo[7]} id="min_weekly_hours" />}</td>
                            <td> {addEmployee ? <input id="max_weekly_hours" /> : <input defaultValue={employeeInfo[8]} id="max_weekly_hours" />}</td>
                            <td> {addEmployee ? <input id="min_days" /> : <input defaultValue={employeeInfo[9]} id="min_days" />}</td>
                            <td> {addEmployee ? <input id="max_days" /> : <input defaultValue={employeeInfo[10]} id="max_days" />}</td>
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
                            <td> {addEmployee ? <input id="sunday_1" /> : <input defaultValue={employeeInfo[11][0]} id="sunday_1" />}</td>
                            <td> {addEmployee ? <input id="monday_1" /> : <input defaultValue={employeeInfo[11][1]} id="monday_1" />}</td>
                            <td> {addEmployee ? <input id="tuesday_1" /> : <input defaultValue={employeeInfo[11][2]} id="tuesday_1" />}</td>
                            <td> {addEmployee ? <input id="wednesday_1" /> : <input defaultValue={employeeInfo[11][3]} id="wednesday_1" />}</td>
                            <td> {addEmployee ? <input id="thursday_1" /> : <input defaultValue={employeeInfo[11][4]} id="thursday_1" />}</td>
                            <td> {addEmployee ? <input id="friday_1" /> : <input defaultValue={employeeInfo[11][5]} id="friday_1" />}</td>
                            <td> {addEmployee ? <input id="saturday_1" /> : <input defaultValue={employeeInfo[11][6]} id="saturday_1" />}</td>

                        </tr>

                        <tr>
                            <td><text>End Time of Availability</text></td>
                            <td> {addEmployee ? <input id="sunday_2" /> : <input defaultValue={employeeInfo[11][7]} id="sunday_2" />}</td>
                            <td> {addEmployee ? <input id="monday_2" /> : <input defaultValue={employeeInfo[11][8]} id="monday_2" />}</td>
                            <td> {addEmployee ? <input id="tuesday_2" /> : <input defaultValue={employeeInfo[11][9]} id="tuesday_2" />}</td>
                            <td> {addEmployee ? <input id="wednesday_2" /> : <input defaultValue={employeeInfo[11][10]} id="wednesday_2" />}</td>
                            <td> {addEmployee ? <input id="thursday_2" /> : <input defaultValue={employeeInfo[11][11]} id="thursday_2" />}</td>
                            <td> {addEmployee ? <input id="friday_2" /> : <input defaultValue={employeeInfo[11][12]} id="friday_2" />}</td>
                            <td> {addEmployee ? <input id="saturday_2" /> : <input defaultValue={employeeInfo[11][13]} id="saturday_2" />}</td>
                        </tr>
                    </tbody>
                </Table>
                <Row className='d-flex align-items-center pb-3 px-5 square border-bottom'>
                    <Col className='d-flex justify-content-end'>
                        <Button id='addEmployee' onClick={() =>PrepEmployeeData(addEmployee)}>
                            {addEmployee ? "Add Employee" : "Update Employee"}
                        </Button>
                    </Col>
                </Row>
                {addEmployee ? null :
                    <Row className='d-flex align-items-center pb-3 px-5 square border-bottom'>
                    <Col className='d-flex justify-content-end'>
                        <Button id='delete' onClick={() => setShowModal(true)}>
                            Delete Employee
                        </Button>
                    </Col>
                </Row>}
            </div>
            {showModal &&
                <DeleteEmployeeModal show={showModal} handleClose={() => setShowModal(false)} handleDelete={() => DeleteEmployee(employeeInfo[0])} />
            }

        </div>
        
    );

};

const PrepEmployeeData = (addEmployee) => {
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
    
    addEmployee ? FetchComponent(basicJsonDict, "POST", "/addEmployee",null) : FetchComponent(basicJsonDict, "POST", "/updateEmployee",null);
};




export default BaseEmployeeDataTable;