DATAFOOT

Courte description du projet : ce qu’il fait et à quoi il sert.

📦 Installation

Cloner le repo :

git clone https://github.com/SylvainBoniou/datafoot.git
cd REPO

Créer un environnement virtuel :

python -m venv venv

Activer l’environnement :

Mac / Linux

source venv/bin/activate

Windows

venv\Scripts\activate

Installer les dépendances :

pip install -r requirements.txt
▶️ Lancer le projet
python app.py

ou

python src/app.py
🧪 Tests
pytest
📁 Structure du projet
project/
│
├── src/
│   ├── main.py
│   └── modules/
│
├── data/
├── tests/
├── requirements.txt
├── README.md
└── .gitignore

⚙️ Variables d’environnement

Créer un fichier .env :

API_KEY=xxxx

Installer python-dotenv si besoin.

👤 Auteur

SylvainBoniou
GitHub : https://github.com/USER