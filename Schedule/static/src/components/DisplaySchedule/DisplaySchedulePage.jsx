import React,{useState, useEffect} from 'react';
import { Table, Row, Col, Button } from 'react-bootstrap';
import '../BaseEmployeeDataTable/BaseEmployeeDataTable.css';
import FetchComponent from '../FetchComponent/FetchComponent';
import GenerateScheduleModal from '../GenerateSchedule/GenerateScheduleModal';
import ScheduleExists from '../ScheduleExists/ScheduleExists';
import { WeeksDropDown } from '../WeeksDropDown/WeeksDropDown';
import { useLocation } from 'react-router-dom';

const DisplaySchedulePage = () => {
    const [showGenSchedModal, setShowGenSchedModal] = useState(false)
    const [fetchedInfo, setFetchedInfo] = useState(null);
    let dateID = { "dataID": useLocation().state };
    console.log(dateID);
    // console.log(dateID["dataID"]);
    const ValidateData = (dateVal) => {
        const dateRegExp = /[0-3]\d\/[0-3]\d\/\d\d\d\d/;
        console.log(dateVal);
        console.log(typeof dateVal);
        try {
            if (!dateVal.match(dateRegExp)) {
            
                return false;
            };
        } catch (error) {
            return false;
        }
        // alert("test");
        
        return true;
    };

    useEffect(() => {
        // const handleBeforeUnload = (event) => {
        //     event.preventDefault();
        //   };
        console.log(dateID["dataID"]);
        const fetchData = async () => {
            try {
                let data;
                ValidateData(dateID["dataID"]) ? data = await FetchComponent(dateID, "GET", "/getSchedule","wEndDate") : data = await FetchComponent(null, "GET", "/getSchedule",null)
                setFetchedInfo(data["body"]);
            } catch (error) {
                console.error("Error fetching data", error);
                
            }
            return "Success"
        };

        fetchData();

    }, [useLocation().state]);
    console.log(fetchedInfo);
    return (
        fetchedInfo && 
        <div className='tableContainer'>
            <div className='containerTitle'>
                <Row className='d-flex align-items-center pb-3 px-5 square border-bottom'>
                    <Col className='align-items-center'>
                        Schedule For Week Ending {fetchedInfo["fetchedDate"]}
                    </Col>
                    <Col className='align-items-center'>
                            <WeeksDropDown datesInfo={fetchedInfo["datesInfo"]} />        
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