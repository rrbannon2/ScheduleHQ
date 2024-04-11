import React from 'react';
import { Table, Button, Row, Col } from 'react-bootstrap';
import '../BaseEmployeeDataTable/BaseEmployeeDataTable.css';
import FetchComponent from '../FetchComponent/FetchComponent';


const BusinessInfoPage = ({ addNew, existingInfo }) => {
    console.log(existingInfo);
    
    return (
        <div className='tableContainer'>
            <div className='containerTitle'>
                <Row className='d-flex align-items-center pb-3 px-5 square border-bottom'>
                    <Col className='align-items-center'>
                        <h4>Add or Update Business Information</h4>
                    </Col>
                </Row>
                <Table striped hover>
                    <thead>
                        <tr>
                            <th>Business Name</th>
                            <td> {addNew ?<input id="name" /> : <input defaultValue={existingInfo[0]} id="name" />} </td>
                        </tr>
                        <tr>
                            <th>Minimum Number of Team Members Working at All Times</th>
                            <th>Minimum Number of Management Team Members Working at All Times</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td> {addNew ? <input id="minEmployees" /> : <input defaultValue={existingInfo[2]} id="minEmployees" />}</td>
                            <td> {addNew ? <input id="minManagers" /> : <input defaultValue={existingInfo[3]} id="minManagers" />}</td>
                        </tr>
                    </tbody>
                    <thead>
                        <tr>
                            <th>Role Assigned to Overtime-Exempt Employees</th>
                            <th>Maximum Number of Hours Per Week (Payroll Budget)</th>
                            <th>How Strict is Limit on Hours Per Week?
                                 (Scale of 1-10 with 10 being the most strict)
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td> {addNew ? <input id="exemptRole" /> : <input defaultValue={existingInfo[4]} id="exemptRole" />}</td>
                            <td> {addNew ? <input id="maxTotalHours" /> : <input defaultValue={existingInfo[5]} id="maxTotalHours" />}</td>
                            <td> {addNew ? <input id="maxHoursImportance" /> : <input defaultValue={existingInfo[6]} id="maxHoursImportance" />}</td>
                        </tr>
                    </tbody>
                    
                </Table>
                <Row className='d-flex align-items-center pb-3 px-5 square border-bottom'>
                    <Col className='align-items-center'>
                        <h4> Hours Of Operation </h4>
                    </Col>
                </Row>
                <Table striped hover>
                    <thead>
                        <tr>
                            <th> </th>
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
                            <td>Opening Time</td>
                            <td> {addNew ? <input id="sunday_1" /> : <input defaultValue={existingInfo[1][0]} id="sunday_1" />}</td>
                            <td> {addNew ? <input id="monday_1" /> : <input defaultValue={existingInfo[1][1]} id="monday_1" />}</td>
                            <td> {addNew ? <input id="tuesday_1" /> : <input defaultValue={existingInfo[1][2]} id="tuesday_1" />}</td>
                            <td> {addNew ? <input id="wednesday_1" /> : <input defaultValue={existingInfo[1][3]} id="wednesday_1" />}</td>
                            <td> {addNew ? <input id="thursday_1" /> : <input defaultValue={existingInfo[1][4]} id="thursday_1" />}</td>
                            <td> {addNew ? <input id="friday_1" /> : <input defaultValue={existingInfo[1][5]} id="friday_1" />}</td>
                            <td> {addNew ? <input id="saturday_1" /> : <input defaultValue={existingInfo[1][6]} id="saturday_1" />}</td>

                        </tr>

                        <tr>
                            <td>Closing Time</td>
                            <td> {addNew ? <input id="sunday_2" /> : <input defaultValue={existingInfo[1][7]} id="sunday_2" />}</td>
                            <td> {addNew ? <input id="monday_2" /> : <input defaultValue={existingInfo[1][8]} id="monday_2" />}</td>
                            <td> {addNew ? <input id="tuesday_2" /> : <input defaultValue={existingInfo[1][9]} id="tuesday_2" />}</td>
                            <td> {addNew ? <input id="wednesday_2" /> : <input defaultValue={existingInfo[1][10]} id="wednesday_2" />}</td>
                            <td> {addNew ? <input id="thursday_2" /> : <input defaultValue={existingInfo[1][11]} id="thursday_2" />}</td>
                            <td> {addNew ? <input id="friday_2" /> : <input defaultValue={existingInfo[1][12]} id="friday_2" />}</td>
                            <td> {addNew ? <input id="saturday_2" /> : <input defaultValue={existingInfo[1][13]} id="saturday_2" />}</td>
                         
                        </tr>
                    </tbody>
                </Table>
                <Row className='d-flex align-items-center pb-3 px-5 square border-bottom'>
                    <Col className='d-flex justify-content-end'>
                        <Button id='addNew' onClick={() => PrepData()}>
                            Update Business Info
                        </Button>
                    </Col>
                </Row>
            </div>
        </div>
    );
};

const PrepData = () => {
    var basicInfoCells = ['name', 'minEmployees', 'minManagers', 'exemptRole', 'maxTotalHours', 'maxHoursImportance',
    'sunday_1', 'monday_1', 'tuesday_1', 'wednesday_1', 'thursday_1', 'friday_1', 'saturday_1',
    'sunday_2', 'monday_2', 'tuesday_2', 'wednesday_2', 'thursday_2', 'friday_2', 'saturday_2'];
    
    var basicJsonDict = {};
   

    for (let basicCell of basicInfoCells) {
        console.log(basicCell);
        var cell = document.getElementById(basicCell).value;
        if (cell !== '') {
            basicJsonDict[basicCell] = cell;
        };
    };
    
    FetchComponent(basicJsonDict, "POST", "/updateBusinessInfo");
};
export default BusinessInfoPage;