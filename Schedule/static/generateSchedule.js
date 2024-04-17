function goToHome(){
    window.location.href = '/';
};
var hasScheduleBeenGenerated = false;

function generateSchedule() {
    if (hasScheduleBeenGenerated === false) {
        fetch('/writeSchedule', {
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
                // Handle the response from the Flask server
                formatScheduleData(data);
                hasScheduleBeenGenerated = true;
                
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
                
            });
    };
};

function formatScheduleData(data) {
    
    var scheduleDict = {};
    for (i in data) {
        if (data[i] != "") {
            var block = data[i].split(":");
            console.log(block);
            var empName = block[0];
            var shiftTime = block[1];
            console.log(shiftTime);
            if (scheduleDict.hasOwnProperty(empName)) {
                scheduleDict[empName].push(shiftTime);
            }
            else {
                scheduleDict[empName] = [];
                scheduleDict[empName].push(shiftTime);
                // scheduleDict[empName].push("Off");
            };
        };
    };
    
    displayScheduleData(scheduleDict);
};

function displayScheduleData(dataDict) {
    var scheduleTable = document.getElementById("scheduleDisplayTable");
    for (let i of Object.keys(dataDict).sort()) {
        var schedRow = document.createElement("tr");
        var empNameCell = document.createElement("td");
        var day0 = document.createElement("td");
        var day1 = document.createElement("td");
        var day2 = document.createElement("td");
        var day3 = document.createElement("td");
        var day4 = document.createElement("td");
        var day5 = document.createElement("td");
        var day6 = document.createElement("td");
        var empRow = dataDict[i];
        
        empNameCell.textContent = i;
        day0.textContent = empRow[0];
        day1.textContent = empRow[1];
        day2.textContent = empRow[2];
        day3.textContent = empRow[3];
        day4.textContent = empRow[4];
        day5.textContent = empRow[5];
        day6.textContent = empRow[6];
        scheduleTable.appendChild(schedRow);
        schedRow.appendChild(empNameCell);
        schedRow.appendChild(day0);
        schedRow.appendChild(day1);
        schedRow.appendChild(day2);
        schedRow.appendChild(day3);
        schedRow.appendChild(day4);
        schedRow.appendChild(day5);
        schedRow.appendChild(day6);

    };
};