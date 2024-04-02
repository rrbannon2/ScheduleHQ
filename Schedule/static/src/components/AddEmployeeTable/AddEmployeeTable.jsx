import React from 'react';
import BaseEmployeeDataTable from '../BaseEmployeeDataTable/BaseEmployeeDataTable';

const AddEmployeeTable = () => {
    return (
        <BaseEmployeeDataTable addEmployee={true}/>
    );
};

export default AddEmployeeTable;