# Credify

A full-stack credit scoring and loan application platform built with:
- `credify_backend/`: Python FastAPI backend with MongoDB, authentication, account aggregation, scoring, agent support, and reports
- `Frontend/`: React + Vite + Tailwind web client with user/admin dashboards, chat assistant and loan application flows
- `credifyapp/`: Flutter mobile application targeting Android/iOS with auth, provider state management, and app navigation
- `resources/`: supporting datasets and notebooks for analysis

## Repository Structure

- `credify_backend/`
  - `main.py`: FastAPI entrypoint
  - `routers/`: API route modules for auth, scoring, applications, reports, account aggregation, admin, and agent endpoints
  - `services/`: business logic services for ML, email, PDF reports, agent behavior, and account aggregation
  - `ml_models/`: trained model definitions and scoring helpers
  - `database/`: MongoDB connection wrapper
  - `core/config.py`: environment and app settings
  - `templates/`: HTML email templates
  - `requirements.txt`: backend dependencies

- `Frontend/`
  - React app powered by Vite and Tailwind CSS
  - Authentication and protected route handling
  - User dashboard, admin dashboard, loan application forms, OTP/KYC verification, score views, EMI calculator, chatbot integration
  - `package.json` for front-end dependencies and scripts

- `credifyapp/`
  - Flutter app using `provider` state management
  - Mobile app entrypoint at `lib/main.dart`
  - Routes, theme, services, and providers for mobile usage
  - `pubspec.yaml` for Flutter dependencies

- `resources/`
  - `credit_score.csv`: dataset for credit score analysis or model training
  - `notebook962949420b.ipynb`: notebook for exploratory analysis or model investigation

## Key Features

- User and admin authentication
- Loan application management
- Credit scoring and predictive modeling
- Account aggregation APIs and analytics
- Admin reporting and dashboard views
- Chatbot/agent integration for user assistance
- PDF generation and email notification support
- Web frontend and Flutter mobile client

## Getting Started

### Backend

1. Install Python dependencies

```bash
cd "./credify_backend"
python -m pip install -r requirements.txt
```

2. Configure environment variables

Create a `.env` file in `credify_backend/` if needed. Common variables:

```env
MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=credify_db
JWT_SECRET=your_jwt_secret
EMAIL_USER=your_email@example.com
EMAIL_PASS=your_email_password
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
ML_MODEL_PATH=ml_models/credit_score_model.pkl
SCALER_PATH=ml_models/scaler.pkl
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.0-flash
```

3. Run the backend

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

4. Visit `http://localhost:8000` to confirm the backend is running.

### Frontend

1. Install Node.js dependencies

```bash
cd "./Frontend"
npm install
```

2. Start the development server

```bash
npm run dev
```

3. Open the local URL shown by Vite (usually `http://localhost:5173`).

### Mobile App

1. Install Flutter dependencies

```bash
cd "./credifyapp"
flutter pub get
```

2. Run the app on a connected device or emulator

```bash
flutter run
```

## Notes

- The backend relies on MongoDB. Make sure MongoDB is running and reachable using `MONGO_URI`.
- The web client and mobile client are separate frontends and may require their own backend base URL configuration.
- The backend contains machine learning support for credit scoring and uses the model files defined in `core/config.py`.

## Useful Commands

- Backend:
  - `python -m pip install -r requirements.txt`
  - `uvicorn main:app --reload`
- Frontend:
  - `npm install`
  - `npm run dev`
  - `npm run build`
- Mobile:
  - `flutter pub get`
  - `flutter run`

## License

This repository does not include a license file. Add one if you want to open-source the project.
# Credify
