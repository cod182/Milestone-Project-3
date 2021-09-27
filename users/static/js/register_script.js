const currentLink = document.getElementById('register-link');

// When windows loads give the page link an underline
window.onload = function () {
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