const currentLink = document.getElementById('profile-link');
const currentNestedLink = document.getElementById('profile-home-link');

// When windows loads give the settings icon a blue glow
window.onload = function () {
  currentLink.classList.add('selected');
  currentNestedLink.classList.add('selectedNested');
};