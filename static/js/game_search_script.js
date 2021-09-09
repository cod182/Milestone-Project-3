const newReview = document.getElementById('new-review-icon');
let rating = document.getElementsByClassName('review-rating');

// When windows loads give the settings icon a blue glow
window.onload = function(){
  newReview.classList.add('glow');
};