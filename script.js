// Burger Menu
const burgerMenu = document.querySelector(".burger-menu");
const mobileMenu = document.querySelector(".nav-menu");
burgerMenu.addEventListener("click", () => {
  burgerMenu.classList.toggle("active");
  mobileMenu.classList.toggle("active");
});

//Initialize Swiper

const swiper = new Swiper(".hero-section-swiper", {
  slidesPerView: "auto",
  centeredSlides: true,
  spaceBetween: 20,
  pagination: {
    el: ".swiper-pagination-hero-section",
    clickable: true,
  },
});


// Initialize mobile swiper with autoplay
const mobileSwiper = new Swiper(".swiper-mobile-swiper", {
  // Autoplay configuration
  autoplay: {
    delay: 3000,
    disableOnInteraction: false,
    pauseOnMouseEnter: true,
  },

  // Pagination
  pagination: {
    el: ".swiper-pagination-mobile",
    clickable: true,
  },

  loop: true,
  speed: 3000,
  /*  effect: 'slide',  */
  preventClicks: false,

  // Responsive breakpoints
  breakpoints: {
    768: {
      allowTouchMove: false,
    },
  },
});

const modal = document.getElementById("videoModal");
const openBtn = document.getElementById("openPopup");
const closeBtn = document.getElementById("closePopup");
function close_video() {
  modal.style.display = "none";
  modal.querySelector("video").pause();
}

function open_video() {
  modal.style.display = "flex";
  modal.querySelector("video").currentTime = 0,
  modal.querySelector("video").play();
}

openBtn.onclick = open_video;

closeBtn.onclick = close_video;

window.onclick = (e) => {
  if (e.target === modal) {
  close_video()
  }
};
