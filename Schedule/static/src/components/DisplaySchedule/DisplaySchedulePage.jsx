import React,{useState, useEffect} from 'react';
import { Table, Row, Col, Button } from 'react-bootstrap';
import '../BaseEmployeeDataTable/BaseEmployeeDataTable.css';
import FetchComponent from '../FetchComponent/FetchComponent';
import { Link } from 'react-router-dom';



const DisplaySchedulePage = () => {
    
    const [fetchedInfo, setFetchedInfo] = useState(null);

    useEffect(() => {
        const handleBeforeUnload = (event) => {
            event.preventDefault();
          };
        const fetchData = async () => {
            try {
                const data = await FetchComponent(null, "GET", "/getSchedule",false);
                setFetchedInfo(data);
            } catch (error) {
                console.error("Error fetching shift data", error);
                // Handle the error accordingly
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