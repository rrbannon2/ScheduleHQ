import React from 'react';
import BaseEmployeeDataTable from '../BaseEmployeeDataTable/BaseEmployeeDataTable';
import FetchComponent from '../FetchComponent/FetchComponent';

const EditEmployeeDataTable = (employeeName) => {
    FetchComponent(employeeName,"GET","/loadEmployeeInfo")
    return (
        <BaseEmployeeDataTable addEmployee={false}/>
    );
};

export default EditEmployeeDataTable;