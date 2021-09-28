const settingsSelect = document.getElementById('settings-icon');
const currentLink = document.getElementById('profile-link');
const currentNestedLink = document.getElementById('profile-settings-link')

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
    alert("\nPassword did not match: Please try again...")
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