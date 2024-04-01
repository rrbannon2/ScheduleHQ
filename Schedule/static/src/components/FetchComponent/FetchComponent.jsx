
export default function FetchComponent(basicJsonDict, whichMethod, where) {
    
    fetch(where, {
        method: whichMethod,
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(basicJsonDict),
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
}