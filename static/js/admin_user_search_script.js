const currentLink = document.getElementById('profile-link');
const currentAdminLink = document.getElementById('manage-users-icon');
const adminSelect = document.getElementById('admin-icon');


// When windows loads give the admin icon a blue glow
window.onload = function(){
  currentAdminLink.classList.add('glow--red');
  adminSelect.classList.add('glow--red');
  currentLink.classList.add('selected');
};