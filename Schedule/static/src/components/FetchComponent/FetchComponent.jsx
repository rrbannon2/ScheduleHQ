import { Navigate } from 'react-router-dom';
var tokenVal = null;

export default function FetchComponent(inputData, whichMethod, where, searchParamName) {
    return new Promise((resolve, reject) => {
        if (whichMethod === "GET") {
            var searchURL = searchParamName ? "?" + new URLSearchParams(searchParamName + "=" + inputData["dataID"]) : "?" + new URLSearchParams("token=" + tokenVal);
        
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
                    tokenVal = data['token'];
                    console.log(tokenVal);
                })
                .catch(error => {
                    console.error("There was a problem with the fetch operation GET:", error);
                    reject(error);
                });
        }
        else {

            if (where == '/login') {
                fetch(where, {
                    // fetch(where,{
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
                        tokenVal = data['token'];
                        console.log(tokenVal);
                            
                    })
                    .catch(error => {
                        console.error('There was a problem with the fetch operation:', error);
                    });
            } else {
                var searchURL2 = where == '/login' ? new URLSearchParams("token" + tokenVal) : "";
                // alert(where);
                console.log(searchURL2);
                fetch(where + searchURL2, {
                    // fetch(where,{
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
                        tokenVal = data['token'];
                        console.log(tokenVal);
                    
                    })
                    .catch(error => {
                        console.error('There was a problem with the fetch operation:', error);
                    });
            };
        };
    });
    }