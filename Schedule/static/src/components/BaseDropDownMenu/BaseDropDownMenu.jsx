import React, { useState, useEffect } from 'react';
import { Dropdown } from 'react-bootstrap';
import FetchComponent from '../FetchComponent/FetchComponent';
import '../BaseEmployeeDataTable/BaseEmployeeDataTable.css';

const BaseDropDownMenu = ({ URL }) => {
    const [fetchedInfo, setFetchedInfo] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await FetchComponent(null, "GET", URL, false);
                setFetchedInfo(data);
                console.log(data);
            } catch (error) {
                console.error("Error fetching shift data", error);
                // Handle the error accordingly
            }
        };

        fetchData();
    }, [URL]);

    return (
        fetchedInfo &&
        <Dropdown>
            
        <Dropdown.Toggle variant="success" id="dropdown-basic">
            Dropdown Button
        </Dropdown.Toggle>

        <Dropdown.Menu>
                {fetchedInfo.map((value, key) => {
                    return (
                        <Dropdown.Item>{value[0]} {value[1]}</Dropdown.Item>
                    );
                })}
        </Dropdown.Menu>
        </Dropdown>
    );
};
export default BaseDropDownMenu;