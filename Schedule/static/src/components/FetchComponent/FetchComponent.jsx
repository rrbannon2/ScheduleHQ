import { Navigate } from 'react-router-dom';
export default function FetchComponent(inputData, whichMethod, where, searchParamName) {
    return new Promise((resolve, reject) => {
        if (whichMethod === "GET") {
            var searchURL = searchParamName ? "?" + new URLSearchParams(searchParamName + "=" + inputData["dataID"]) : "";
        
            fetch(where + searchURL, {
                method: whichMethod,
                headers: {
                    'Content-Type': 'application/json',
                },
            })
                .then(response => {
                    if (!response.ok) {
                        alert(response.statusText);
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                
                })
                .then(data => {
                    resolve(data);
                })
                .catch(error => {
                    console.error("There was a problem with the fetch operation GET:", error);
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
                    
                    resolve(data);
                    // console.log(data);
                    // alert(data['token']);
                    
                })
                .catch(error => {
                    console.error('There was a problem with the fetch operation:', error);
                });
        };
    });
    }