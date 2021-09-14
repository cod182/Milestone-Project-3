const currentLink = document.getElementById('home-link');

// When windows loads give the page link an underline
window.onload = function(){
  currentLink.classList.add('selected');
};

/* Set the width of the side navigation to 250px */
function openNav() {
  document.getElementById("mySidenav").style.width = "250px";
};
  
/* Set the width of the side navigation to 0 */
function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
};

function goBack() {
  window.history.back();
}