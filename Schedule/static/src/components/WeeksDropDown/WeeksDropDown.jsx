import React, { useState, useEffect } from 'react';
import { Dropdown } from 'react-bootstrap';
import FetchComponent from '../FetchComponent/FetchComponent';
import '../BaseEmployeeDataTable/BaseEmployeeDataTable.css';
import { Link } from 'react-router-dom';
import DisplaySchedulePage from '../DisplaySchedule/DisplaySchedulePage';

export const BaseDropDownMenu = ({ dropDownPlaceholderVal, dataToMap }) => {

    return (
        dataToMap &&
        <Dropdown>
            
        <Dropdown.Toggle variant="success" id="dropdown-basic">
            {dropDownPlaceholderVal}
        </Dropdown.Toggle>

        <Dropdown.Menu>
                {dataToMap.map((value) => {
                    return (
                        <Dropdown.Item key={value.key} >{value.displayVal}</Dropdown.Item>
                    );
                })}
        </Dropdown.Menu>
        </Dropdown>
    );
};

export const WeeksDropDown = ({ datesInfo }) => {
    // let weekEndingVals = createDropDownListVals({ curWeekEndingDate });
    // console.log(weekEndingVals);



    return (
        <Dropdown>
            
        <Dropdown.Toggle  id="dropdown-basic">
            Week Ending {datesInfo[2]}
        </Dropdown.Toggle>
        <Dropdown.Menu>
        {datesInfo.map((value) => {
                return (
                    <Dropdown.Item key={value}>
                        <Link to="/home" state={value}>
                            Week Ending {value}
                        </Link>

                    </Dropdown.Item>
                );
            })}
        </Dropdown.Menu>
        </Dropdown>
    );
};
