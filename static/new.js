document.addEventListener("DOMContentLoaded", function(event) {
  var welcomeMessage = document.getElementById("welcome-message");
  
  // Hide other elements on the page
  document.body.classList.add("no-scroll");
  
  // Fade in welcome message
  welcomeMessage.classList.add("show");
  
  // Fade out welcome message after 3 seconds
  setTimeout(function() {
    welcomeMessage.classList.remove("show");
    
    // Load additional content after fade out
    setTimeout(function() {
      // Your code to load additional content goes here
      
      // Show other elements on the page
      document.body.classList.remove("no-scroll");
      var hiddenElements = document.querySelectorAll("#welcome-message.show ~ *");
      hiddenElements.forEach(function(element) {
        element.style.opacity = "";
        element.style.pointerEvents = "";
      });
    }, 1000); // Wait 1 second after fade out is complete before loading content
  }, 3000); // Wait 3 seconds before fading out welcome message
});


function prediction() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const username = urlParams.get("username");
    console.log(username);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://localhost:5000/api/pred_rat");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        var response = JSON.parse(xhr.responseText);
        console.log(response);
        getmoviedata(response.data,username)
      }
    };
    xhr.send(JSON.stringify({
      "username":username
    }));
  }

  async function getmoviedata(response,username){

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://localhost:5000/api/getdata");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var response = JSON.parse(xhr.responseText); // Access the movie objects by accessing the "movies" key
            movies = response.movies; 
            console.log(movies)// Access the movie objects by accessing the "movies" key
            generateCards(movies,username)
        }
    };
    xhr.send(JSON.stringify(response));
  
  }    


  function generateCards(movies,username) {

    let cardList = "";
    for (let i = 0; i < movies.length; i++) {
    
      const imdbId = movies[i][0].imdb_id; // replace with the IMDb ID of the movie
      const apiKey = "8134811032100258ec27af24089d17a1"; // replace with your TMDB API key
    
    
      const url = `https://api.themoviedb.org/3/find/${imdbId}?api_key=${apiKey}&language=en-US&external_source=imdb_id`;
    
      fetch(url)
        .then(response => response.json())
        .then(data => {
          const poster = data.movie_results[0].poster_path;
          if (movies[i] && movies[i][0]) {
            movies[i][0].poster_path = poster;
          }
          console.log(movies[i][0].poster_path)
          const baseUrl = "https://image.tmdb.org/t/p/w300/";
          const urlParameter = movies[i][0].poster_path;
          imageUrl = baseUrl + urlParameter;
          console.log(imageUrl);
          
          
          cardList += `
          <div class="card">
          <div class="card-thumbnail">
            <img src=${imageUrl} alt="">
          </div>
          <div class="card-body">
            <span class="card-title">${movies[i][0].original_title}</span>
            <p>
              <span>Movie ID : </span>
              <span>${movies[i][0].id}</span><br>
              <span>Date : ${movies[i][0].release_date}</span><br> 
              <span>Genres :${movies[i][0].genres}</span>
            </p>
            <p class="card-description">${movies[i][0].overview}</p>
            <a href="#">Watched Already ?? </br> Rate below</a>
            <div class="stars">
            <i class="fa fa-star"></i>
            <i class="fa fa-star"></i>
            <i class="fa fa-star"></i>
            <i class="fa fa-star"></i>
            <i class="fa fa-star"></i>
          </div>
          </div>
        </div>`;
    
          document.getElementById("cardList").innerHTML = cardList;
          wait.style.display = "none";
          icon.style.display="none";
          main.style.display = "block";
    
          const cards = document.querySelectorAll(".card");
    
          cards.forEach(card => {
            const stars = card.querySelectorAll(".stars i");
            let rating = 0;
    
            stars.forEach((star, index) => {
              star.addEventListener("click", () => {
                rating = index + 1;
                for (let i = 0; i <= index; i++) {
                  if (i <= index) {
                    stars[i].classList.add("active");
                  } else {
                    stars[i].classList.remove("active");
                  }
                }
                const movieID = card.querySelector(".card-body p span:nth-of-type(2)").textContent;
                console.log(`Rating for ${movieID}: ${rating}`);
                InsertRating(movieID,rating,username);
    
              });
            });
          });
        })
        
        .catch(error => {
          console.error(error);
        });
    }
    }
    window.onload = prediction;
    
    function InsertRating(id,rating,username){
      console.log(username+"dahjisdifasifsagfgg");
      console.log(id);
      console.log(rating);
        var xhr = new XMLHttpRequest();
        xhr.open("POST","http://localhost:5000/api/update-users");
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var response = JSON.parse(xhr.responseText);
            if(response.statusCode==200){
                // window.location.href  = `/?username=${encodeURIComponent(username)}`;
                console.log("success");
            }
            else{
                alert(response.statusMessage);
            }
        }
                
        };
        xhr.send(JSON.stringify({
          "name":username,
           "id":id,
           "rating": rating
        }));
    }
    