// Burger Menu
const burgerMenu = document.querySelector ('.burger-menu');
const mobileMenu =document.querySelector ('.nav-menu')
burgerMenu.addEventListener('click',()=>{
    burgerMenu.classList.toggle('active');
    mobileMenu.classList.toggle('active');
})

// Language Selector 


function setupLanguageSelector(currentFlagSelector, altFlagSelector) {
  const currentFlag = document.querySelector(currentFlagSelector);
  const altFlag = document.querySelector(altFlagSelector);

  if (!currentFlag || !altFlag) return; // Protection

  altFlag.addEventListener('click', (e) => {
    e.preventDefault();

    const currentSrc = currentFlag.getAttribute('src');
    const currentLang = currentFlag.getAttribute('data-lang');

    const altSrc = altFlag.getAttribute('src');
    const altLang = altFlag.getAttribute('data-lang');


    currentFlag.setAttribute('src', altSrc);
    currentFlag.setAttribute('data-lang', altLang);

    altFlag.setAttribute('src', currentSrc);
    altFlag.setAttribute('data-lang', currentLang);
  });
}


setupLanguageSelector('#current-flag-mobile', '#alt-flag-mobile');
setupLanguageSelector('.current-flag', '.alt-flag');




