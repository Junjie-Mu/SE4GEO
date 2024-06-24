
var login = document.getElementById("footer");

var openBtn = document.getElementById("open-btn");

var closeBtn = document.getElementById("close-btn");

openBtn.onclick = function() {
    login.style.display = "block";
}

closeBtn.onclick = function() {
    login.style.display = "none";
}


var register = document.getElementById("register");

var openRegister= document.getElementById("open-register");

var closeRegister = document.getElementById("close-register");

openRegister.onclick = function() {
    register.style.display = "block";
}

closeRegister.onclick = function() {
    register.style.display = "none";
}

var workflow = document.getElementById("workflow");

// Register function
document.getElementById('registerForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var formData = new FormData(this);
    fetch('/register', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        if (data.success) {
            register.style.display = "none";
        }
    })
    .catch(error => console.error('Error:', error));
});

// Login function
document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var formData = new FormData(this);
    fetch('/login', {  
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); 
        if (data.success) {
            login.style.display = "none";
            workflow.style.display = "inline";
            window.location.href = 'workflow.html';
        }
    })
    .catch(error => console.error('Error:', error));
});


document.getElementById('creat-user').addEventListener('click', function () {
    event.preventDefault();
    fetch('/createUser', {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('envForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var formData = new FormData(this);

    fetch('/updateEnv', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => console.error('Error:', error));
})

var testDbCon = document.getElementById("testDbConn");
testDbCon.onclick = function() {
    fetch('/testDb', {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => console.error('Error:', error));
};
