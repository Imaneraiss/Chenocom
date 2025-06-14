function moveElementsForMobile() {
  const navMenu = document.querySelector(".nav-menu");
  const flagSelector = document.querySelector(".flag-selector");
  const contactBtn = document.querySelector(".contact-botton-link");

  // Vérification que les éléments existent
  if (!navMenu || !flagSelector || !contactBtn) return;

  // Stockage des parents d'origine (déplacé ici pour éviter les problèmes de scope)
  const originalFlagParent = flagSelector.parentNode;
  const originalContactParent = contactBtn.parentNode;

  if (window.innerWidth <= 768) {
    // Version mobile
    if (!navMenu.contains(flagSelector)) {
      navMenu.appendChild(flagSelector);
    }
    if (!navMenu.contains(contactBtn)) {
      navMenu.appendChild(contactBtn);
    }
  } else {
    // Version desktop
    if (originalFlagParent !== flagSelector.parentNode) {
      originalFlagParent.appendChild(flagSelector);
    }
    if (originalContactParent !== contactBtn.parentNode) {
      originalContactParent.appendChild(contactBtn);
    }
  }
}

window.addEventListener("DOMContentLoaded", () => {
  // Initialisation
  moveElementsForMobile();
  
  // Gestion du redimensionnement avec debounce pour performance
  let resizeTimeout;
  window.addEventListener("resize", () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(moveElementsForMobile, 100);
  });
});