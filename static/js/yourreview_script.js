const yourreviewicon = document.getElementById('your-reviews-icon');
let rating = document.getElementsByClassName('review-rating');
let starRating = document.getElementsByClassName('review-star-rating');

// When windows loads give the settings icon a blue glow
window.onload = function(){
  yourreviewicon.classList.add('glow');
  
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