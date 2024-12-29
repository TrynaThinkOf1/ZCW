import React, { useState } from "react";
import { verifyEmail, verifyCode } from "../services/apiService";
import '../style/EmailVerification.css'

const EmailVerification: React.FC = () => {
  const [code, setCode] = useState("");
  const [step, setStep] = useState(1);
  const [userData, setUserData] = useState({
    passkey: "",
    email: "",
    firstName: "",
    lastName: "",
    displayName: "",
  });
  const [verif_passkey, setVerifPasskey] = useState("");

  const handleEmailSubmit = async () => {
    if (verif_passkey !== userData.passkey) {
      alert("Passkeys don't match");
      return;
    }
    try {
      const response = await verifyEmail(userData.email);
      alert(response.message);
      setStep(2);
    } catch (error: any) {
      alert(error.response?.data?.message || "Error verifying email.");
    }
  };

  const handleCodeSubmit = async () => {
    try {
      const response = await verifyCode(code, userData);
      alert("Verification successful!");
      console.log(response);
    } catch (error: any) {
      alert(error.response?.data?.message || "Error verifying code.");
    }
  };

  return (
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
            />
            <button onClick={handleEmailSubmit}>Create Account</button>
          </div>
      )}
      {step === 2 && (
          <div>
            <h2>Verify Email</h2>
            <input
                type="text"
                value={code}
                onChange={(e) => setCode(e.target.value)}
                placeholder="Enter the code"
                autoCapitalize="characters"
          />
          <button onClick={handleCodeSubmit}>Verify</button>
        </div>
      )}
    </div>
  );
};

export default EmailVerification;
