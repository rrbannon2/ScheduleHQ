import { Navigate } from 'react-router-dom';
var tokenVal = null;

export default function FetchComponent(inputData, whichMethod, where, searchParamName) {
    return new Promise((resolve, reject) => {
        if (whichMethod === "GET") {
            var searchURL = searchParamName ? "?" + new URLSearchParams(searchParamName + "=" + inputData["dataID"]+"&"+"token=" + tokenVal) : "?" + new URLSearchParams("token=" + tokenVal);
        
            fetch(where + searchURL, {
                method: whichMethod,
                headers: {
                    'Content-Type': 'application/json',
                },
            })
                .then(response => {
                    if (!response.ok) {
                        alert(response.statusText + " Please return to the log in page");
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                
                })
                .then(data => {
                    resolve(data);
                    if (data['token']) {
                        tokenVal = data['token'];
                    };
                    
                })
                .catch(error => {
                    console.error("There was a problem with the fetch operation GET:", error);
                    reject(error);
                });
        }
        else {

            if (where == '/login' || where == '/updateBusinessInfo') {
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
                        if (data['token']) {
                            tokenVal = data['token'];
                        };
                            
                    })
                    .catch(error => {
                        console.error('There was a problem with the fetch operation:', error);
                    });
            } else {
                var searchURL2 = new URLSearchParams("token=" + tokenVal);
                // alert(where);
                // inputData["token"]
                fetch(where +"?" + searchURL2, {
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
                        if (data['token']) {
                            tokenVal = data['token'];
                        };
                        
                    
                    })
                    .catch(error => {
                        console.error('There was a problem with the fetch operation:', error);
                    });
            };
        };
    });
    }