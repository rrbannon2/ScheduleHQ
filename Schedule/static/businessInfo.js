document.addEventListener('DOMContentLoaded', loadBusinessInfo());

function goToHome() {
    window.location.href = '/';
};

function loadBusinessInfo() {
    fetch('/loadBusinessInfo', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
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
        displayBusData(data);
        
        
        // Perform actions based on the response
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        // Handle errors here
    });
};

function displayBusData(data) {
    var data = data[0];

    cells = ['name','avail','min_employees','min_managers','exempt_role','max_total_hours','max_hours_importance'];
    var availArray;
    for (i in cells) {
        if (i != 1) {
            document.getElementById(cells[i]).value = data[i];    
        };
        
    };
    timesArray = data[1];
    timesCells = ['sunday_1', 'monday_1', 'tuesday_1', 'wednesday_1', 'thursday_1', 'friday_1',
        'saturday_1', 'sunday_2', 'monday_2', 'tuesday_2', 'wednesday_2', 'thursday_2', 'friday_2', 'saturday_2']
    for (i in timesCells) {
        document.getElementById(timesCells[i]).value = timesArray[i];
    };
};

function submitBusinessInfo() {

    var basicInfoCells = ['name', 'min_employees', 'min_managers', 'exempt_role', 'max_total_hours', 'max_hours_importance',
        'sunday_1', 'monday_1', 'tuesday_1', 'wednesday_1', 'thursday_1', 'friday_1', 'saturday_1',
        'sunday_2', 'monday_2', 'tuesday_2', 'wednesday_2', 'thursday_2', 'friday_2', 'saturday_2'];
    
    var basicJsonDict = {};
   

    for (let basicCell of basicInfoCells) {
        cell = document.getElementById(basicCell).value;
        if(cell != ''){
            basicJsonDict[basicCell] = cell;
        };
    };

    fetch('/updateBusinessInfo', {
        method: 'POST',
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
};