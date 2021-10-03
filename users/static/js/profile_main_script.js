const hideLatestGameBtn = document.getElementById('latest-games-visability-btn');
const latestGamesCont = document.getElementById('latest-games-container');
let latestGames = localStorage.getItem('latestGames');


//Checks if latest games is enabled in local storage
if (latestGames === 'hide') {
  hideLatestGames();
};

// hides the latest games container then creates the show latest games button
hideLatestGameBtn.addEventListener('click', function () {
  hideLatestGames();
});

function hideLatestGames() {
  latestGamesCont.classList.add('hide');
  let btn = createShowLatestGamesBtn();
  let parent = document.getElementById('latest-games-container').parentNode;
  let container = document.getElementById('latest-games-container');
  parent.insertBefore(btn, container);
  localStorage.setItem('latestGames', 'hide');
}

// Ceates the show latest game sbutton
function createShowLatestGamesBtn() {
  let latestGamesContainer = makeDivTwoClass("container-fluid", "lg-btn-container");
  latestGamesContainer.setAttribute('id', 'latest-games-btn-cont');

  let latestGamesContainerRow = makeDivOneClass("row");
  latestGamesContainer.appendChild(latestGamesContainerRow);

  let latestGamesContainerCol = makeDivOneClass("Col-12");
  latestGamesContainerRow.appendChild(latestGamesContainerCol);

  let btn = document.createElement('button');
  btn.classList.add('btn');
  btn.classList.add('btn-open');
  btn.setAttribute('id', 'latest-open-btn');
  btn.setAttribute('onclick', 'showLatestGames()');

  btn.textContent = 'Show Latest Games';
  latestGamesContainerCol.appendChild(btn);

  return latestGamesContainer;
}

// unhides the latest games div and remove the latest games button container
function showLatestGames() {
  document.getElementById('latest-games-btn-cont').remove();
  latestGamesCont.classList.remove('hide');
  localStorage.setItem('latestGames', null);

}

// Create and returns a div with 1 class
function makeDivOneClass(nameOfClass) {
  let div = document.createElement('div'); //Create a new div called div
  div.classList.add(nameOfClass); //Adds the class to the div
  return div; // returns the created div
};

// Create and returns a div with 2 classes
function makeDivTwoClass(nameOfClass, nameOfClassTwo) {
  let div = document.createElement('div'); //Create a new div called div
  div.classList.add(nameOfClass); //Adds the class to the div
  div.classList.add(nameOfClassTwo); //Adds the class to the div
  return div; // returns the created div
};

// Create and returns a div with 3 classes
function makeDivThreeClass(nameOfClass, nameOfClassTwo, nameOfClassThree) {
  let div = document.createElement('div'); //Create a new div called div
  div.classList.add(nameOfClass); //Adds the class to the div
  div.classList.add(nameOfClassTwo); //Adds the class to the div
  div.classList.add(nameOfClassThree); //Adds the class to the div
  return div; // returns the created div
};

function passwordMatchCheck(form) {
  password = form.password.value;
  passwordConfirm = form.passwordConfirm.value;

  if (password != passwordConfirm) {
    alert("\nPassword did not match: Please try again...");
    return false;
  } else {
    return true;
  }
}