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


setupLanguageSelector('#current-flag-mobile','#alt-flag-mobile');
setupLanguageSelector('.current-flag','.alt-flag');

//Initialize Swiper
 
const swiper = new Swiper('.mySwiper', {
  slidesPerView: 'auto',
  centeredSlides: true,
  spaceBetween: 20,
  pagination: {
    el: '.swiper-pagination-hero-section',
    clickable: true,
    
  },
});

// Initialize mobile swiper with autoplay
const mobileSwiper = new Swiper('.swiper-mobile .mySwiper', {
  // Autoplay configuration
  autoplay: {
    delay: 3000, 
    disableOnInteraction: false, 
    pauseOnMouseEnter: true, 
  },
  
  // Pagination
  pagination: {
    el: '.swiper-pagination-mobile',
    clickable: true,
    dynamicBullets: true, 
  },
  
  
  loop: true, 
  speed: 800, 
  grabCursor: true, 
  effect: 'slide', 
  preventClicks: false, 
  
  // Responsive breakpoints
  breakpoints: {
    768: {
      allowTouchMove: false 
    }
  }
});

  const modal = document.getElementById('videoModal');
  const openBtn = document.getElementById('openPopup');
  const closeBtn = document.getElementById('closePopup');

  openBtn.onclick = () => {
    modal.style.display = 'flex';
  }

  closeBtn.onclick = () => {
    modal.style.display = 'none';
    modal.querySelector('video').pause();
  }

  window.onclick = (e) => {
    if (e.target === modal) {
      modal.style.display = 'none';
      modal.querySelector('video').pause();
    }
  }


