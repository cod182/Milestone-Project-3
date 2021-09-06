const starOne = document.getElementById('one');
const starTwo = document.getElementById('two');
const starThree = document.getElementById('three');
const starFour = document.getElementById('four');
const starFive = document.getElementById('five');
const ratingValue = document.getElementById('rating');

starOne.addEventListener('mouseover', function() {
  ratingValue.setAttribute('value', 1)
  oneStarGlow();
})

starTwo.addEventListener('mouseover', function() {
  ratingValue.setAttribute('value', 2)
  twoStarGlow();
})

starThree.addEventListener('mouseover', function() {
  ratingValue.setAttribute('value', 3)
  threeStarGlow();
})

starFour.addEventListener('mouseover', function() {
  ratingValue.setAttribute('value', 4)
  fourStarGlow();
})

starFive.addEventListener('mouseover', function() {
  ratingValue.setAttribute('value', 5)
  fiveStarGlow();
})


function oneStarGlow(){
  starOne.classList.add('gold');
  starTwo.classList.remove('gold');
  starThree.classList.remove('gold');
  starFour.classList.remove('gold');
  starFive.classList.remove('gold');
}

function twoStarGlow(){
  starOne.classList.add('gold');
  starTwo.classList.add('gold');
  starThree.classList.remove('gold');
  starFour.classList.remove('gold');
  starFive.classList.remove('gold');
}

function threeStarGlow(){
  starOne.classList.add('gold');
  starTwo.classList.add('gold');
  starThree.classList.add('gold');
  starFour.classList.remove('gold');
  starFive.classList.remove('gold');
}

function fourStarGlow(){
  starOne.classList.add('gold');
  starTwo.classList.add('gold');
  starThree.classList.add('gold');
  starFour.classList.add('gold');
  starFive.classList.remove('gold');
}

function fiveStarGlow(){
  starOne.classList.add('gold');
  starTwo.classList.add('gold');
  starThree.classList.add('gold');
  starFour.classList.add('gold');
  starFive.classList.add('gold');
}
