import React, { useState, useEffect } from 'react';
import axios from "axios";
import { Table, Button, Row, Col } from 'react-bootstrap';
import './EmployeeTable.css';
import AddEmployeeModal from '../AddEmployeeModal/AddEmployeeModal';
import FetchComponent from '../FetchComponent/FetchComponent';

const EmployeeTable = () => {
    const [listOfEmployees, setListOfEmployees] = useState([]);
    const [showModal, setShowModal] = useState(false);

    useEffect(() => {
        axios.get("http://localhost:3000/loadEmployeeListData").then((response) => {
            setListOfEmployees(response.data);
        });
    }, []);
    console.log(listOfEmployees);
    // const [fetchedInfo, setFetchedInfo] = useState(null);

    // useEffect(() => {
    //     const fetchData = async () => {
    //         try {
    //             const data = await FetchComponent(null, "GET", "loadEmployeeNames", false);
    //             setFetchedInfo(data);
    //             console.log(data);
    //         } catch (error) {
    //             console.error("Error fetching shift data", error);
    //             // Handle the error accordingly
    //         }
    //     };

    //     fetchData();
    // }, []);
    return (
        <div className='tableContainer'>
            <div className='containerTitle'>
                <Row className='d-flex align-items-center pb-3 px-5 square border-bottom'>
                    <Col className='align-items-center'>
                        <h4>Employees</h4>
                    </Col>
                    <Col className='d-flex justify-content-end'>
                        <Button id='addEmployee'>
                            Add Employee
                        </Button>
                    </Col>
                </Row>
                <Table striped hover>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>First Name</th>
                            <th>Last Name</th>
                            <th>Username</th>
                            <th>Edit</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>1</td>
                            <td>Mark</td>
                            <td>Otto</td>
                            <td>@mdo</td>
                            <td>
                                <Button variant='link' onClick={() => setShowModal(true)}>
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-three-dots" viewBox="0 0 16 16">
                                        <path d="M3 9.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3m5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3m5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3" />
                                    </svg>
                                </Button>
                            </td>
                        </tr>
                        <tr>
                            <td>2</td>
                            <td>Jacob</td>
                            <td>Thornton</td>
                            <td>@fat</td>
                            <td>
                                <Button variant='link'>
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-three-dots" viewBox="0 0 16 16">
                                        <path d="M3 9.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3m5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3m5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3" />
                                    </svg>
                                </Button>
                            </td>
                        </tr>
                        <tr>
                            <td>3</td>
                            <td colSpan={2}>Larry the Bird</td>
                            <td>@twitter</td>
                            <td>
                                <Button variant='link'>
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-three-dots" viewBox="0 0 16 16">
                                        <path d="M3 9.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3m5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3m5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3" />
                                    </svg>
                                </Button>
                            </td>
                        </tr>
                        <tr>
                            <td>4</td>
                            <td>Jacob</td>
                            <td>Thornton</td>
                            <td>@fat</td>
                            <td>
                                <Button variant='link'>
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-three-dots" viewBox="0 0 16 16">
                                        <path d="M3 9.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3m5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3m5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3" />
                                    </svg>
                                </Button>
                            </td>
                        </tr>
                    </tbody>
                </Table>
            </div>
            {showModal &&
                <AddEmployeeModal show={showModal} handleClose={() => setShowModal(false)} />
            }
        </div>
    );
};

export default EmployeeTable;