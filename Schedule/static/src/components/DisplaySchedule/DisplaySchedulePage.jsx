import React,{useState, useEffect} from 'react';
import { Table, Row, Col, Button } from 'react-bootstrap';
import '../BaseEmployeeDataTable/BaseEmployeeDataTable.css';
import FetchComponent from '../FetchComponent/FetchComponent';
import GenerateScheduleModal from '../GenerateSchedule/GenerateScheduleModal';
import ScheduleExists from '../ScheduleExists/ScheduleExists';



const DisplaySchedulePage = () => {
    const [showGenSchedModal, setShowGenSchedModal] = useState(false)
    const [fetchedInfo, setFetchedInfo] = useState(null);
    useEffect(() => {
        // const handleBeforeUnload = (event) => {
        //     event.preventDefault();
        //   };
        const fetchData = async () => {
            try {
                const data = await FetchComponent({"wEndDate":null}, "GET", "/getSchedule",null);
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
                        Schedule For Week Ending {fetchedInfo["response"]==="False" ? fetchedInfo["fetchedDate"] : fetchedInfo["response"][0][11]}
                    </Col>
                    <Col className='d-flex justify-content-end'>
                        <Button id='addNew' onClick={() => setShowGenSchedModal(true)}>
                                {/* <Link id='linkAddNew' to="/generateschedule">Generate New Schedule</Link>     */}
                                Generate New Schedule
                        </Button>
                    </Col>
                </Row>
                {fetchedInfo["response"] === "False" ?  <h6> There is no existing schedule for this week. If you wish to create one, select the Generate Schedule button. Otherwise, select a different week from the drop-down menu.</h6> : <ScheduleExists fetchedInfo={fetchedInfo["response"]} />}
                {showGenSchedModal && <GenerateScheduleModal show={showGenSchedModal} handleClose={() => setShowGenSchedModal(false)} />}
            </div>
        </div>
        
    );
};


export default DisplaySchedulePage;