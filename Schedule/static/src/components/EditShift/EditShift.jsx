import React, { useState, useEffect } from 'react';
import ShiftPage from '../ShiftPage/ShiftPage';
import FetchComponent from '../FetchComponent/FetchComponent';

const EditShiftPage = (dataID) => {
    console.log(dataID);
    const [fetchedInfo, setFetchedInfo] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await FetchComponent(dataID, "GET", "/loadShiftInfo","shift");
                setFetchedInfo(data[0]);
            } catch (error) {
                console.error("Error fetching shift data", error);
                // Handle the error accordingly
            }
        };

        fetchData();
    }, [dataID]);

    // Render component only when empInfo is available
    return (
        fetchedInfo && <ShiftPage addNew={false} existingInfo={fetchedInfo} />
    );
};

export default EditShiftPage;