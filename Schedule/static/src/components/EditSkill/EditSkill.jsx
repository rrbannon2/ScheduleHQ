import React, { useState, useEffect } from 'react';
import SkillPage from '../SkillPage/SkillPage';
import FetchComponent from '../FetchComponent/FetchComponent';

const EditSkillPage = (dataID) => {
    console.log(dataID);
    const [fetchedInfo, setFetchedInfo] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await FetchComponent(dataID, "GET", "/loadSkillInfo","skill");
                setFetchedInfo(data[0]);
            } catch (error) {
                console.error("Error fetching skill data", error);
                // Handle the error accordingly
            }
        };

        fetchData();
    }, [dataID]);

    // Render component only when empInfo is available
    return (
        fetchedInfo && <SkillPage addNew={false} existingInfo={fetchedInfo} />
    );
};

export default EditSkillPage;