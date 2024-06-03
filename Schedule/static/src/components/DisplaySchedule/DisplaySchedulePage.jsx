import React,{useState, useEffect} from 'react';
import { Table, Row, Col, Button } from 'react-bootstrap';
import '../BaseEmployeeDataTable/BaseEmployeeDataTable.css';
import FetchComponent from '../FetchComponent/FetchComponent';
import { Link,useLocation,Navigate, useNavigate, redirect } from 'react-router-dom';




const DisplaySchedulePage = () => {
    
    const [fetchedInfo, setFetchedInfo] = useState(null);
    var token = useLocation().state;
    try {
        token = { "dataID": token['data'] };
    } catch (error) {
        alert("You are not currently signed in, you will now be redirected to the sign in page.")
        Navigate({"to":'/'});
    }

    useEffect(() => {
        const handleBeforeUnload = (event) => {
            event.preventDefault();
          };
        const fetchData = async () => {
            try {
                const data = await FetchComponent(token, "GET", "/getSchedule","token");
                setFetchedInfo(data);
            } catch (error) {
                alert("Please return to the log in page");
                console.error("Error fetching data", error);
            }
        };

        fetchData();

    }, []);


    return (
        fetchedInfo && 
        <div className='tableContainer'>
            <div className='containerTitle'>
                <Row className='d-flex align-items-center pb-3 px-5 square border-bottom'>
                    <Col className='align-items-center'>
                        Schedule For Week Ending {fetchedInfo[0].split(" ")[1]}
                    </Col>
                    <Col className='d-flex justify-content-end'>
                        <Button id='addNew'>
                            <Link id='linkAddNew' to="/generateschedule">Generate New Schedule</Link>    
                        </Button>
                    </Col>
                </Row>
  
                <Table striped hover>
                    <thead>
                        
                        <tr>
                                <th></th>
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
                        {fetchedInfo.map((value) => {
                            if (value.substring(0, 3) !== "*-!") {
                                var splitVal = value.split(",");
                            
                                return (
                                    <tr key={splitVal[0]}>
                                        <td>{splitVal[0]}</td>
                                        <td>{splitVal[1]}</td>
                                        <td>{splitVal[2]}</td>
                                        <td>{splitVal[3]}</td>
                                        <td>{splitVal[4]}</td>
                                        <td>{splitVal[5]}</td>
                                        <td>{splitVal[6]}</td>
                                        <td>{splitVal[7]}</td>
                                    </tr>
                                );
                            }
                            else {return null};
                        })}     
                    </tbody>
                </Table>
            </div>
        </div>
    );
};


export default DisplaySchedulePage;