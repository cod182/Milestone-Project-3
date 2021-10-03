const currentLink = document.getElementById('profile-link');
const currentAdminLink = document.getElementById('manage-reviews-icon');
const adminSelect = document.getElementById('admin-icon');
let rating = document.getElementsByClassName('review-rating');


// When windows loads give the admin icon a blue glow
window.onload = function(){
  currentAdminLink.classList.add('glow--red');
  adminSelect.classList.add('glow--red');
  currentLink.classList.add('selected');
};

// Changes the review rating number to a star
for (var i = 0; i < rating.length; i++) {
  if(rating[i].textContent == 1) {
    rating[i].innerHTML = `
    <i class="fa fa-star"></i>
  `;
  } else if(rating[i].textContent == 2) {
    rating[i].innerHTML = `
    <i class="fa fa-star"></i>
    <i class="fa fa-star"></i>
  `;
  } else if(rating[i].textContent == 3) {
    rating[i].innerHTML = `
    <i class="fa fa-star"></i>
    <i class="fa fa-star"></i>
    <i class="fa fa-star"></i>
  `;
  } else if(rating[i].textContent == 4) {
    rating[i].innerHTML = `
    <i class="fa fa-star"></i>
    <i class="fa fa-star"></i>
    <i class="fa fa-star"></i>
    <i class="fa fa-star"></i>
  `;
  } else if(rating[i].textContent == 5) {
    rating[i].innerHTML = `
    <i class="fa fa-star"></i>
    <i class="fa fa-star"></i>
    <i class="fa fa-star"></i>
    <i class="fa fa-star"></i>
    <i class="fa fa-star"></i>
  `;
  } 
}