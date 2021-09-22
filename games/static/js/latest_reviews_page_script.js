const yourreviewicon = document.getElementById('your-reviews-icon');
let rating = document.getElementsByClassName('review-rating');
const currentLink = document.getElementById('latest-reviews-link');

// When windows loads give the page link an underline
window.onload = function(){
  currentLink.classList.add('selected');
};

// Changes the review rating number to a star
for (var i = 0; i < rating.length; i++) {
  if(rating[i].textContent == 1) {
    rating[i].innerHTML = `
    <i class="fa fa-star"></i>
  `
  } else if(rating[i].textContent == 2) {
    rating[i].innerHTML = `
    <i class="fa fa-star"></i>
    <i class="fa fa-star"></i>
  `
  } else if(rating[i].textContent == 3) {
    rating[i].innerHTML = `
    <i class="fa fa-star"></i>
    <i class="fa fa-star"></i>
    <i class="fa fa-star"></i>
  `
  } else if(rating[i].textContent == 4) {
    rating[i].innerHTML = `
    <i class="fa fa-star"></i>
    <i class="fa fa-star"></i>
    <i class="fa fa-star"></i>
    <i class="fa fa-star"></i>
  `
  } else if(rating[i].textContent == 5) {
    rating[i].innerHTML = `
    <i class="fa fa-star"></i>
    <i class="fa fa-star"></i>
    <i class="fa fa-star"></i>
    <i class="fa fa-star"></i>
    <i class="fa fa-star"></i>
  `
  } 
}