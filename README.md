# 🌿 AI-Powered Leaf Disease Detection System

A full-stack agricultural AI application that combines **computer vision, image segmentation, and deep-learning classification** to detect leaf diseases, identify infected regions, and estimate infection severity from uploaded leaf images.

> Developed as an internship project at the **Ethiopian Artificial Intelligence Institute**.

---

## 📌 Overview

The **AI-Powered Leaf Disease Detection System** is a web application that demonstrates how machine learning and computer vision can be applied to agricultural disease detection.

Users can upload an image of a plant leaf and receive an AI-generated analysis containing:

- 🌱 Disease classification
- 🎯 Detection of infected regions
- 📊 Infection severity estimation
- 🖼️ Visualized prediction results
- 📚 Prediction history

The application combines a **React frontend**, **Django REST API**, **SQLite database**, and trained machine-learning models into a complete end-to-end system.

---

## ✨ Features

### 🔐 Authentication

- User registration
- User login and logout
- JWT-based authentication
- Protected application functionality
- Admin account support

### 🌿 AI-Powered Leaf Analysis

Users can upload a leaf image and have the system:

1. Validate the uploaded image
2. Segment potentially infected regions
3. Identify individual disease regions
4. Classify detected diseases
5. Estimate infection severity
6. Generate a visualized prediction image
7. Store the prediction for later review

### 🧠 Disease Detection

The classification pipeline supports multiple disease categories, including:

- **Free Feeder**
- **Leaf Rust**
- **Leaf Skeletonizer**

The system can identify multiple disease regions within a single image.

### 📊 Prediction History

Users can review previous analyses, including:

- Original uploaded image
- AI-processed image
- Detected diseases
- Severity score
- Prediction date
- Prediction metadata

### 📈 Dashboard & Analytics

The dashboard provides an overview of:

- Total analyzed images
- Disease categories
- Registered users
- Alerts
- Prediction/severity statistics
- Historical prediction data

---

## 🧠 AI Pipeline

The core of the application combines **image validation, segmentation, classification, and severity estimation**.

```text
                  ┌──────────────────┐
                  │   Upload Leaf    │
                  │      Image       │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │ Image Validation │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │ Disease Region   │
                  │   Segmentation   │
                  └────────┬─────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
    ┌──────────────────┐      ┌──────────────────┐
    │ Disease Region   │      │ Leaf Segmentation│
    │   Detection      │      │                  │
    └────────┬─────────┘      └────────┬─────────┘
             │                         │
             ▼                         ▼
    ┌──────────────────┐      ┌──────────────────┐
    │ Disease          │      │ Infection Area   │
    │ Classification   │      │ Calculation      │
    └────────┬─────────┘      └────────┬─────────┘
             │                         │
             └────────────┬────────────┘
                          ▼
                 ┌──────────────────┐
                 │ Prediction Result│
                 │                  │
                 │ • Disease        │
                 │ • Severity       │
                 │ • Visual Overlay │
                 └──────────────────┘
```

### Image Validation

Before running the main prediction pipeline, the uploaded image is passed through a lightweight TensorFlow Lite model to help verify that the input is suitable for analysis.

### Disease Segmentation

A segmentation model identifies regions associated with disease within the uploaded image.

The detected regions are converted into contours that can be analyzed individually.

### Disease Classification

Detected regions are cropped and passed through the classification model to determine the corresponding disease category.

### Visualized Detection

Detected disease regions are overlaid on the original image, allowing users to visually see where the system identified potential infection.

### Severity Estimation

The application compares the detected diseased area with the segmented leaf area to produce a normalized severity score.

> **Note:** The severity value is a model-derived indicator and should not be interpreted as a professionally validated agricultural diagnosis.

---

## 🏗️ System Architecture

```text
┌───────────────────────────────┐
│          React + Vite         │
│                               │
│  Authentication               │
│  Image Upload                 │
│  Prediction Results           │
│  Prediction History           │
│  Dashboard & Charts           │
└───────────────┬───────────────┘
                │
                │ REST API
                ▼
┌───────────────────────────────┐
│       Django REST API         │
│                               │
│  Authentication               │
│  User Management              │
│  Image Processing             │
│  Prediction API               │
│  Prediction History           │
└───────────────┬───────────────┘
                │
       ┌────────┴─────────┐
       │                  │
       ▼                  ▼
┌─────────────┐   ┌─────────────────┐
│   SQLite    │   │ ML Inference    │
│             │   │                 │
│ Users       │   │ TensorFlow      │
│ Predictions │   │ OpenCV          │
│ Diseases    │   │ Segmentation    │
└─────────────┘   │ Classification  │
                  └─────────────────┘
```

---

## 🛠️ Tech Stack

### Frontend

- React
- Vite
- Tailwind CSS
- React Router
- Axios
- React Icons
- Recharts

### Backend

- Python
- Django
- Django REST Framework
- Simple JWT

### Database

- SQLite

### Machine Learning & Computer Vision

- TensorFlow
- TensorFlow Lite
- OpenCV
- NumPy
- Pandas
- Matplotlib
- Google Colab

### Model Storage

- Git LFS

---

## 🤖 Machine Learning Models

The application integrates multiple trained models into the inference pipeline:

