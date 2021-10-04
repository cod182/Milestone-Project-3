# Milestone-Project-3

## 

## Project

The purpose of this site will be to allow users to add their review for a recently played game. If the game does not exist in the archive, a user would be able to add the game to the archive. Users would also be able to search for a game to read reviews on it. A link will be available to users to purchase the game from an affiliate site.

# Showcase

A deployed link to the site can be found on Heroku[here](https://mp3-game-corner.herokuapp.com/)

![Preivew](static/images/responsive.png)


# UX

## User Story

- The end user for the site is someone who is interesed in video games and wants:
    - Find reviews on a game
    - Leave a review for a game
- The user may also want to discover games by looking a highly rated reviews
- The user may wish to purchase the game after reading reviews and a link will be available.
- The site's main access will be on mobile, as users will generally access the site when on the move as reading material.
- The end user will want to be able to easily find the game that they are interested in and either quicky read a review or post their own. Information will need to be easily accessible and clear.

## Strategy

### User Needs

- The user needs the site to be fully functionaly on a mobile device as it will be on a tablet or desktop.
- Information must be easy to access, clearly displayed and easy to digest.
- Easily understand how the site works. Access to a profile page to leave a review will need to be simple.
- Be able to search for a game quickly and concisely.
- Be able to find where to purchase the game if they like the reviews.

### Technical Capabilities

It is possible to create this site efficiently using the bootstrap framework and HTML/CSS/Javascript/Python that I have learned along with knowledge of the a mongodb database. Apis will also be used for getting extra information on the game, such as videos

### Business Vision

To create a community for like minded individuals who enjoy gaming, providing a useful resource. Simplicity of the site will be 
Simplicit and speed at the forefront so the user is not delayed in their search.
Afilliate links will be available to purchase games to help with costs of the site.

## Scope

The site will quickly show what it's purpose is for a user. A search will be easy to complete by a user without loggin in.


The site will include an about section detailing what the site does and what a user can gain from it.
It will be easy to enact a search and read the results.

## Structure

- The site will be detailed but simply laid out, cover 15 pages in total with some pages generated when clicked on.
- The navigation bar will give access to the mainpages of the site
- Site pages - Login, Register, Latest Reviews, Games, Game,  Profile(If logged in)
- User will be able to search for a game from the navigation bar at the top of the page.
- Each user will have a profile page with access to adding games and reviews, changing their password and view all of their reviews
- An admin panel will be accesiable by admin users allowing reviews, games and users to be managed
- A contact us modal will be availabe on all pages

## Skeleton

### Wireframes
- Wireframes were created at the begining of the project and will be used to create the site as closly as possible
## Original

- [Mobile >576px](static/wireframes/SM.png)
- [Tablet ≥768px](static/wireframes/MD.png)
- [Desktop ≥1400px](static/wireframes/LG.png)

## Surface

The site will be set over multiple pages with the ability for users to add and remove infomation relating to games

### Home
- The page will be presented to the user showing the goals of the site.
- There will be a cached latest games section


### Register Page
- Available from the navigation menu
- A page for a user to enter their details to register to the site

### Login Page
- Available from the navigation menu
- Page for a registered user to login

### Profile Page

- Once a user has signed up, they will have access to their prescence on the site.
- Their reviews will be available along with the ability to add more.
- They will be able to search for a game and add it to the site if it does not exist.
- They will have quick access to the latest reviews

### Game search page from profile

- When the user wants to add a new review, they will need to search for the games first.
- If the game is not on the site, they will be able to run a search via the RAWG API

### New Game Page

- If a game is not currently on the site, the user will be able to add it from the API result
### New Review

- The user will be able to leave a review for the game they have selected, if logged in.
- Page is simple with only the information that is reqired for a review

### Games Page

- Will display all of the games listed on the site, paginated to 10 per page
- Will be searchable to show only the game(s) the user is looking for.
- Each game clickable to allow linking to the game's page

### Game Page

- Will show the individual game the user has clicked on.
- Will give detailed description of the game, overall rating and afilliate purchasing link.
- Will display 2 videos relating to the game from Youttube
- Will show all user reviews, paginated to 10 per page

### Latest Reviews Page

- This page will show the user the 9 latest reviews posted to the site
- Title of the games are clickable, leading to the game page

## Visual Design
	
The colour scheme of the site will be a triad of <span style="color:#3232cd">Blue</span>, <span style="color:#7070cd">Light Blue</span>, <span style="color:#32cd32">Green</span>, <span style="color:#cd3232">Red</span>, <span style="color:#cd7070">Light Red</span>

#3232cd, #7070cd, #32cd32, #cd3232, #cd7070

![colors](static/wireframes/color-scheme.png)

## Features

### Existing Features

#### By a User 
- Login/Register to site
- Add a game to the site
- Edit a games information
- Add a review to a game
- Edit their reviews
- Delete their reviews

#### By an Admin User
- All features from User
- Remove games from site
- Remove reviews from site
- Remove users from site
- Edit users username / type

### Features to be implemented
- User change profile image
- User change username
- A forum for users


## Technoogies used
- HTML
    - Font Awesome CDN
- CSS
    - Bootstrap
- Javascript
    - EmailJS
- Python
    - cachetools==4.2.2
    - click==8.0.1
    - dnspython==2.1.0
    - Flask==2.0.1
    - Flask-Caching==1.10.1
    - flask-paginate==0.8.1
    - Flask-PyMongo==2.3.0
    - gunicorn==20.1.0
    - httplib2==0.19.1
    - itsdangerous==2.0.1
    - oauthlib==3.1.1
    - protobuf==3.18.0
    - pyasn1==0.4.8
    - pyasn1-modules==0.2.8
    - pymongo==3.12.0
    - requests-oauthlib==1.3.0
    - rsa==4.7.2
    - uritemplate==3.0.1
    - Werkzeug==2.0.1
    - requests==2.26.0
- APIs
    - RAWG
    - Youtube


# Testing

## Planning



## Running Tests

- Testing the HTML code was done by generating a page and copying the HTML into the [W3C](https://validator.w3.org/) HTML Validator
- Testing the CSS was done with the [W3C](https://jigsaw.w3.org/css-validator/validator) validator
- Tesing Javascript was done with [Beautify Tools](https://beautifytools.com/javascript-validator.php)

### HTML5 
- /index - Passed, No Error
- /latest-reviews - Passed, No error
    - Duplicate class & alt attribute. Fixed, removed class & changed to aria-label.
- /games - Passed, No Error
    - Duplicate id attribute & bad type on a tag
- game/<game-id> - Passed, No Error
    - deprecated frameborder & width in iframe
- edit-game/<game-id> - Passed, No Error
    - mismatched h1/h2
- add-review - Passed, No Error
- login - Passed, No Errors
    - duplicate attribute & spelling on attribute
- register - Passed, No Errors
- profile - Passed, No Errors
- settings - Passed, No errors
- your-reviews - Passed, No errors
    - section heading
- review-game-search - Passed, No Errors
- edit-review - Passed, No Errors
- admin-base - Passed, No Errors
- admin-games-lookup - Passed, No Errors
    - Incorrect use of <select>
- admin-review-lookup - Passed, No Errors
- admin-user-lookup - Passed, No Errors
- edit-user - Passed, No Errors
    - Incorrect user of <select>

### CSS3 
[CSS Validated without error](static/images/css-validation.png)
### Javascript
- admin_games_search_script.js - No Errors
- admin_review_search_script.js - Missing semicolons - Fixed, No Errors
- admin_script.js - No Errors
- admin_user_search_script.js - No Errors
- game_page_script.js - Missing semicolons - Fixed, No Errors
- game_scripts.js - No Errors
- latest_reviews_script.js - Unused variable - Fixed, No Errors
- base_script.js - No Errors
- email_script.js - No Errors
- index_script.js - No Errors
- changepass_script.js - Missing Semicolons - Fixed, No Errors
- edit_review_script.js - Missing Semicolons - Fixed, No Errors
- game_search_script.js - No Errors
- profile_main_script.js - Missing Semicolons - Fixed, No Errors
- profile_script.js - Missing Semicolon - Fixed, No Errors
- register_script.js - No Errors
- yourreview_script.js - No Errors

### Lighthouse Results
#### Admin Pages
- Admin
    - [Desktop](static/images/lighthouse-tests/admin/admin_desktop.png)
    - [Mobile](static/images/lighthouse-tests/admin/admin_mobile.png)
- Game Search
    - [Desktop](static/images/lighthouse-tests/admin/admin_game-search_desktop.png)
    - [Mobile](static/images/lighthouse-tests/admin/admin_game-search_mobile.png)
- Review Search
    - [Desktop](static/images/lighthouse-tests/admin/admin_review-search_desktop.png)
    - [Mobile](static/images/lighthouse-tests/admin/admin_review-search_mobile.png)
- User Search
    - [Desktop](static/images/lighthouse-tests/admin/admin_user-search_desktop.png)
    - [Mobile](static/images/lighthouse-tests/admin/admin_user-search_mobile.png)

#### User Pages
- Login
    - [Desktop](static/images/lighthouse-tests/users/login_desktop.png)
    - [Mobile](static/images/lighthouse-tests/users/login_mobile.png)
- Profile Game Search
    - [Desktop](static/images/lighthouse-tests/users/profile_game-search_desktop.png)
    - [Mobile](static/images/lighthouse-tests/users/profile_game-search_mobile.png)
- Settings
    - [Desktop](static/images/lighthouse-tests/users/profile_settings_desktop.png)
    - [Mobile](static/images/lighthouse-tests/users/profile_settings_mobile.png)
- Your Reviews
    - [Desktop](static/images/lighthouse-tests/users/profile_your-reviews_desktop.png)
    - [Mobile](static/images/lighthouse-tests/users/profile_your-reviews_mobile.png)
- Profile Page
    - [Desktop](static/images/lighthouse-tests/users/profile-page_desktop.png)
    - [Mobile](static/images/lighthouse-tests/users/profile-page_mobile.png)
- Register
    - [Desktop](static/images/lighthouse-tests/users/register_desktop.png)
    - [Mobile](static/images/lighthouse-tests/users/register_mobile.png)
- User Game Search (API)
    - [Desktop](static/images/lighthouse-tests/users/user_game-search_desktop.png)
    - [Mobile](static/images/lighthouse-tests/users/user_game-search_mobile.png)

#### Game Pages
- Game Page
    - [Desktop](static/images/lighthouse-tests/games/game_desktop.png)
    - [Mobile](static/images/lighthouse-tests/games/game_mobile.png)
- Games Page
    - [Desktop](static/images/lighthouse-tests/games/games_desktop.png)
    - [Mobile](static/images/lighthouse-tests/games/games_mobile.png)
- Latest Games
    - [Desktop](static/images/lighthouse-tests/games/latest-reviews_desktop.png)
    - [Mobile](static/images/lighthouse-tests/games/latest-reviews_mobile.png)
#### Base Pages
- Index
    - [Desktop](static/images/lighthouse-tests/base/index_desktop.png)
    - [Mobile](static/images/lighthouse-tests/base/index_mobile.png)


## Testing Results

### Bugs that occured

## Deployment

## Bugs/Changes During Development

# Credits
- [Caching documentation](https://flask-caching.readthedocs.io/en/latest/)
- [Production server setup](https://gunicorn.org/)
- [Glowing button on hover start point](https://codepen.io/Stockin/pen/XPvpoB)
- [Flask Pagination](https://pythonhosted.org/Flask-paginate/)
- [Graphic for error page](https://pixabay.com/vectors/pixelgrafic-dos-game-invaders-158720/)
- [Flask custom error pages](https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/)
- [RAWG API](https://rawg.io/apidocs)
- [Youtube Search API](https://developers.google.com/youtube/v3/docs/search/list)

## This project is for educational purposes only

### Created by Codie Stephens-Evans