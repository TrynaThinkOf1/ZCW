import { BrowserRouter, Routes, Route } from 'react-router-dom';
import CreateAccount from './components/CreateAccount.tsx'; // Import your components
import LoginPage from './components/LoginPage.tsx';
import ProfilePage from './components/ProfilePage.tsx';
import InitialPage from "./components/InitialPage.tsx";
import SettingsPage from './components/SettingsPage.tsx';

function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <Routes>
            <Route path="/" element={<InitialPage />} />
            <Route path="/create-account" element={<CreateAccount />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/profile" element={<ProfilePage />} />
            <Route path="/settings" element={<SettingsPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;