| Model | Purpose |
|---|---|
| TensorFlow Lite verification model | Validates uploaded images before analysis |
| Disease segmentation model | Identifies potentially infected regions |
| Leaf segmentation model | Determines leaf area for severity estimation |
| Disease classification model | Classifies detected disease regions |

The trained model files are tracked using **Git Large File Storage (Git LFS)** due to their size.

---

## 📸 Application Preview

### Dashboard

The dashboard provides an overview of analyzed images, disease categories, users, alerts, and prediction statistics.
<img width="1919" height="901" alt="Screenshot 2026-08-08 144041" src="https://github.com/user-attachments/assets/1829b37b-de24-43a7-bba6-fe6d118cfc5e" />


### AI Prediction Results

<img width="1919" height="758" alt="Screenshot 2026-08-08 144119" src="https://github.com/user-attachments/assets/fe40affc-3e19-4eaa-9367-e18475c61ffe" />

The prediction interface displays the processed leaf image alongside detected disease and severity information.


### Prediction History

Previously analyzed images can be reviewed together with their prediction metadata.

<img width="1919" height="758" alt="Screenshot 2026-08-08 144119" src="https://github.com/user-attachments/assets/fdb5f4e7-4609-4062-8dfb-8e46f78e305c" />

---

## 🔑 Example Prediction

A prediction returned by the system contains information such as:

```text
Severity: 0.1200813249184633
Disease: leaf_rust, free_feeder
Date: 2023-10-19T15:17:04.132608Z
```

The system also generates a processed image in which detected disease regions are visually highlighted.

---

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3 and up
- Node.js
- npm
- Git
- Git LFS

Initialize Git LFS:

```bash
git lfs install
```

---

## 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd <PROJECT_DIRECTORY>
```

Pull the machine-learning models tracked with Git LFS:

```bash
git lfs pull
```

---

## 2. Backend Setup

Navigate to the backend:

```bash
cd backend
```

Create a Python virtual environment:

### Windows

```bash
python -m venv env
```

Activate the environment:

```bash
env\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run database migrations:

```bash
python manage.py migrate
```

Create an administrator account:

```bash
python manage.py createsuperuser
```

Start the Django development server:

```bash
python manage.py runserver
```

The backend will be available at:

```text
http://127.0.0.1:8000/
```

---

## 3. Frontend Setup

Open another terminal and navigate to the frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the Vite development server:

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173/
```

---

## 🔐 Authentication

The application uses **JSON Web Tokens (JWT)** for authentication.

Authentication functionality includes:

- User registration
- Login
- Access tokens
- Refresh tokens
- Token blacklisting
- Protected API endpoints
- User-specific prediction history

---

## 🔌 API Overview

### Authentication

```text
POST /api/token/
POST /api/token/refresh/
POST /api/user/create/
POST /api/user/logout/blacklist/
```

### Predictions

```text
POST /api/user/predict/
GET  /api/user/predictions/
GET  /api/user/prediction/<id>/
GET  /api/user/predictionDetail/
```

### Diseases

```text
GET /api/user/all_diseases/
GET /api/user/deseaseDetail/
GET /api/user/diseaseDetail/<id>/
```

### Users

```text
GET /api/user/user/
GET /api/user/userdetail/
```

---

## 🗄️ Data Model

The application primarily manages three domain entities:

```text
User
 │
 │
 └────────── Prediction
                 │
                 │ Many-to-Many
                 ▼
              Disease
```

### User

Stores application users and authentication information.

### Prediction

Stores:

- Uploaded image
- Processed prediction image
- Severity score
- Prediction metadata
- Timestamp
- Associated diseases

### Disease

Stores disease categories identified by the prediction pipeline.

---

## 📁 Project Structure

```text
App/
│
├── backend/
│   ├── core/
│   ├── users/
│   ├── base/
│   ├── models/
│   ├── media/
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── layouts/
│   │   ├── admin/
│   │   ├── axios/
│   │   └── utils/
│   │
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
├── .gitignore
└── README.md
```

---

## 🎓 Project Background

This project was developed as an **internship assignment at the Ethiopian Artificial Intelligence Institute**.

The project explored the practical application of machine learning and computer vision to agriculture by combining trained image-processing models with a full-stack web application.

The machine-learning models were developed and trained using **Google Colab**, while Django and React were used to turn the models into an interactive application accessible through a web interface.

---

## 🎥 Demo

A full video demonstration of the application will be added here soon.


---

## 🔮 Future Improvements

- [ ] Deploy the application for public access
- [ ] Improve model accuracy with larger and more diverse datasets
- [ ] Expand the number of supported diseases
- [ ] Add crop/plant species detection
- [ ] Improve severity estimation and calibration
- [ ] Add more detailed prediction analytics
- [ ] Add automated backend and frontend tests
- [ ] Containerize the application with Docker
- [ ] Add CI/CD
- [ ] Improve production security configuration

---

## ⚠️ Disclaimer

This project is a **machine-learning demonstration and internship project**.

Its predictions should not be considered a substitute for professional agricultural diagnosis or expert advice.

Model predictions depend on the quality and characteristics of the input image and the training data used to develop the models.

---

## 👨‍💻 Author

**Tobel Mikiyas**

Full-stack developer interested in building practical software systems that combine modern web technologies with AI and machine learning.
