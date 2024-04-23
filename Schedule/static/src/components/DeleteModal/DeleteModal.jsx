import React from 'react';
import { Button, Modal } from 'react-bootstrap';
import './DeleteModal.css';

const DeleteEmployeeModal = ({show, handleClose, handleDelete}) => {
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
                <Button id="deleteBtn" onClick={handleDelete}>
                    Delete Employee
                </Button>
                {/* Additional buttons or actions can be placed here */}
            </Modal.Footer>
        </Modal>
    );
};



export default DeleteEmployeeModal;