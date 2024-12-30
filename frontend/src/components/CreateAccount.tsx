import React, { useState } from "react";
import { verifyEmail, verifyCode } from "../services/apiService";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import styles from "../style/CreateAccount.module.css";

const CreateAccount: React.FC = () => {
  const [code, setCode] = useState("");
  const [step, setStep] = useState(1);
  const [userData, setUserData] = useState({
    passkey: "",
    email: "",
    firstName: "",
    lastName: "",
    displayName: "",
  });
  const [verifPasskey, setVerifPasskey] = useState("");
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

  const handleEmailSubmit = async () => {
    if (verifPasskey !== userData.passkey) {
      renderMessage("Passkeys don't match");
      return;
    }
    try {
      const response = await verifyEmail(userData.email);
      setStep(2);
      setMessage("");
    } catch (error: any) {
      renderMessage(error.response?.data?.message || "Error verifying email.");
    }
  };

  const handleCodeSubmit = async () => {
    try {
      const response = await verifyCode(code, userData);
      const { token, user } = response;

      localStorage.setItem("jwt", token);

      console.log("User Info:", user);
      console.log("Token:", token);

      renderMessage("Code verified. Redirecting...");
      setTimeout(() => navigate("/profile", { state: { user } }), 1000);
    } catch (error: any) {
      renderMessage(error.response?.data?.message || "Error verifying code.");
    }
  };

  const navigate = useNavigate();

  return (
      <div className={styles.outercontainer}>
        <div>
          {step === 1 && (
              <div>
                <h2>Create Account</h2>
                <input
                    type="email"
                    value={userData.email}
                    onChange={(e) =>
                        setUserData({...userData, email: e.target.value})
                    }
                    placeholder="Email"
                />
                <input
                    type="text"
                    value={userData.displayName}
                    onChange={(e) =>
                        setUserData({...userData, displayName: e.target.value})
                    }
                    placeholder="Display Name"
                />
                <input
                    type="text"
                    value={userData.firstName}
                    onChange={(e) =>
                        setUserData({...userData, firstName: e.target.value})
                    }
                    placeholder="First Name"
                />
                <input
                    type="text"
                    value={userData.lastName}
                    onChange={(e) =>
                        setUserData({...userData, lastName: e.target.value})
                    }
                    placeholder="Last Name"
                />
                <input
                    type="password"
                    value={userData.passkey}
                    onChange={(e) =>
                        setUserData({...userData, passkey: e.target.value})
                    }
                    placeholder="Create a Passkey"
                />
                <input
                    type="password"
                    onChange={(e) => setVerifPasskey(e.target.value)}
                    placeholder="Verify Passkey"
                /><br/>
                {message && <p className="message">{message}</p>}
                <br/><button onClick={handleEmailSubmit}>Create Account</button>
                <br/><Link to="/login">or Login</Link>
              </div>
          )}
          {step === 2 && (
              <div>
                <h2>Verify Email</h2>
                <input
                    type="text"
                    value={code}
                    placeholder="Enter the code"
                    onChange={(e) => setCode(e.target.value.toUpperCase())}
              />
              {message && <p className="message">{message}</p>}
              <button onClick={handleCodeSubmit}>Verify</button>
            </div>
          )}
        </div>
      </div>
  );
};

export default CreateAccount;
