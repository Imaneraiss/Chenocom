from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

import pdfplumber
from docx import Document
from google.cloud import dialogflow_v2 as dialogflow
from google.cloud.dialogflow_v2.types import TextInput, QueryInput
import uuid
import json
import re
from fpdf import FPDF
from google.protobuf.json_format import MessageToDict
import ast
import string
from flask import send_from_directory
from flask import send_file

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ma_clef_dialogflow.json"
PROJECT_ID = "monprojetdialogflow-465522"

def extract_text(filepath):
    text = ""
    if filepath.endswith('.pdf'):
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
    elif filepath.endswith('.docx'):
        doc = Document(filepath)
        text = "\n".join([para.text for para in doc.paragraphs])
    elif filepath.lower().endswith(('.png', '.jpg', '.jpeg')):
        img = Image.open(filepath)
        text = pytesseract.image_to_string(img)
    else:
        raise ValueError("Unsupported file type")
    return text.strip()

def clean_feature(feat):
    # Enlever ponctuation finale (ex: '.'), et mettre en minuscules
    return feat.strip().rstrip(string.punctuation).lower()

def clean_features(features_raw):
    mapping = {
        "formulaire": "formulaire de contact",
        "formulaire de contact": "formulaire de contact",
        "formulaire de contact form": "formulaire de contact",
        "contact": "formulaire de contact",
        "form": "formulaire de contact",
        "map": "carte interactive",
        "carte google": "carte interactive",
        "google maps": "carte interactive",
        "carte interactive": "carte interactive",
        "galerie": "portfolio",
        "galerie photo": "portfolio",
        "portfolio": "portfolio",
        "recrutement": "recrutement",
        "page recrutement": "recrutement",
        "blog": "blog",
        "articles": "blog"
    }

    cleaned = []
    seen = set()
    for f in features_raw:
        key = f.lower().strip()
        key = mapping.get(key, key)
        if key not in seen:
            cleaned.append(key)
            seen.add(key)
    return cleaned

def convert_french_numbers_to_digits(text):
    mapping = {
        'un': '1', 'une': '1', 'deux': '2', 'trois': '3', 'quatre': '4',
        'cinq': '5', 'six': '6', 'sept': '7', 'huit': '8', 'neuf': '9',
        'dix': '10', 'onze': '11', 'douze': '12', 'treize': '13',
        'quatorze': '14', 'quinze': '15', 'seize': '16',
        'dix-sept': '17', 'dix-huit': '18', 'dix-neuf': '19', 'vingt': '20'
    }

    pattern = r'\b(' + '|'.join(mapping.keys()) + r')\b'
    return re.sub(pattern, lambda m: mapping[m.group(0).lower()], text, flags=re.IGNORECASE)

def detect_intent_text(text):
    session_client = dialogflow.SessionsClient()
    session_id = str(uuid.uuid4())
    session = session_client.session_path(PROJECT_ID, session_id)
    text_input = TextInput(text=text, language_code='fr')
    query_input = QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    result = response.query_result
    fulfillment = result.fulfillment_text
    params = result.parameters
    website_type = params.get("website_type", "Non spécifié")
    try:
        number_of_pages = int(params.get("number_of_pages", 0))
    except Exception:
        number_of_pages = 0

    raw_features = params.get("website_feature")
    print("RAW FEATURES FROM DIALOGFLOW:", raw_features)

    

    # Nettoyage : enlever ponctuation finale et mettre en minuscules
    features = [clean_feature(f) for f in raw_features]

    return fulfillment, number_of_pages, features, website_type
# --------------- Partie de prix -------------


with open('prices.json', 'r', encoding='utf-8') as f:
    prices = json.load(f)

# Dictionnaire de mapping des fonctionnalités
feature_mapping = {
    "formulaire de contact": "contact",
    "contact": "contact",
    "carte google": "carte interactive",
    "carte interactive": "carte interactive",
    "recrutement": "recrutement",
    "page recrutement": "recrutement",
    "blog": "blog",
    "articles": "blog",
    "portfolio": "portfolio" 
}

# Calculate total price :
def calculate_price(number_of_pages, features):
    total = 0

    for tranche in prices['pages']:
        if tranche['min'] <= number_of_pages <= tranche['max']:
            total += tranche['price']
            break

    for feat in features:
        key = feature_mapping.get(feat) 
        if key and key in prices['features']:
            total += prices['features'][key]

    return total

