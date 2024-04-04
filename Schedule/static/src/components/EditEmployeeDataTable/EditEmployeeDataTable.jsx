import React from 'react';
import BaseEmployeeDataTable from '../BaseEmployeeDataTable/BaseEmployeeDataTable';
import FetchComponent from '../FetchComponent/FetchComponent';

const EditEmployeeDataTable = (employeeName) => {

    var empInfo = FetchComponent(employeeName, "GET", "/loadEmployeeInfo");
    console.log(empInfo);
    return (
        <BaseEmployeeDataTable addEmployee={false} employeeInfo={empInfo} />
    );
};

export default EditEmployeeDataTable;