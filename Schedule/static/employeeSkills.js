document.addEventListener('DOMContentLoaded', getSkillLevels());

function goToHome() {
    window.location.href = '/';
};

function addSkillToTable(skillsJson){
    var skillLevelsTbl = document.getElementById("skillLevelsTbl");
    
    for (let skill of skillsJson){
        var skillRow = document.createElement("tr");
        var skillOne = document.createElement("td");
        var lvlCell = document.createElement("td");
        var lvl = document.createElement("input");
        var buttonCell = document.createElement("td");
        var rowSubmitBtn = document.createElement("button");
        rowSubmitBtn.setAttribute("onclick", "rowSubmit(this.parentElement.parentElement.children)");
        rowSubmitBtn.textContent = "Update Skill Level";
        rowSubmitBtn.type = "button";
        skillOne.textContent = skill[0];
        lvl.setAttribute("value", skill[1]);
        lvl.setAttribute("id", skill[0]);
        
        skillLevelsTbl.appendChild(skillRow);
        skillRow.appendChild(skillOne);
        skillRow.appendChild(lvlCell);
        lvlCell.appendChild(lvl);
        skillRow.appendChild(buttonCell);
        buttonCell.appendChild(rowSubmitBtn);
        
    };
};
function rowSubmit(row) {
    skillName = row[0].textContent;
    skillLvl = document.getElementById(skillName).value;
    jsonDict = {};
    jsonDict['skill'] = skillName;
    jsonDict['skill_level'] = skillLvl;
    jsonDict['id'] = document.getElementById('id_1').value;
    console.log(jsonDict);

    fetch('/updateSkillLevel', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(jsonDict),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        return response.json();
        
    })
    .then(data => {
        // Handle the response from the Flask server
        alert(data)
        // Perform actions based on the response
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        // Handle errors here
    });
};

function getSkillLevels() {
    fetch('/loadSkillLevels?' + new URLSearchParams({employee: document.getElementById("id_1").value}), {
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
        addSkillToTable(data);
        
        // Perform actions based on the response
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        // Handle errors here
    });
};