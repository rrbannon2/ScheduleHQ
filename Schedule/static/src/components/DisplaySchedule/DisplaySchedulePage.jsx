import React,{useState, useEffect} from 'react';
import { Table, Button, Row, Col } from 'react-bootstrap';
import '../BaseEmployeeDataTable/BaseEmployeeDataTable.css';
import FetchComponent from '../FetchComponent/FetchComponent';


const DisplaySchedulePage = ({ employeeInfo }) => {
    
    return (
        <div className='tableContainer'>
            <div className='containerTitle'>
                <Row className='d-flex align-items-center pb-3 px-5 square border-bottom'>
                    <Col className='align-items-center'>
                        
                    </Col>
                </Row>
                <Table striped hover>
                    <thead>
                        <tr>
                            
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            


                        </tr>
                    </tbody>
                    
                </Table>
                
                


            </div>
        </div>
    );
};


export default DisplaySchedulePage;