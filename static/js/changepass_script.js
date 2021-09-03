const settingsSelect = document.getElementById('settings-icon');

// When windows loads give the settings icon a blue glow
window.onload = function(){
  settingsSelect.classList.add('glow');
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