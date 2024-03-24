import React from 'react';
import { Button, Modal } from 'react-bootstrap';

const AddEmployeeModal = ({show, handleClose}) => {
    return (
        <Modal show={show} onClose={handleClose}>
            <Modal.Header closeButton onClick={handleClose}>
                <Modal.Title>Add Employee</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <p>Modal body content goes here...</p>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={handleClose}>
                    Close
                </Button>
                {/* Additional buttons or actions can be placed here */}
            </Modal.Footer>
        </Modal>
    );
};

export default AddEmployeeModal;