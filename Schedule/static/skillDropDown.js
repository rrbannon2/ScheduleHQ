document.addEventListener('DOMContentLoaded', getSkills());

function goToHome() {
    window.location.href = '/';
};

function goToPage(page){
    window.location.href = page; 
};

function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
};

function filterFunction() {
    var input, filter, ul, li, a, i;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    div = document.getElementById("myDropdown");
    a = div.getElementsByTagName("a");
    for (i = 0; i < a.length; i++) {
        txtValue = a[i].textContent || a[i].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
        a[i].style.display = "";
        } else {
        a[i].style.display = "none";
        }
    }
};

function getSkills(){
    fetch('/loadRequiredSkills', {
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
        addSkillToDropdown(data);
        
        // Perform actions based on the response
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        // Handle errors here
    });
};

function addSkillToDropdown(skillsJson){
    var dropDownList = document.getElementById("myDropdown");
    
    for (let skill of skillsJson){
        var skillOne = document.createElement("a");
        
        skillOne.text = skill;
        
        skillOne.setAttribute('onclick','skillSelect(this.text)');
        dropDownList.appendChild(skillOne);
    };
};

function skillSelect(selectedSkill){
    window.location.href = '/selectSkillToEdit?'+ new URLSearchParams({skill: selectedSkill}); 
    
};
