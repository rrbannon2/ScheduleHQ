import React, { useState, useEffect } from 'react';
import SkillPage from '../SkillPage/SkillPage';
import FetchComponent from '../FetchComponent/FetchComponent';
import { useLocation } from 'react-router-dom';

const EditSkillPage = () => {

    const [fetchedInfo, setFetchedInfo] = useState(null);
    let dataID = { "dataID": useLocation().state };
    useEffect(() => {
        const fetchData = async () => {
            try {
                console.log("Testing in Edit Skill Page");
                const data = await FetchComponent(dataID, "GET", "/loadSkillInfo","skill");
                setFetchedInfo(data['body'][0]);
                console.log(data['body'][0]);
            } catch (error) {
                console.error("Error fetching skill data", error);
                // Handle the error accordingly
            }
        };

        fetchData();
    }, []);

    // Render component only when empInfo is available
    return (
        fetchedInfo && <SkillPage addNew={false} existingInfo={fetchedInfo} />
    );
};

export default EditSkillPage;