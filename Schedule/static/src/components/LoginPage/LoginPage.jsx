import React,{useState, useEffect} from 'react';
import { Table, Button, Row, Col } from 'react-bootstrap';
import '../BaseEmployeeDataTable/BaseEmployeeDataTable.css';
import FetchComponent from '../FetchComponent/FetchComponent';
import { useNavigate } from 'react-router-dom';

const LoginPage = () => {
    const navigate = useNavigate();
    const prepData = async () => {
        var infoCells = ['userEmail', 'password'];
        let passWord = document.getElementById("password").value;
        var basicJsonDict = {};
       
        for (let basicCell of infoCells) {
            var cell = document.getElementById(basicCell).value;
            if (cell !== '') {
                basicJsonDict[basicCell] = cell;
            };
        };
        
        const dataVal = await FetchComponent(basicJsonDict, "POST", "/login", null);
        console.log(dataVal['token']);
        const tokenVal = dataVal['token'];
        if (!(tokenVal === null)) {
            navigate('/home', { state: { data: tokenVal } }); 
        } else {
            alert(dataVal['response']);
        };
    }
    
    return (
        <div className='tableContainer'>
            <div className='containerTitle'>
                <Row className='d-flex align-items-center pb-3 px-5 square border-bottom'>
                    <Col className='align-items-center'>
                        <h4>Log in</h4>
                    </Col>
                </Row>
                <Row className='d-flex align-items-center pb-3 px-5 square border-bottom'>
                    <th>Email Address</th>
                    <th><input id="userEmail"></input></th>
                </Row>
                <Row className='d-flex align-items-center pb-3 px-5 square border-bottom'> 
                    <th>Password</th> 
                    <th><input id="password" type = "password"></input></th>
                </Row>
                <Row className='d-flex align-items-center pb-3 px-5 square border-bottom'>
                    <Col>
                        <Button onClick={() => prepData() }>Log in</Button>
                    </Col>
                </Row>
            </div>
        </div>
    )
};
export default LoginPage;

// const PrepData = async() => {
    
// };