import React from 'react';
import { Button, Modal } from 'react-bootstrap';


export const EmployeeSkillModal = ({show, handleClose, handleSubmit}) => {
    return (
        <Modal show={show} onClose={handleClose} >
            <Modal.Header closeButton onClick={handleClose}>
                <Modal.Title>Delete Employee</Modal.Title>
            </Modal.Header>
            <Modal.Body>
            <p>Are you sure you want to delete this employee?</p>
            <p>This action <b>cannot be undone</b> and will delete all information associated with the employee.</p>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={handleClose}>
                    Cancel
                </Button>
                <Button id="updateSkillLevelBtn" onClick={handleSubmit}>
                    Update Skills
                </Button>
                {/* Additional buttons or actions can be placed here */}
            </Modal.Footer>
        </Modal>
    );
};