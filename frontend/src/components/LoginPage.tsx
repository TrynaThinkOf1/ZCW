import React, { useState } from "react";
import { loginUser } from "../services/apiService";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";

const CreateAccount: React.FC = () => {
  const [userData, setUserData] = useState({
    passkey: "",
    email: "",
  });
  const [message, setMessage] = useState("");

  const renderMessage = (message: string, field: string = "") => {
    setMessage(message);
    if (field) {
      const inputElement = document.querySelector(`input[name=${field}]`);
      if (inputElement) {
        inputElement.classList.add("error");
        setTimeout(() => {
          inputElement.classList.remove("error");
        }, 1500);
      }
    }
};


  const handleLogin = async () => {
    try {
      const response = await loginUser(userData.email, userData.passkey);
      const { user } = response;

      renderMessage("Login Successful");
      setTimeout(() => navigate("/profile", { state: { user, pfp: response.pfp } }), 1000);
    } catch (error: any) {
      renderMessage(error.response?.data?.message || "Error");
      console.error(error);
    }
  };

  const navigate = useNavigate();

  return (
      <div className={""}>
        <div>
              <div>
                <h2>Login</h2>
                <input
                    type="email"
                    value={userData.email}
                    onChange={(e) =>
                        setUserData({...userData, email: e.target.value})
                    }
                    placeholder="Email"
                />
                <input
                    type="password"
                    onChange={(e) => setUserData({...userData, passkey: e.target.value})}
                    placeholder="Passkey"
                /><br/>
                {message && <p className={""}>{message}</p>}
                <br/><button onClick={handleLogin}>Login</button>
                <br/><Link to="/create-account">or Create Account</Link>
              </div>
        </div>
      </div>
  );
};

export default CreateAccount;
