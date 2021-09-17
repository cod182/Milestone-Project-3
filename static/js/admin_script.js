const currentLink = document.getElementById('profile-link');
const adminSelect = document.getElementById('admin-icon');


// When windows loads give the admin icon a blue glow
window.onload = function(){
  adminSelect.classList.add('glow--red');
  currentLink.classList.add('selected');
};