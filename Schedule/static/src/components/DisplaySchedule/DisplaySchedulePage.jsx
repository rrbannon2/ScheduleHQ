import React,{useState, useEffect} from 'react';
import { Table, Row, Col, Button } from 'react-bootstrap';
import '../BaseEmployeeDataTable/BaseEmployeeDataTable.css';
import FetchComponent from '../FetchComponent/FetchComponent';
import GenerateScheduleModal from '../GenerateSchedule/GenerateScheduleModal';





const DisplaySchedulePage = () => {
    const [showGenSchedModal, setShowGenSchedModal] = useState(false)
    const [fetchedInfo, setFetchedInfo] = useState(null);
    useEffect(() => {
        // const handleBeforeUnload = (event) => {
        //     event.preventDefault();
        //   };
        const fetchData = async () => {
            try {
                const data = await FetchComponent(null, "GET", "/getSchedule",null);
                setFetchedInfo(data["body"]);
            } catch (error) {
                console.error("Error fetching data", error);
                
            }
            return "Success"
        };

        fetchData();

    }, []);
    console.log(fetchedInfo);
    return (
        fetchedInfo && 
        <div className='tableContainer'>
            <div className='containerTitle'>
                <Row className='d-flex align-items-center pb-3 px-5 square border-bottom'>
                    <Col className='align-items-center'>
                        Schedule For Week Ending {fetchedInfo[0][11]}
                    </Col>
                    <Col className='d-flex justify-content-end'>
                        <Button id='addNew' onClick={() => setShowGenSchedModal(true)}>
                                {/* <Link id='linkAddNew' to="/generateschedule">Generate New Schedule</Link>     */}
                                Generate New Schedule
                        </Button>
                    </Col>
                </Row>
  
                <Table striped hover responsive>
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
                                <th>Hours</th>
                        </tr>
                    </thead>
                    <tbody>
                        {fetchedInfo.map((value) => {
                            var splitVal = value;
                        
                            return (
                                <tr key={splitVal[0]}>
                                    <td>{splitVal[1] + " " + splitVal[2]}</td>
                                    <td>{splitVal[3]}</td>
                                    <td>{splitVal[4]}</td>
                                    <td>{splitVal[5]}</td>
                                    <td>{splitVal[6]}</td>
                                    <td>{splitVal[7]}</td>
                                    <td>{splitVal[8]}</td>
                                    <td>{splitVal[9]}</td>
                                    <td>{splitVal[10]}</td>
                                </tr>
                            );
                        })}     
                    </tbody>
                </Table>
                </div>
                {showGenSchedModal && <GenerateScheduleModal show={showGenSchedModal} handleClose={() => setShowGenSchedModal(false)} />}
        </div>
    );
};


export default DisplaySchedulePage;