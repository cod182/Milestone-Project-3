const yourreviewicon = document.getElementById('your-reviews-icon');
let rating = document.getElementsByClassName('review-rating');
const currentLink = document.getElementById('profile-link');
const currentNestedLink = document.getElementById('profile-your-revs-link')

// When windows loads give the settings icon a blue glow
window.onload = function () {
  yourreviewicon.classList.add('glow');
  currentLink.classList.add('selected');
  currentNestedLink.classList.add('selected');
};

// Changes the review rating number to a star
for (var i = 0; i < rating.length; i++) {
  switch (rating[i].innerText) {
    case '1':
      rating[i].innerHTML = `
        <i class="fa fa-star"></i>
      `
      break;
    case '2':
      rating[i].innerHTML = `
        <i class="fa fa-star"></i>
        <i class="fa fa-star"></i>
      `
      break;
    case '3':
      rating[i].innerHTML = `
        <i class="fa fa-star"></i>
        <i class="fa fa-star"></i>
        <i class="fa fa-star"></i>
      `
      break;
    case '4':
      rating[i].innerHTML = `
        <i class="fa fa-star"></i>
        <i class="fa fa-star"></i>
        <i class="fa fa-star"></i>
        <i class="fa fa-star"></i>
      `
      break;
    case '5':
      rating[i].innerHTML = `
        <i class="fa fa-star"></i>
        <i class="fa fa-star"></i>
        <i class="fa fa-star"></i>
        <i class="fa fa-star"></i>
        <i class="fa fa-star"></i>
      `
      break;
    default:
      "No Rating"
  }
}