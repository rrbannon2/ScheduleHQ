document.addEventListener('DOMContentLoaded', getShifts());

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

function getShifts(){
    fetch('/loadShifts', {
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
        addShiftToDropdown(data);
        
        // Perform actions based on the response
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        // Handle errors here
    });
};

function addShiftToDropdown(shiftsJson){
    var dropDownList = document.getElementById("myDropdown");
    
    for (let shift of shiftsJson){
        var shiftOne = document.createElement("a");
        
        shiftOne.text = shift;
        
        shiftOne.setAttribute('onclick','shiftSelect(this.text)');
        dropDownList.appendChild(shiftOne);
    };
};

function shiftSelect(selectedShift){
    window.location.href = '/selectShiftToEdit?'+ new URLSearchParams({shift: selectedShift}); 
    
};
