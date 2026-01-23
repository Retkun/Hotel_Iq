# 🏨 Hotel IQ – Plateforme d'Analyse de Données et d'Avis Hôteliers Pilotée par l'IA

**Hotel IQ** est une plateforme full-stack d'analyse de données qui combine la visualisation Power BI, le développement web moderne et l'analyse de sentiment par IA pour transformer les avis clients en insights stratégiques.

---

## 📋 Table des matières

- [Vue d'ensemble](#-vue-densemble)
- [Fonctionnalités principales](#-fonctionnalités-principales)
- [Architecture](#-architecture)
- [Technologies utilisées](#-technologies-utilisées)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [API](#-api)
- [Analyse IA](#-analyse-ia)
- [Améliorations futures](#-améliorations-futures)
- [Auteur](#-auteur)

---

## 🎯 Vue d'ensemble

Hotel IQ centralise et analyse les avis clients provenant de **TripAdvisor** pour offrir une vision complète de la satisfaction client. La plateforme propose :

- **Tableaux de bord Power BI** interactifs pour visualiser les KPIs métier
- **Analyse de sentiment alimentée par l'IA** (OpenAI) pour comprendre les retours clients
- **Interface web moderne** 100% en français pour une expérience utilisateur optimale
- **Architecture full-stack** démontrant des compétences en data engineering, développement web et IA

---

## ✨ Fonctionnalités principales

### 📊 Visualisation de données
- Trois tableaux de bord Power BI intégrés (Colt, Webhelp, Réservations)
- Consultation des KPIs en temps réel
- Interface responsive et intuitive

### 🤖 Intelligence artificielle
- Analyse automatique du sentiment des 5 derniers avis
- Détection des thèmes clés et tendances
- Synthèse des points forts et axes d'amélioration

### 🏨 Gestion hôtelière
- Liste complète des hôtels
- Consultation détaillée des avis clients
- Données synchronisées depuis TripAdvisor

---

## 🏗️ Architecture

```
Hotel_IQ/
│
├── Data_Analysis_and_AI-Reviews_frontend/    # Application Angular
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/                   # Composants UI
│   │   │   ├── services/                     # Services API
│   │   │   └── models/                       # Modèles TypeScript
│   │   └── assets/                           # Ressources statiques
│   └── package.json
│
├── Data_Analysis_and_AI-Reviews_backend/     # API FastAPI
│   ├── src/
│   │   ├── main.py                           # Point d'entrée
│   │   ├── models/                           # Modèles SQLAlchemy
│   │   ├── routes/                           # Endpoints API
│   │   └── services/                         # Logique métier
│   ├── database/                             # SQLite
│   ├── requirements.txt
│   └── .env.example
│
└── README.md
```

---

## 🛠️ Technologies utilisées

### Frontend
- **Angular 19** – Framework web moderne
- **TypeScript** – Typage statique
- **Power BI Embedded** – Intégration des dashboards
- **Iconify** – Bibliothèque d'icônes (Solar Icons)

### Backend
- **FastAPI** – Framework Python haute performance
- **SQLAlchemy** – ORM pour la gestion de base de données
- **SQLite** – Base de données légère
- **OpenAI API** – Analyse de sentiment par IA
- **TripAdvisor API** – Source des données hôtelières

---

## 🚀 Installation

### Prérequis

Assurez-vous d'avoir installé :
- **Node.js** 18+ et **npm**
- **Angular CLI** 19
- **Python** 3.8+
- **pip** (gestionnaire de paquets Python)

Vous aurez également besoin de :
- Clé API **TripAdvisor**
- Clé API **OpenAI**
- Accès **Power BI Embed**

---

### ⚙️ Configuration du Backend

1. **Naviguez vers le dossier backend**
   ```bash
   cd Data_Analysis_and_AI-Reviews_backend
   ```

2. **Créez un environnement virtuel** (recommandé)
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows : venv\Scripts\activate
   ```

3. **Installez les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurez les variables d'environnement**
   
   Créez un fichier `.env` à la racine du dossier backend :
   ```env
   API_KEY=votre_clé_tripadvisor
   OPENAI_API_KEY=votre_clé_openai
   ```

5. **Lancez le serveur**
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
   ```

6. **Vérifiez l'installation**
   
   Accédez à la documentation Swagger : [http://localhost:8000/docs](http://localhost:8000/docs)

---

### 🎨 Configuration du Frontend

1. **Naviguez vers le dossier frontend**
   ```bash
   cd Data_Analysis_and_AI-Reviews_frontend
   ```

2. **Installez les dépendances**
   ```bash
   npm install
   ```

3. **Lancez l'application**
   ```bash
   npm start
   ```

4. **Accédez à l'application**
   
   Ouvrez votre navigateur : [http://localhost:4200](http://localhost:4200)

---

## 💡 Utilisation

### Navigation principale

L'interface propose les sections suivantes :

| Page | Description |
|------|-------------|
| **Accueil** | Page d'accueil et présentation |
| **KPI Overflow** | Vue d'ensemble des indicateurs clés |
| **Tableau de Bord Colt** | Dashboard Power BI Colt |
| **Tableau de Bord Webhelp** | Dashboard Power BI Webhelp |
| **Tableau de Bord Réservations** | Dashboard Power BI Réservations |
| **Avis sur les Hôtels** | Consultation des hôtels et analyse IA |

### Analyse de sentiment

1. Accédez à la section **Avis sur les Hôtels**
2. Sélectionnez un hôtel dans la liste
3. Cliquez sur **Analyser avec l'IA**
4. Consultez le rapport de sentiment généré

---

## 🔌 API

Le backend expose une API RESTful accessible à `http://localhost:8000`

### Endpoints principaux

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/hotels/` | Liste tous les hôtels |
| `GET` | `/hotels/{location_id}` | Détails d'un hôtel spécifique |
| `GET` | `/hotels/{location_id}/reviews` | Avis d'un hôtel |
| `GET` | `/hotels/{location_id}/analysis` | Analyse IA des derniers avis |

### Exemple de requête

```bash
curl http://localhost:8000/hotels/123456/analysis
```

### Exemple de réponse

```json
{
  "sentiment": "positif",
  "themes": ["propreté", "emplacement", "personnel accueillant"],
  "summary": "Les clients apprécient particulièrement...",
  "reviews_analyzed": 5
}
```

---

## 🤖 Analyse IA

### Approche technique

L'analyse de sentiment utilise une **approche RAG légère** :

1. **Retrieval** : Récupération des 5 derniers avis depuis la base SQLite
2. **Augmentation** : Structuration des données pour le contexte
3. **Generation** : Envoi à l'API OpenAI pour analyse

### Résultats fournis

- ✅ Sentiment global (positif/négatif/neutre)
- 🔑 Thèmes récurrents identifiés
- 📈 Tendances de satisfaction
- 💬 Résumé synthétique des retours clients

> **Note** : Cette implémentation n'utilise pas de base vectorielle mais reste efficace pour des analyses ponctuelles sur de petits volumes de données.

---

## 🔮 Améliorations futures

### Court terme
- [ ] Graphiques de tendances temporelles
- [ ] Export des analyses en PDF
- [ ] Filtres avancés sur les avis

### Moyen terme
- [ ] Système d'authentification et rôles utilisateurs
- [ ] Migration vers PostgreSQL
- [ ] Cache Redis pour optimiser les performances

### Long terme
- [ ] Conteneurisation Docker
- [ ] Pipeline CI/CD (GitHub Actions)
- [ ] Base vectorielle pour RAG avancé
- [ ] Support multilingue de l'interface

---

## 👨‍💻 Auteur

**Malek Harbaoui**  
Data Science & Software Engineering

🔗 Compétences : Full-stack | Intelligence Artificielle | Analyse de Données

---

## 🙏 Remerciements

Merci d'avoir consulté **Hotel IQ** ! N'hésitez pas à contribuer ou à signaler des problèmes via les issues GitHub.

---

<div align="center">

**⭐ Si ce projet vous plaît, n'hésitez pas à lui donner une étoile ! ⭐**

</div>




