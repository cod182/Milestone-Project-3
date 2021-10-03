const settingsSelect = document.getElementById('settings-icon');
const currentLink = document.getElementById('profile-link');
const currentNestedLink = document.getElementById('profile-settings-link');
const backgroundToggle = document.getElementById('background-toggle');



// When windows loads give the settings icon a blue glow
window.onload = function () {
  settingsSelect.classList.add('glow');
  currentLink.classList.add('selected');
  currentNestedLink.classList.add('selectedNested');
};

//Check passwords match on submit
function passwordMatchCheck(form) {
  password = form.password.value;
  passwordConfirm = form.passwordConfirm.value;

  if (password != passwordConfirm) {
    alert("\nPassword did not match: Please try again...");
    return false;
  } else {
    return true;
  }
}

// Adds the selected class to the settings Link in Nav dropdown
function selectSettings() {
  for (let i = 0; i < settingsLink.length; i++) {
    settingsLink[i].classList.add('selected');
  }
}

// Adds the selected class to the profile link in nav
function selectProfile() {
  for (let x = 0; x < profileLink.length; x++) {
    profileLink[x].classList.add('selected');
  }
}

//Checks if background is on in local storage
if(background === 'on') {
  addBackground();
  backgroundToggle.setAttribute('checked', '');
};

// Toggle for background image / solid color
backgroundToggle.addEventListener('click', () => { //listens for dark button clicked
  background = localStorage.getItem('background');
  if(background !== 'on') { //if body has a class
      addBackground(); // add classes
  } else {    // if body has no class
      removeBackground(); //remove classed
  }
});

// Adds the background image and saves on state to local storage
function addBackground() {
  document.body.style.background = 'url("https://images.saymedia-content.com/.image/c_limit%2Ccs_srgb%2Cq_auto:eco%2Cw_400/MTc0MDE0OTk4MzEyMzk2NjY3/asteroids-by-atari-classic-video-games-reviewed.webp")';
  localStorage.setItem('background', 'on');
}

// sets background to grey and saves off state background to local storage
// Also sets the back
function removeBackground() {
  document.body.style.background = '#444444';
  localStorage.setItem('background', 'off');
}