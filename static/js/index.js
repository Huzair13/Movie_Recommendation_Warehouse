var wait = document.getElementById("wait");
var main = document.getElementById("main");
var icon =document.getElementById("loading-icon");
var textload=document.getElementById("loading-message");

setTimeout(function() {
    document.getElementById("loading-message").innerHTML = "Hey !!! Its Almost there... ";
  }, 10000); 

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
        if(response.status.statusMessage=="novalue"){
          console.log("Function called");
          newusers(username);
        }else{
          getmoviedata(response.data,username)
        }
      }
    };
    xhr.send(JSON.stringify({
      "username":username
    }));
  }
  // else if(this.status==400){
  //   pred_random(username)
  // }

//   function pred_random(){
//       var xhr = new XMLHttpRequest();
//       xhr.open("POST", "http://localhost:5000/api/pred_rat");
//       xhr.setRequestHeader("Content-Type", "application/json");
//       xhr.onreadystatechange = function() {
//         if (this.readyState == 4 && this.status == 200) {
//           var response = JSON.parse(xhr.responseText);
//           console.log(response);
//           getmoviedata(response.data,username)
//       };
//       xhr.send(JSON.stringify({
//         "username":"Vijay"
//       }));
//   }
// }


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
            alert("rated");
        }
    }
            
    };
    xhr.send(JSON.stringify({
      "name":username,
       "id":id,
       "rating": rating
    }));
}

function newusers(username){
  const movieHeader = document.getElementById("movie-header");
  movieHeader.innerHTML = `Welcome ${username}, Here some of the random recommendations for you as you a new user,
   To get recommendation based on your likes please rate the movies and Refresh. If any issues login again`;
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://localhost:5000/api/random");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        var response = JSON.parse(xhr.responseText);
        console.log(response);
        getmoviedata(response.data,username);
      }
    };
    xhr.send(JSON.stringify({
      "username":username
    }));
}


document.querySelector('#logout').addEventListener('click', function(event) {
  var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://localhost:5000/api/logout");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        alert("you are logged out")
      }
    };
});
