# DataFoot 

Analyse des performances des clubs et joueurs de Ligue. 

## 📦 Installation

Cloner le repo :

```bash
git clone https://github.com/SylvainBoniou/datafoot.git
cd REPO
```

Créer un environnement virtuel :

```bash
python -m venv venv
```

Activer l’environnement :

**Mac / Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

---

## ▶️ Lancer le projet

```bash
python app.py
```

---

## 🧪 Tests

```bash
pytest
```

---

## 📁 Structure du projet

```
project/
│
├──assets/
├──config/
├──data/
│   ├── processed/
│   └── raw/
│   └── test/
├──src/
│   ├── dashboard/
│   └── pipelines/
│   └── processing/
│   └── scrapping/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Variables d’environnement

Créer un fichier `.env` :

```
API_KEY=xxxx
```

Installer python-dotenv si besoin.

---

## 👤 Auteur

Sylvain BONIOU
GitHub : [https://github.com/SylvainBoniou](https://github.com/SylvainBoniou)
