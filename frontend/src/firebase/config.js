// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBwq-PwDfJVxxsxNGsNOaGRlMCPWKi5Hvk",
  authDomain: "herbie-8d4b4.firebaseapp.com",
  projectId: "herbie-8d4b4",
  storageBucket: "herbie-8d4b4.firebasestorage.app",
  messagingSenderId: "31597545737",
  appId: "1:31597545737:web:ff573e693059479e3febd8",
  measurementId: "G-LVM6626PEC"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

export { app, analytics };
export default app;