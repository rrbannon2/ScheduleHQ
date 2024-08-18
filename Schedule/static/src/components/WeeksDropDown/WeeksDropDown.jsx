import React, { useState, useEffect } from 'react';
import { Dropdown, NavItem,Row } from 'react-bootstrap';
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
        <div style={{ "display": "flex","flex-direction": "row","justify-content": "center" , "align-items": "center"}} >
        <Link style={{ "text-decoration": "none","paddingRight":"5px"}} to="/home" state={datesInfo[2] + "-1"}>&lt; </Link>
        <Dropdown>
            
        <Dropdown.Toggle  id="dropdown-weeks">
            Schedule For Week Ending {datesInfo[2]}
        </Dropdown.Toggle>
        <Dropdown.Menu>
        {datesInfo.map((value) => {
                return (
                    <Dropdown.Item key={value}>
                        <Link style={{ "text-decoration": "none" }} to="/home" state={value}>
                            Week Ending {value}
                        </Link>

                    </Dropdown.Item>
                );
            })}
        </Dropdown.Menu>
            </Dropdown>
            <Link style={{ "text-decoration": "none","paddingLeft":"5px","paddingRight":"20px" }} to ="/home" state={datesInfo[2]+" 1"}> &gt;</Link>
        </div>

    );
};
