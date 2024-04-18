import React,{useState, useEffect} from 'react';
import { Table, Row, Col } from 'react-bootstrap';
import '../BaseEmployeeDataTable/BaseEmployeeDataTable.css';
import FetchComponent from '../FetchComponent/FetchComponent';


const DisplaySchedulePage = () => {
    
    const [fetchedInfo, setFetchedInfo] = useState(null);

    useEffect(() => {
        const handleBeforeUnload = (event) => {
            event.preventDefault();
            // Custom logic to handle the refresh
            // Display a confirmation message or perform necessary actions
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
        // console.log(fetchedInfo);
    }, []);

    // Render component only when empInfo is available
    return (
        fetchedInfo && 
        <div className='tableContainer'>
            <div className='containerTitle'>
                <Row className='d-flex align-items-center pb-3 px-5 square border-bottom'>
                    <Col className='align-items-center'>
                        Schedule For Week Ending XX/XX/XXXX
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
                        {fetchedInfo.map((value, key) => {
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
                        })}     
                    </tbody>
                </Table>
            </div>
        </div>
    );
};
const formatScheduleData = (data) => {
    
    var scheduleDict = {};
    for (var i in data) {
        if (data[i] !== "") {
            var block = data[i].split(":");
            // console.log(block);
            var empName = block[0];
            var shiftTime = block[1];
            // console.log(shiftTime);
            if (scheduleDict.hasOwnProperty(empName)) {
                scheduleDict[empName].push(shiftTime);
            }
            else {
                scheduleDict[empName] = [];
                scheduleDict[empName].push(shiftTime);
                // scheduleDict[empName].push("Off");
            };
        };
    };
    return scheduleDict;
};

export default DisplaySchedulePage;