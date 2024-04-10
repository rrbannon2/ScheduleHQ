import React from 'react';
import ShiftPage from '../ShiftPage/ShiftPage';

const AddShiftPage = () => {
    return (
        <ShiftPage addNew={true} existingInfo={null} />
    );
};

export default AddShiftPage;