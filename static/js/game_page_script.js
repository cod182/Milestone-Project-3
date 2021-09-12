const yourreviewicon = document.getElementById('your-reviews-icon');
let rating = document.getElementsByClassName('review-rating');
const descriptionHolder = document.getElementById('description-holder');
const descriptionArea = document.getElementById('game-description');

// Takes the styles inner text od descriptionHolder and puts in in the innerhtml of descriptionArea
descriptionArea.innerHTML = descriptionHolder.innerText

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