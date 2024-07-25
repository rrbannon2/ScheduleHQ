import React,{useState, useEffect} from 'react';
import { Table, Button, Row, Col } from 'react-bootstrap';
import '../BaseEmployeeDataTable/BaseEmployeeDataTable.css';
import FetchComponent from '../FetchComponent/FetchComponent';
import { DeleteShiftModal } from '../DeleteModal/DeleteModal';

const ShiftPage = ({ addNew, existingInfo }) => {
    console.log(existingInfo);
    
    const [showModal, setShowModal] = useState(false);
    const DeleteShift = (toDelete) => {
        FetchComponent(toDelete, "POST", "/deleteShift"); 
        setShowModal(false);
    };
    return (
        <div className='tableContainer'>
            <div className='containerTitle'>
                <Row className='d-flex align-items-center pb-3 px-5 square border-bottom'>
                    <Col className='align-items-center'>
                        {addNew ? <h4>Add New Shift</h4> : <h4>Edit Shift</h4>}
                    </Col>
                </Row>
                <Table striped hover>
                    <thead>
                        <tr>
                            <th>Shift Name</th>
                            <th>Shift Importance</th>
                            <th>Maximum Hours to Use</th> {/* Add hoverable info icon to inform user that if value is 0, no limit is being applied to number of hours used. */}
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td> {addNew ? <input id="shiftName" /> : <input defaultValue={existingInfo[0]} id="shiftName" />}</td>
                            <td> {addNew ? <input id="importance" /> : <input defaultValue={existingInfo[2]} id="importance" />}</td>
                            <td> {addNew ? <input id="maxHours" /> : <input defaultValue={existingInfo[3]} id="maxHours" />}</td>
                        </tr>
                    </tbody>
                    
                </Table>
                <Row className='d-flex align-items-center pb-3 px-5 square border-bottom'>
                    <Col className='align-items-center'>
                        <h4> When does this shift occur? </h4>
                    </Col>
                </Row>
                <Table striped hover>
                    <thead>
                        <tr>
                            <th> </th>
                            <th>Start Time</th>
                            <th>End Time</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Sunday</td>
                            <td> {addNew ? <input id="sunday_1" /> : <input defaultValue={existingInfo[1][0]} id="sunday_1" />}</td>
                            <td> {addNew ? <input id="sunday_2" /> : <input defaultValue={existingInfo[1][7]} id="sunday_2" />}</td>
                        </tr>

                        <tr>
                            <td>Monday</td>                            
                            <td> {addNew ? <input id="monday_1" /> : <input defaultValue={existingInfo[1][1]} id="monday_1" />}</td>
                            <td> {addNew ? <input id="monday_2" /> : <input defaultValue={existingInfo[1][8]} id="monday_2" />}</td>                            
                        </tr>
                        <tr>
                            <td>Tuesday</td>
                            <td> {addNew ? <input id="tuesday_1" /> : <input defaultValue={existingInfo[1][2]} id="tuesday_1" />}</td>
                            <td> {addNew ? <input id="tuesday_2" /> : <input defaultValue={existingInfo[1][9]} id="tuesday_2" />}</td>
                        </tr>
                        <tr>
                            <td>Wednesday</td>
                            <td> {addNew ? <input id="wednesday_1" /> : <input defaultValue={existingInfo[1][3]} id="wednesday_1" />}</td>
                            <td> {addNew ? <input id="wednesday_2" /> : <input defaultValue={existingInfo[1][10]} id="wednesday_2" />}</td>
                        </tr>
                        <tr>
                            <td>Thursday</td>
                            <td> {addNew ? <input id="thursday_1" /> : <input defaultValue={existingInfo[1][4]} id="thursday_1" />}</td>
                            <td> {addNew ? <input id="thursday_2" /> : <input defaultValue={existingInfo[1][11]} id="thursday_2" />}</td>
                        </tr>
                        <tr>
                            <td>Friday</td>
                            <td> {addNew ? <input id="friday_1" /> : <input defaultValue={existingInfo[1][5]} id="friday_1" />}</td>
                            <td> {addNew ? <input id="friday_2" /> : <input defaultValue={existingInfo[1][12]} id="friday_2" />}</td>
                        </tr>
                        <tr>
                            <td>Saturday</td>
                            <td> {addNew ? <input id="saturday_1" /> : <input defaultValue={existingInfo[1][6]} id="saturday_1" />}</td>
                            <td> {addNew ? <input id="saturday_2" /> : <input defaultValue={existingInfo[1][13]} id="saturday_2" />}</td>
                        </tr>

                    </tbody>
                </Table>
                
                <Row className='d-flex align-items-center pb-3 px-5 square border-bottom'>
                    <Col className='d-flex justify-content-end'>
                        <Button id='addNew' onClick={() => PrepData(addNew)}>
                            {addNew ? "Add Shift" : "Update Shift"}
                        </Button>
                    </Col>
                </Row>
                {addNew ? null :
                    <Row className='d-flex align-items-center pb-3 px-5 square border-bottom'>
                    <Col className='d-flex justify-content-end'>
                        <Button id='delete' onClick={() => setShowModal(true)}>
                            Delete Shift
                        </Button>
                    </Col>
                </Row>}
            </div>
            {showModal &&
                <DeleteShiftModal show={showModal} handleClose={() => setShowModal(false)} handleDelete={() => DeleteShift(existingInfo[0])} />
            }
        </div>
    );
};

const PrepData = (addNew) => {
    var basicInfoCells = ['shiftName','importance','maxHours',
        'sunday_1', 'monday_1', 'tuesday_1', 'wednesday_1', 'thursday_1', 'friday_1', 'saturday_1',
        'sunday_2', 'monday_2', 'tuesday_2', 'wednesday_2', 'thursday_2', 'friday_2', 'saturday_2'];
    
    var basicJsonDict = {};
   

    for (let basicCell of basicInfoCells) {
        var cell = document.getElementById(basicCell).value;
        if (cell !== '') {
            basicJsonDict[basicCell] = cell;
        };
    };
    
    addNew ? FetchComponent(basicJsonDict, "POST", "/addShift",null) : FetchComponent(basicJsonDict, "POST", "/updateShift",null);
};
export default ShiftPage;