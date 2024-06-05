import React, { useState, useEffect } from 'react';
import BaseEmployeeDataTable from '../BaseEmployeeDataTable/BaseEmployeeDataTable';
import FetchComponent from '../FetchComponent/FetchComponent';
import { useLocation } from 'react-router-dom';

const EditEmployeeDataTable = ( ) => {
    const [empInfo, setEmpInfo] = useState(null);
    var dataID = { "dataID": useLocation().state };
    
    useEffect(() => {
        
        const fetchData = async () => {
            try {
                const data = await FetchComponent(dataID, "GET", "/loadEmployeeInfo","employee");
                setEmpInfo(data['body'][0]);
            } catch (error) {
                console.error("Error fetching employee data", error);
                // Handle the error accordingly
            }
        };

        fetchData();
    }, []);

    // Render component only when empInfo is available
    return (
        empInfo && <BaseEmployeeDataTable addEmployee={false} employeeInfo={empInfo} />
    );
};

export default EditEmployeeDataTable;