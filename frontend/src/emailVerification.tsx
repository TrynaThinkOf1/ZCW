import React, { useState } from "react";
import { verifyEmail, verifyCode } from "./services/apiService";

const EmailVerification: React.FC = () => {
    const [email, setEmail] = useState("");
    const [code, setCode] = useState("");
    const [step, setStep] = useState(1);
    const [userData, setUserData] = useState({
        passkey: "",
        email: "",
        firstName: "",
        lastName: "",
        displayName: "",
    });

    const handleEmailSubmit = async () => {
        try {
            const response = await verifyEmail(email);
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
                    <h2>Verify Email</h2>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Enter your email"
                    />
                    <button onClick={handleEmailSubmit}>Send Verification Code</button>
                </div>
            )}
            {step === 2 && (
                <div>
                    <h2>Enter Verification Code</h2>
                    <input
                        type="text"
                        value={code}
                        onChange={(e) => setCode(e.target.value)}
                        placeholder="Enter the code"
                    />
                    <input
                        type="password"
                        value={userData.passkey}
                        onChange={(e) =>
                            setUserData({ ...userData, passkey: e.target.value })
                        }
                        placeholder="Create a password"
                    />
                    <input
                        type="text"
                        value={userData.firstName}
                        onChange={(e) =>
                            setUserData({ ...userData, firstName: e.target.value })
                        }
                        placeholder="First Name"
                    />
                    <input
                        type="text"
                        value={userData.lastName}
                        onChange={(e) =>
                            setUserData({ ...userData, lastName: e.target.value })
                        }
                        placeholder="Last Name"
                    />
                    <input
                        type="text"
                        value={userData.displayName}
                        onChange={(e) =>
                            setUserData({ ...userData, displayName: e.target.value })
                        }
                        placeholder="Display Name"
                    />
                    <button onClick={handleCodeSubmit}>Verify Code</button>
                </div>
            )}
        </div>
    );
};

export default EmailVerification;
