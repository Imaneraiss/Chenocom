
function setLang(lang) {
    let newFlag = 'images/flags.svg'; // anglais par défaut
    if (lang === 'fr') {
      newFlag = 'images/fr.svg';
    }
    document.getElementById('current-flag').src = newFlag;
  }
