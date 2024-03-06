document.addEventListener('DOMContentLoaded', loadSkillInfo());
function goToHome() {
    window.location.href = '/';
};

function loadSkillInfo(){
    console.log(document.getElementById("skillName").value);
    fetch('/loadSkillInfo?'+ new URLSearchParams({skill: document.getElementById("skillName").value}), {
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
        displaySkillData(data);
        
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        // Handle errors here
    });    
};

function displaySkillData(data){
    var data = data[0];
    var timeArray;
    document.getElementById('skillName').value = data[0];
    document.getElementById('role').value = data[2];
    document.getElementById('importance').value = data[3];
    timeArray = data[1];
    timeCells = ['sunday_1', 'monday_1', 'tuesday_1', 'wednesday_1', 'thursday_1', 'friday_1',
        'saturday_1', 'sunday_2', 'monday_2', 'tuesday_2', 'wednesday_2', 'thursday_2', 'friday_2', 'saturday_2'];
    for (i in timeCells) {
        document.getElementById(timeCells[i]).value = timeArray[i];
    };
};
function submitFunction(){
    var skillCells = ['skillName','role','importance','sunday_1','monday_1','tuesday_1','wednesday_1','thursday_1','friday_1','saturday_1','sunday_2','monday_2','tuesday_2','wednesday_2','thursday_2','friday_2','saturday_2'];
    var skillJsonDict = {};
    for (let skillCell of skillCells) {
        cell = document.getElementById(skillCell).value;
        if(cell != ''){
            skillJsonDict[skillCell] = cell;
        };
    };
    fetch('/updateSkill', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(skillJsonDict),
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