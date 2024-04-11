import React, { useState, useEffect } from 'react';
import BusinessInfoPage from './BusinessInfo';
import FetchComponent from '../FetchComponent/FetchComponent';

const UpdateBusinessInfo = () => {
    const [fetchedInfo, setFetchedInfo] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await FetchComponent(null, "GET", "/loadBusinessInfo",false);
                setFetchedInfo(data[0]);
            } catch (error) {
                console.error("Error fetching shift data", error);
                // Handle the error accordingly
            }
        };

        fetchData();
    }, []);

    // Render component only when empInfo is available
    return (
        fetchedInfo && <BusinessInfoPage addNew={false} existingInfo={fetchedInfo} />
    );
};

export default UpdateBusinessInfo;