#  Chenocom - Générateur intelligent de devis pour sites web

Bienvenue dans **Chenocom**, un projet réalisé dans le cadre de mon stage chez [Chenocom](https://chenocom.com), une agence web spécialisée dans la création de sites modernes et performants.

EstimateurWeb permet aux clients de **téléverser un fichier (PDF, DOCX, image)** contenant leur demande de site web, puis génère automatiquement un **devis détaillé au format PDF**, après confirmation du client.

---

##  Fonctionnalités principales

-  **Upload de fichier (PDF, DOCX, PNG, JPG)**
- **Analyse intelligente avec Dialogflow**
- **Détection automatique de la langue (FR/EN)**
- **Nettoyage et enrichissement des informations**
- **Calcul dynamique du prix à partir de `prices.json`**
- **Message de confirmation interactif (CHENOCOM)**
- **Génération d’un devis PDF multilingue prêt à télécharger**
- **Détection d’incohérence de langue entre le site et le fichier**

---

## 🖼️ Aperçu du flux utilisateur

1. L'utilisateur arrive sur le site vitrine de **Chenocom**.
2. Il clique sur **"Demande de devis"**.
3. Il sélectionne la langue (FR/EN) et **upload son fichier**.
4. Le système analyse la demande et propose un **résumé clair**.
5. L'utilisateur **confirme ou refuse** le devis.
6. En cas de confirmation, un **PDF est généré** et proposé en téléchargement.

---

## 📁 Structure du projet

estimateurweb/
│
├── app.py # Application principale Flask
├── prices.json # Grille tarifaire pages + fonctionnalités
├── uploads/ # Fichiers uploadés et PDF générés
├── static/
│ └── images/
│ └── style.css 
│ └── style_devis.css  
├── templates/
│ ├── index.html # Page d'accueil (EN)
│ ├── index_fr.html # Page d'accueil (FR)
│ ├── demande_de_devis.html # Formulaire (EN)
│ └── demande_de_devis_fr.html # Formulaire (FR)
├── requirements.txt # Dépendances Python
└── README.md # 

** Créer et activer un environnement virtuel **
python -m venv venv
venv\Scripts\activate  # Sur Windows
# ou
source venv/bin/activate  # Sur Mac/Linux


** Installer les dépendances **
pip install -r requirements.txt

** Configurer Dialogflow **
Crée un projet sur Dialogflow
Télécharge le fichier clé JSON 
Renomme-le en ma_clef_dialogflow.json et place-le à la racine du projet

** Lancer le serveur **
python app.py
