import React,{useState, useEffect} from 'react';
import { Table, Button, Row, Col } from 'react-bootstrap';
import '../BaseEmployeeDataTable/BaseEmployeeDataTable.css';
import FetchComponent from '../FetchComponent/FetchComponent';


const SkillPage = ({ addNew, existingInfo }) => {
    console.log(existingInfo);
    
    return (
        <div className='tableContainer'>
            <div className='containerTitle'>
                <Row className='d-flex align-items-center pb-3 px-5 square border-bottom'>
                    <Col className='align-items-center'>
                        {addNew ? <h4>Add New Skill</h4> : <h4>Edit Skill</h4>}
                    </Col>
                </Row>
                <Table striped hover>
                    <thead>
                        <tr>
                            <th>Skill Name</th>
                            <th>Role Required</th>
                            <th>Skill Importance</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td> {addNew ? <input id="skillName" /> : <input defaultValue={existingInfo[0]} id="skillName" />}</td>
                            <td> {addNew ? <input id="role" /> : <input defaultValue={existingInfo[1]} id="firstName" />}</td>
                            <td> {addNew ? <input id="importance" /> : <input defaultValue={existingInfo[2]} id="lastName" />}</td>
                        </tr>
                    </tbody>
                    
                </Table>
                <Row className='d-flex align-items-center pb-3 px-5 square border-bottom'>
                    <Col className='align-items-center'>
                        <h4> When is this skill used/important? </h4>
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
                            <td><text>Start Time</text></td>
                            <td> {addNew ? <input id="sunday_1" /> : <input defaultValue={existingInfo[11][0]} id="sunday_1" />}</td>
                            <td> {addNew ? <input id="monday_1" /> : <input defaultValue={existingInfo[11][1]} id="monday_1" />}</td>
                            <td> {addNew ? <input id="tuesday_1" /> : <input defaultValue={existingInfo[11][2]} id="tuesday_1" />}</td>
                            <td> {addNew ? <input id="wednesday_1" /> : <input defaultValue={existingInfo[11][3]} id="wednesday_1" />}</td>
                            <td> {addNew ? <input id="thursday_1" /> : <input defaultValue={existingInfo[11][4]} id="thursday_1" />}</td>
                            <td> {addNew ? <input id="friday_1" /> : <input defaultValue={existingInfo[11][5]} id="friday_1" />}</td>
                            <td> {addNew ? <input id="saturday_1" /> : <input defaultValue={existingInfo[11][6]} id="saturday_1" />}</td>

                        </tr>

                        <tr>
                            <td><text>End Time</text></td>
                            <td> {addNew ? <input id="sunday_2" /> : <input defaultValue={existingInfo[11][7]} id="sunday_2" />}</td>
                            <td> {addNew ? <input id="monday_2" /> : <input defaultValue={existingInfo[11][8]} id="monday_2" />}</td>
                            <td> {addNew ? <input id="tuesday_2" /> : <input defaultValue={existingInfo[11][9]} id="tuesday_2" />}</td>
                            <td> {addNew ? <input id="wednesday_2" /> : <input defaultValue={existingInfo[11][10]} id="wednesday_2" />}</td>
                            <td> {addNew ? <input id="thursday_2" /> : <input defaultValue={existingInfo[11][11]} id="thursday_2" />}</td>
                            <td> {addNew ? <input id="friday_2" /> : <input defaultValue={existingInfo[11][12]} id="friday_2" />}</td>
                            <td> {addNew ? <input id="saturday_2" /> : <input defaultValue={existingInfo[11][13]} id="saturday_2" />}</td>
                         
                        </tr>
                    </tbody>
                </Table>
                <Row className='d-flex align-items-center pb-3 px-5 square border-bottom'>
                    <Col className='d-flex justify-content-end'>
                        <Button id='addNew' onClick={() => PrepData(addNew)}>
                            {addNew ? "Add Skill" : "Update Skill"}
                        </Button>
                    </Col>
                </Row>
            </div>
        </div>
    );
};

const PrepData = (addNew) => {
    var basicInfoCells = ['skillName', 'role', 'importance',
        'sunday_1', 'monday_1', 'tuesday_1', 'wednesday_1', 'thursday_1', 'friday_1', 'saturday_1',
        'sunday_2', 'monday_2', 'tuesday_2', 'wednesday_2', 'thursday_2', 'friday_2', 'saturday_2'];
    
    var basicJsonDict = {};
   

    for (let basicCell of basicInfoCells) {
        console.log(basicCell)
        var cell = document.getElementById(basicCell).value;
        if (cell !== '') {
            basicJsonDict[basicCell] = cell;
        };
    };
    
    addNew ? FetchComponent(basicJsonDict, "POST", "/addSkill") : FetchComponent(basicJsonDict, "POST", "/updateSkill");
};
export default SkillPage;