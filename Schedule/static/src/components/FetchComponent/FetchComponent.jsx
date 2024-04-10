
export default function FetchComponent(inputData, whichMethod, where, searchParamName) {
    return new Promise((resolve, reject) => {
        if (whichMethod === "GET") {
        
            // fetch(where + "?" + searchParam new URLSearchParams({ searchParamName: inputData["employeeName"] }), {
            // console.log(searchParam);
            fetch(where + "?" + new URLSearchParams(searchParamName+"="+inputData["dataID"]), {
                method: whichMethod,
                headers: {
                    'Content-Type': 'application/json',
                },
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                
                })
                .then(data => {
                    console.log(data[0]);
                    resolve(data);
                })
                .catch(error => {
                    reject(error);
                });
        }
        else {
            fetch(where, {
                method: whichMethod,
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(inputData),
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
            
                    return response.json();
            
                })
                .then(data => {
                    // Handle the response from the Flask server
                    console.log(data);
                    // Perform actions based on the response
                })
                .catch(error => {
                    console.error('There was a problem with the fetch operation:', error);
                    // Handle errors here
                });
        };
    });
    }