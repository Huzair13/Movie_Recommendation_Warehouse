document.addEventListener("DOMContentLoaded", function() {
    const inputs = document.querySelectorAll(".textbox input");
    const progressBar = document.querySelector(".progress-bar");
    const progressContainer = document.querySelector(".progress-container");
  
    var button = document.getElementById("Signin");
  
    button.addEventListener("click", function(){
      var usernameInput = document.getElementById("username");
      var passwordInput = document.getElementById("password");
  
      var username = usernameInput.value;
      var password = passwordInput.value;
  
      if (username.length === 0) {
        showSnackbar("Username Can't be empty");
      }
      else if(password.length === 0){
        showSnackbar("password can't be empty");
      }else{
        let width = 0;
        let intervalId = setInterval(function() {
          if (width >= 100) {
            clearInterval(intervalId);
          } else {
            width++;
            progressBar.style.width = width + "%";
          }
        }, 10);
        var xhr = new XMLHttpRequest();
        xhr.open("POST","http://localhost:5000/api/signin");
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                progressContainer.style.display = "none";
                var response = JSON.parse(xhr.responseText);
                if(response.statusCode==200){
                    window.location.href  = `/index?username=${encodeURIComponent(username)}`;
                }
                else{
                  alert(response.statusMessage);
                }
            }
            
        };
        xhr.send(JSON.stringify({
            "name":username,
            "password": password
          }));
      }
  
      
    });
  
  
    function addClass() {
      let parent = this.parentNode.parentNode;
      parent.classList.add("focus");
    }
  
    function removeClass() {
      let parent = this.parentNode.parentNode;
      if (this.value == "") {
        parent.classList.remove("focus");
      }
    }
  
    function showSnackbar(message) {
      var snackbar = document.getElementById("snackbar");
      snackbar.innerText = message;
      snackbar.classList.add("show");
      setTimeout(function(){ snackbar.classList.remove("show"); }, 3000);
    }
  
    inputs.forEach((input) => {
      input.addEventListener("focus", addClass);
      input.addEventListener("blur", removeClass);
    })
  });
  