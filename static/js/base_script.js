let background = localStorage.getItem('background');


/* Set the width of the side navigation to 250px */
function openNav() {
  document.getElementById("mySidenav").style.width = "250px";
};
  
/* Set the width of the side navigation to 0 */
function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
};

// Goes back to previous page
function goBack() {
  window.history.back();
};

//Checks if background is on in local storage
if(background) {
  if(background === 'on') {
    addBackground();
  }
} else {
  addBackground();
};

// Adds the background image and saves on state to local storage
function addBackground() {
  document.body.style.background = 'url("https://images.saymedia-content.com/.image/c_limit%2Ccs_srgb%2Cq_auto:eco%2Cw_400/MTc0MDE0OTk4MzEyMzk2NjY3/asteroids-by-atari-classic-video-games-reviewed.webp")';
  localStorage.setItem('background', 'on');
};