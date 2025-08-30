@echo off
echo 🚀 Starting H.E.R.B.I.E. Chatbot Deployment to Firebase
echo ==================================================

REM Check if Firebase CLI is installed
firebase --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Firebase CLI not found. Installing...
    npm install -g firebase-tools
)

REM Navigate to project root
cd /d "%~dp0\.."

echo 📦 Installing Functions dependencies...
cd deployment\firebase\functions
call npm install
cd ..\..\..

echo 🏗️  Building React frontend...
cd frontend
call npm install
call npm run build
cd ..

echo 🔧 Building Firebase Functions...
cd deployment\firebase\functions
call npm run build
cd ..\..\..

echo 📋 Deployment Summary:
echo - Frontend: React build ready
echo - Backend: Firebase Functions ready
echo - Configuration: firebase.json configured

echo.
echo 🔥 Next Steps:
echo 1. Login to Firebase: firebase login
echo 2. Create Firebase project: firebase projects:create herbie-chatbot-ai
echo 3. Set active project: firebase use herbie-chatbot-ai
echo 4. Deploy: firebase deploy

echo.
echo ✅ Pre-deployment build completed!
echo Ready to deploy H.E.R.B.I.E. to Firebase! 🤖

pause