# Generating the pdf:
def generate_quote_pdf(client_text, number_of_pages, features, total_price, website_type, filename='devis.pdf'):
    pdf = FPDF()
    pdf.add_page()
    # Couleur de fond #2D2D2D
    pdf.set_fill_color(45, 45, 45)
    pdf.rect(0, 0, pdf.w, pdf.h, 'F')  # Remplit toute la page
    #Borders 
    pdf.set_draw_color(255, 255, 255) 

    pdf.set_font("Arial", size=12)

    pdf.set_font("Helvetica", 'B', 30)
    pdf.set_text_color(255, 255, 255)
    pdf.ln(10)
    pdf.set_xy(10, 15)
    pdf.cell(0, 10, "DEVIS", ln=True) # cell= one line , ln =new line, C center 
    pdf.image('static/images/logo.png', x=150, y=13, w=40)
    pdf.ln(25)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, "Commencez à voir des résultats - plus tôt nous commençons, plus vite vous gagnez..", ln=True)
    pdf.ln(10)

        # Définition de la table
    col1_width = 60
    col2_width = 80
    col3_width = 40
    line_height = 10

    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(245, 180, 0)
    pdf.cell(col1_width, line_height, "Elément", border=1, fill=True, align='C')
    pdf.cell(col2_width, line_height, "Détail", border=1, fill=True, align='C')
    pdf.cell(col3_width, line_height, "Prix", border=1, ln=True, fill=True, align='C')

    pdf.set_font("Arial", '', 12)
    pdf.set_text_color(255, 255, 255)

    pdf.cell(col1_width, line_height, "Type de site", border=1, align='C')
    pdf.cell(col2_width, line_height, website_type, border=1, align='C')
    pdf.cell(col3_width, line_height, "-", border=1, ln=True, align='C')

    for tranche in prices['pages']:
        if tranche['min'] <= number_of_pages <= tranche['max']:
            page_price = tranche['price']
            break
    else:
        page_price = "Inconnu"

    pdf.cell(col1_width, line_height, "Nombre de pages", border=1 , align='C')
    pdf.cell(col2_width, line_height, f"{number_of_pages} page(s)", border=1 , align='C')
    pdf.cell(col3_width, line_height, f"{page_price} dh", border=1, ln=True, align='C')

    # Lignes : Fonctionnalités
    if features:
        for feat in features:
            key = feature_mapping.get(feat.lower())
            prix = prices['features'].get(key, "Inconnu") if key else "Inconnu"
            pdf.cell(col1_width, line_height, "Fonctionnalité", border=1, align='C')
            pdf.cell(col2_width, line_height, feat, border=1, align='C')
            pdf.cell(col3_width, line_height, f"{prix} dh", border=1, ln=True , align='C')
    else:
        pdf.cell(col1_width, line_height, "Fonctionnalité", border=1 , align='C')
        pdf.cell(col2_width, line_height, "Aucune", border=1, align='C')
        pdf.cell(col3_width, line_height, "-", border=1, ln=True, align='C')

    # Ligne Total
    pdf.set_font("Arial", 'B', 13)
    pdf.cell(col1_width + col2_width, line_height, "Total", border=1, align='C')
    pdf.cell(col3_width, line_height, f"{total_price} dh", border=1, ln=True, align='C')

    pdf.ln(5)
    pdf.set_font("Arial", '', 10)
    pdf.cell(182, 10, "Confirmez ce devis et nous nous occupons du reste.", ln=True,align='R')

    output_path = os.path.join("uploads", filename)
    pdf.output(output_path)
    return output_path



@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/fr')
def index_fr():
    return render_template('index_fr.html')

@app.route("/demande_de_devis")
def demande_de_devis():
    return render_template("demande_de_devis.html")

@app.route("/demande_de_devis_fr")
def demande_de_devis_fr():
    return render_template("demande_de_devis_fr.html") 

def clean_text(text):
    import re
    text = re.sub(r'\n+', ' ', text)   # remplace retours à la ligne multiples par un espace
    text = re.sub(r'\s+', ' ', text)   # remplace espaces multiples par un seul espace
    return text.strip() 

@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files.get('file')
        if not file:
            return jsonify({"error": "Aucun fichier reçu"}), 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        text = extract_text(filepath)
        text = clean_text(text)
        text = convert_french_numbers_to_digits(text) 
        reply, number_of_pages, features, website_type = detect_intent_text(text)
        
        features = clean_features(features)


        total_price = calculate_price(number_of_pages, features)
        pdf_path = generate_quote_pdf(text, number_of_pages, features, total_price, website_type, filename='devis.pdf')


        """ return jsonify({
            "CLIENT": text,
            "CHENOCOM": reply,
            "TYPE_SITE": website_type,
            "number_of_pages": number_of_pages,
            "FEATURES": features,
            "PRIX_TOTAL": total_price,
            "DEVIS_PDF": pdf_path
        }) """
        """ return send_file(pdf_path, as_attachment=True) """
        return jsonify({
            "pdf_filename": "devis.pdf",
            "message": "Your quote is ready !"
    })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


@app.route('/download')
def download_file():
    filename = request.args.get('filename')
    if not filename:
        return "Nom de fichier manquant", 400
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    print("+++++++++++ Flask is running at http://127.0.0.1:5000/ ++++++")
    app.run(debug=True)




#Activate venv : venv\Scripts\activate
# Run : python app.py
