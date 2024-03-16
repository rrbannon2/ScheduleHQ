function goToHome() {
    window.location.href = '/';
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
    fetch('/addShift', {
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
        console.log(data);
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        // Handle errors here
    });    
};



