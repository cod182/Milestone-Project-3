const currentLink = document.getElementById('register-link');
const profileImages = document.getElementsByClassName('addSelectedAttribute');

// When windows loads give the page link an underline
window.onload = function(){
  currentLink.classList.add('selected');
};

// Checks the passwords match
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

function addSelectedAttribute(img) {
  img.classList.add('glow');
  img.setAttribute('name', 'profile_image');
  for (var i = 0; i > profileImages.length; i++) {
    profileImages[i].classList.remove('glow');
    profileImages[i].removeAttribute('name')
  }
}