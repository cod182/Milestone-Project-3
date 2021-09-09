const releaseYear = document.getElementById('release_year');

//Adds the current year to the max value on release_year on load
window.onload = function(){
  let year =  new Date().getFullYear(); //Gets the current year
  releaseYear.setAttribute('max', year); //puts the current year as the max value
};