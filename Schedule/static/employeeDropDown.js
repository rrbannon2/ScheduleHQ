document.addEventListener('DOMContentLoaded', getEmployees());

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

function getEmployees(){
    fetch('/loadEmployeeListData', {
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
        
        addEmpToDropdown(data);
        
        // Perform actions based on the response
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        // Handle errors here
    });
};

function addEmpToDropdown(employeesJson){
    var dropDownList = document.getElementById("myDropdown");
    for (let emp of employeesJson){
        var empOne = document.createElement("a");
        
        empOne.text = emp[0].concat(" ").concat(emp[1]);
        empOne.id = emp[2];
        empOne.setAttribute('onclick','empSelect(this.id)');
        dropDownList.appendChild(empOne);
    };
    
    
    
};

function empSelect(selectedEmp){
    window.location.href = '/selectEmpToEdit?'+ new URLSearchParams({employee: selectedEmp}); 
};