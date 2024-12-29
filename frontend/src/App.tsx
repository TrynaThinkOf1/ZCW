import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import CreateAccount from './components/CreateAccount.tsx'; // Import your components
import LoginPage from './components/LoginPage.tsx';
import ProfilePage from './components/ProfilePage.tsx';
import InitialPage from "./components/InitialPage.tsx";

function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <Routes>
            <Route path="/" element={<InitialPage />} />
          <Route path="/create-account" element={<CreateAccount />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/profile" element={<ProfilePage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;