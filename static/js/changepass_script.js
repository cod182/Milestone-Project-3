const settingsSelect = document.getElementById('settings-icon');
const hideLG = document.getElementById('latest-games-visability-btn')
const latestGamesCont = document.getElementById('latest-games-container');
const currentLink = document.getElementById('profile-link');
const currentNestedLink = document.getElementById('profile-settings-link')

// When windows loads give the settings icon a blue glow
window.onload = function(){
  settingsSelect.classList.add('glow');
  currentLink.classList.add('selected');
  currentNestedLink.classList.add('selected');
};

//Check passwords match on submit
function passwordMatchCheck(form) {
  password = form.password.value;
  passwordConfirm = form.passwordConfirm.value;

  if (password != passwordConfirm) {
    alert("\nPassword did not match: Please try again...")
    return false;
  } else {
    return true;
  }
}

// Adds the selected class to the settings Link in Nav dropdown
function selectSettings() {
  for (let i = 0; i < settingsLink.length; i++) {
    settingsLink[i].classList.add('selected');
  }
}

// Adds the selected class to the profile link in nav
function selectProfile() {
  for (let x = 0; x < profileLink.length; x++) {
    profileLink[x].classList.add('selected');
  }
}

// hides the latest games container then creates the show latest games button
hideLG.addEventListener('click', function () {
  latestGamesCont.classList.add('hide');
  let btn = createShowLatestGamesBtn();
  let parent = document.getElementById('latest-games-container').parentNode;
  let container = document.getElementById('latest-games-container');
  parent.insertBefore(btn, container);
});

// Ceates the show latest game sbutton
function createShowLatestGamesBtn() {
  let LGCont = makeDivTwoClass("container-fluid", "lg-btn-container");
  LGCont.setAttribute('id', 'latest-games-btn-cont')

  let LGContRow = makeDivOneClass("row");
  LGCont.appendChild(LGContRow);

  let LGContCol = makeDivOneClass("Col-12");
  LGContRow.appendChild(LGContCol);

  let btn = document.createElement('button');
  btn.classList.add('btn');
  btn.classList.add('btn-open');
  btn.setAttribute('id', 'latest-open-btn')
  btn.setAttribute('onclick', 'showLatestGames()')

  btn.textContent = 'Show Latest Games';
  LGContCol.appendChild(btn);

  return LGCont
}

// unhides the latest games div and remove the latest games button container
function showLatestGames(){
  document.getElementById('latest-games-btn-cont').remove();
  latestGamesCont.classList.remove('hide');
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