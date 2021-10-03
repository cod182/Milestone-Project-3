const newReview = document.getElementById('new-review-icon');
let rating = document.getElementsByClassName('review-rating');
const currentLink = document.getElementById('profile-link');
const currentNestedLink = document.getElementById('profile-new-rev-link');

// When windows loads give the settings icon a blue glow
window.onload = function () {
  newReview.classList.add('glow');
  currentLink.classList.add('selected');
  currentNestedLink.classList.add('selectedNested');
};

// Adds the selected class to the New Review Link in Nav dropdown
function selectNewRev() {
  for (let i = 0; i < newRevLink.length; i++) {
    newRevLink[i].classList.add('selected');
  }
};

// Adds the selected class to the profile link in nav
function selectProfile() {
  for (let x = 0; x < profileLink.length; x++) {
    profileLink[x].classList.add('selected');
  }
};