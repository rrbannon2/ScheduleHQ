import React,{useState, useEffect} from 'react';
import { Button, Modal, Container, Col, Row, Table } from 'react-bootstrap';
import FetchComponent  from '../FetchComponent/FetchComponent';


export const EmployeeSkillModal = ({ show, empID, handleClose }) => {
    const [fetchedInfo, setFetchedInfo] = useState(null);
    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await FetchComponent({ "dataID": empID }, "GET", "/loadSkillLevels", "employee");
                setFetchedInfo(data["body"]);
            } catch (error) {
                console.error("Error fetching data", error);
                
            }
            return "Success"
        };

        fetchData();
        
    }, []);


    const submitUpdatedSkillLevels = (info) => {
        let skillLevelDict = {};
        skillLevelDict["id"] = empID;
        skillLevelDict["skills"] = {};
        info.map((val) => {
            skillLevelDict["skills"][val[0]] = document.getElementById(val[0] + "level").value;
            skillLevelDict["id"] = empID;
        })
        FetchComponent(skillLevelDict, "POST", "/updateSkillLevel", null);
    }

    return (
        fetchedInfo &&
        <Modal show={show} onClose={handleClose} >
            <Modal.Header closeButton onClick={handleClose}>
                <Modal.Title>Update Skill Levels</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Container>
                    {fetchedInfo.map((val) => {
                        return (
                            <Row key={val[0]}>
                                <Col>{val[0]}</Col>
                                <Col><input id={val[0]+"level"} defaultValue = {val[1]}/></Col>
                            </Row>
                        );
                    })}     
        </Container>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={handleClose}>
                    Cancel
                </Button>
                <Button id="updateSkillLevelBtn" onClick={() => submitUpdatedSkillLevels(fetchedInfo)}>
                    Update Skill Levels
                </Button>
                {/* Additional buttons or actions can be placed here */}
            </Modal.Footer>
        </Modal>
    );
};