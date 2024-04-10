import React, { useState, useEffect } from 'react';
import BaseEmployeeDataTable from '../BaseEmployeeDataTable/BaseEmployeeDataTable';
import FetchComponent from '../FetchComponent/FetchComponent';

const EditEmployeeDataTable = ( dataID ) => {
    const [empInfo, setEmpInfo] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await FetchComponent(dataID, "GET", "/loadEmployeeInfo","employee");
                setEmpInfo(data[0]);
            } catch (error) {
                console.error("Error fetching employee data", error);
                // Handle the error accordingly
            }
        };

        fetchData();
    }, [dataID]);

    // Render component only when empInfo is available
    return (
        empInfo && <BaseEmployeeDataTable addEmployee={false} employeeInfo={empInfo} />
    );
};

export default EditEmployeeDataTable;