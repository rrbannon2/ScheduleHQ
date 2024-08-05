import { Table, Row, Col, Button } from 'react-bootstrap';
const ScheduleExists = ({ fetchedInfo }) => {
    console.log(fetchedInfo);
    return(
            <div>
  
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
            </div>)
}
export default ScheduleExists;