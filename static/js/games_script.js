const currentLink = document.getElementById('games-link');

// When windows loads give the settings icon a blue glow
window.onload = function(){
  currentLink.classList.add('selected');
};