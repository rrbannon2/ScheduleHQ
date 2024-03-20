document.addEventListener('DOMContentLoaded', loadShiftInfo());
function goToHome() {
    window.location.href = '/';
};

function loadShiftInfo(){
    console.log(document.getElementById("shiftName").value);
    fetch('/loadShiftInfo?'+ new URLSearchParams({shift: document.getElementById("shiftName").value}), {
    method: 'GET',
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
        displayShiftData(data);
        
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        // Handle errors here
    });    
};

function displayShiftData(data) {
    console.log(data);
    var data = data[0];
    var timeArray;
    document.getElementById('shiftName').value = data[0];
    document.getElementById('importance').value = data[2];
    document.getElementById('maxHours').value = data[3];
    timeArray = data[1];
    timeCells = ['sunday_1', 'monday_1', 'tuesday_1', 'wednesday_1', 'thursday_1', 'friday_1',
        'saturday_1', 'sunday_2', 'monday_2', 'tuesday_2', 'wednesday_2', 'thursday_2', 'friday_2', 'saturday_2'];
    for (i in timeCells) {
        document.getElementById(timeCells[i]).value = timeArray[i];
    };
};
function submitFunction(){
    var shiftCells = ['shiftName','importance','maxHours','sunday_1','monday_1','tuesday_1','wednesday_1','thursday_1','friday_1','saturday_1','sunday_2','monday_2','tuesday_2','wednesday_2','thursday_2','friday_2','saturday_2'];
    var shiftJsonDict = {};
    for (let shiftCell of shiftCells) {
        cell = document.getElementById(shiftCell).value;
        if(cell != ''){
            shiftJsonDict[shiftCell] = cell;
        };
    };
    fetch('/updateShift', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(shiftJsonDict),
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