let rating = document.getElementsByClassName('review-rating');
const descriptionHolder = document.getElementById('description-holder');
const descriptionArea = document.getElementById('game-description');
const currentLink = document.getElementById('games-link');

// When windows loads give the page link an underline
window.onload = function(){
  currentLink.classList.add('selected');
};

// Takes the styles inner text od descriptionHolder and puts in in the innerhtml of descriptionArea
descriptionArea.innerHTML = descriptionHolder.innerText;

// Changes the review rating number to a star
for (var i = 0; i < rating.length; i++) {
  switch(rating[i].innerText) {
    case '1':
      rating[i].innerHTML = `
        <i class="fa fa-star"></i>
      `;
      break;
    case '2':
      rating[i].innerHTML = `
        <i class="fa fa-star"></i>
        <i class="fa fa-star"></i>
      `;
      break;
    case '3':
      rating[i].innerHTML = `
        <i class="fa fa-star"></i>
        <i class="fa fa-star"></i>
        <i class="fa fa-star"></i>
      `;
      break;
    case '4':
      rating[i].innerHTML = `
        <i class="fa fa-star"></i>
        <i class="fa fa-star"></i>
        <i class="fa fa-star"></i>
        <i class="fa fa-star"></i>
      `;
      break;
    case '5':
      rating[i].innerHTML = `
        <i class="fa fa-star"></i>
        <i class="fa fa-star"></i>
        <i class="fa fa-star"></i>
        <i class="fa fa-star"></i>
        <i class="fa fa-star"></i>
      `;
    break;
  }
}