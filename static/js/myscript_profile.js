const newReview = document.getElementById('new-review-btn');
const newReviewIcon = document.getElementById('new-review-icon');
const yourReviews = document.getElementById('your-reviews-btn');
const yourReviewsIcon = document.getElementById('your-reviews-icon');
const settings = document.getElementById('settings-btn');
const settingsIcon = document.getElementById('settings-icon');
const profileInfoCont = document.getElementById('profile-info-container');

newReview.addEventListener('click', function() {
  profileInfoCont.innerHTML = '';
  newReviewIcon.classList.add('glow');
  yourReviewsIcon.classList.remove('glow');
  settingsIcon.classList.remove('glow');
  makeGameSearchHTML();
});

function makeGameSearchHTML() {
  let body = [];
  let resultDiv = makeSearchContainer(body); //Creates the body div for the game search
  makeSearchTitle(body); // Creates the Title for the game search section
  makeSearchForm(body); // Create the form for the game search section
  let bodyReady = body.join('').toString(); // Joins all the arrays togather and pushes stores them in bodyReady variable
  
  resultDiv.innerHTML = bodyReady; //Puts resultReady HTML into the resultDiv innerHTML
  profileInfoCont.appendChild(resultDiv); //Appends resultDiv to resultContain, finalising the result on the page
};

function makeSearchContainer(body) {
  let resultDiv = document.createElement('div'); //Create a new div called resultDiv
  resultDiv.classList.add('col-12'); //Adds the class to the div
  resultDiv.classList.add('game-search'); //Adds the class to the div
  return resultDiv; // returns the created div
};

// added the Title HTML and pushes to body div
function makeSearchTitle(body){
  let info = `
    <div class="row">
      <div class="col-12">
        <h3>Search For A Game!</h3>
      </div>
    </div>
  `
  body.push(info);
};

// added the form HTML and pushes to body div
function makeSearchForm(body){
  let info = `
    <div class="row">
        <form action="">
            <div class="row">
                <div class="col-12">
                    <input type="text" name="name_of_game" placeholder="Name of Game" required>
                </div>
            </div>
            <div class="row">
                <div class="col-12">
                    <button type="submit" class="btn btn-green">Search</button>
                </div>
            </div>
        </form>
    </div>
  `
  body.push(info);
};


// Creates the Your Review section on the profiel Page
yourReviews.addEventListener('click', function() {
  profileInfoCont.innerHTML = '';
  yourReviewsIcon.classList.add('glow');
  newReviewIcon.classList.remove('glow');
  settingsIcon.classList.remove('glow');
  makeYourReviewsHTML();
});

function makeYourReviewsHTML() {
  let body = [];
  let resultDiv = makeSearchContainer(body); //Creates the body div for the game search
  makeReviewsTitle(body); // Creates the Title for the game search section
  makeReviews(body); // Create the form for the game search section
  let bodyReady = body.join('').toString(); // Joins all the arrays togather and pushes stores them in bodyReady variable
  
  resultDiv.innerHTML = bodyReady; //Puts resultReady HTML into the resultDiv innerHTML
  profileInfoCont.appendChild(resultDiv); //Appends resultDiv to resultContain, finalising the result on the page
};

function makeYourReviewsContainer(body) {
  let resultDiv = document.createElement('div'); //Create a new div called resultDiv
  resultDiv.classList.add('col-12'); //Adds the class to the div
  resultDiv.classList.add('profile-reviews'); //Adds the class to the div
  return resultDiv; // returns the created div
};

// added the Title HTML and pushes to body div
function makeReviewsTitle(body){
  let info = `
    <div class="row">
      <div class="col-12">
          <h3>Your Reviews</h3>
      </div>
    </div>
  `
  body.push(info);
};

// added the form HTML and pushes to body div
function makeReviews(body){
  let info = `
    <div class="row">
      <div class="col-10 your-reviews-container-block">
          <div class="your-review-container">
              <div class="row">
                  <div class="col-12 col-sm-2 col-md-3">
                      <button type="submit" class="btn btn-warning">Edit</button>
                  </div>

                  <div class="col-12 col-sm-3 col-md-5">
                      <p>####GAME NAME####</p>
                  </div>

                  <div class="col-12 col-sm-3 col-md-4">
                      <p>#####Rating####</p>
                  </div>
              </div>

          </div>
      </div>
    </div>
  `
  body.push(info);
};


// Creates the Your Review section on the profiel Page
settings.addEventListener('click', function() {
  profileInfoCont.innerHTML = '';
  settingsIcon.classList.add('glow');
  yourReviewsIcon.classList.remove('glow');
  newReviewIcon.classList.remove('glow');
  makeSettingsHTML();
});

function makeSettingsHTML() {
  let body = [];
  let resultDiv = makeSearchContainer(body); //Creates the body div for the game search
  makeSettingsTitle(body); // Creates the Title for the game search section
  makeSettingsBody(body); // Create the form for the game search section
  let bodyReady = body.join('').toString(); // Joins all the arrays togather and pushes stores them in bodyReady variable
  
  resultDiv.innerHTML = bodyReady; //Puts resultReady HTML into the resultDiv innerHTML
  profileInfoCont.appendChild(resultDiv); //Appends resultDiv to resultContain, finalising the result on the page
};

function makeSettingsContainer(body) {
  let resultDiv = document.createElement('div'); //Create a new div called resultDiv
  resultDiv.classList.add('col-12'); //Adds the class to the div
  resultDiv.classList.add('profile-settings'); //Adds the class to the div
  return resultDiv; // returns the created div
};

// added the Title HTML and pushes to body div
function makeSettingsTitle(body){
  let info = `
    <div class="row">
      <div class="col-12">
          <h3>Settings</h3>
      </div>
    </div>
  `
  body.push(info);
};

// added the form HTML and pushes to body div
function makeSettingsBody(body){
  let info = [];
  let form = `
    <div class="col-12">
      <h5>Change Password</h5>
      <form class="password-reset-form" action="">
          <div class="row">
              <div class="col-12">
                  <input class="pass-input" id="orig-pass" type="text" name="orig-pass" placeholder="Current Password" required>
              </div>
          </div>
  `
  info.push(form) // Pushes the form into info
  createNewPass(info); // Creates the new Pass part of the form
  let infoReady = info.join('').toString(); // Joins all the arrays together and stores them in infoReady variable
  body.push(infoReady); // Pushed the infoReady into body
};

function createNewPass(info){
  let newPass = `
    <div class="row">
              <div class="col-12">
                  <input class="pass-input" id="new-pass" type="text" name="new-pass" placeholder="New Password" required>
              </div>
          </div>

          <div class="row">
              <div class="col-12">
                  <input class="pass-input" id="new-pass-confirm" type="text" name="new-pass-confirm" placeholder="Confirm New Password" required>
              </div>
          </div>
          <div class="row">
              <div class="col-6 m-auto">
                  <button class="btn btn-green pass-submit" type="submit">Update</button>
              </div>
          </div>
      </form>
    </div>
  `
  info.push(newPass); // Pushes the new Pass part of form into info
}