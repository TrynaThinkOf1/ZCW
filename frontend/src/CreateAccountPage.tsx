import { Fragment, useState } from "react";
import './CreateAccountPage.css';

function MakeForm() {
    const [displayName, set_displayName] = useState<string>("");
    const [firstName, set_firstName] = useState<string>("");
    const [lastName, set_lastName] = useState<string>("");
    const [email, set_email] = useState<string>("");
    const [passkey, set_passkey] = useState<string>("");
    const [verif_passkey, set_verifyPasskey] = useState<string>("");

    const [verificationStep, setVerificationStep] = useState<'form' | 'verification'>('form');
    const [verificationCode, setVerificationCode] = useState<string>("");
    const [missingField, set_missingField] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(false);

    const checkForm = () => {
        if (!displayName) {
            set_missingField("Please add a Display Name");
            return false;
        }
        if (!firstName) {
            set_missingField("Please add a First Name");
            return false;
        }
        if (!lastName) {
            set_missingField("Please add a Last Name");
            return false;
        }
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!Boolean(re.test(email))) {
            set_missingField("Please add a valid Email Address");
            return false;
        }
        if (!passkey || passkey !== verif_passkey) {
            if (passkey !== verif_passkey) {
                set_missingField("Passkeys don't match");
                return false;
            }
            set_missingField("Please enter a Passkey");
            return false;
        }

        set_missingField(null);
        return true;
    };

    const requestVerification = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();

        if (!checkForm()) {
            return;
        }

        setIsLoading(true);
        try {
            const response = await fetch(`http://45.79.216.238:5000/api/user/verify/${email}`, {
                method: "GET"
            });

            const data = await response.json();

            if (response.ok) {
                setVerificationStep('verification');
                set_missingField(null);
            } else {
                set_missingField(data.message || "Failed to send verification code");
            }
        } catch (error) {
            set_missingField("Error connecting to server");
            console.error(error);
        } finally {
            setIsLoading(false);
        }
    };

    const submitVerification = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();

        if (!verificationCode) {
            set_missingField("Please enter verification code");
            return;
        }

        setIsLoading(true);

        const formData = new FormData();
        formData.append("displayName", displayName);
        formData.append("firstName", firstName);
        formData.append("lastName", lastName);
        formData.append("email", email);
        formData.append("passkey", passkey);

        try {
            const response = await fetch(`http://45.79.216.238:5000/api/code/verify/${verificationCode}`, {
                method: "POST",
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                alert("Account created successfully!");
                window.location.href = '/login';
            } else {
                set_missingField(data.message || "Invalid verification code");
            }
        } catch (error) {
            set_missingField("Error connecting to server");
            console.error(error);
        } finally {
            setIsLoading(false);
        }
    };

    const renderForm = () => (
        <form onSubmit={requestVerification}>
            <input
                type="text"
                id="displayname"
                placeholder="Display Name"
                value={displayName}
                onChange={(e) => set_displayName(e.target.value)}
                required
            /><br/>
            <input
                type="text"
                id="firstname"
                placeholder="First Name"
                value={firstName}
                onChange={(e) => set_firstName(e.target.value)}
                required
            /><br/>
            <input
                type="text"
                id="lastname"
                placeholder="Last Name"
                value={lastName}
                onChange={(e) => set_lastName(e.target.value)}
                required
            /><br/>
            <input
                type="text"
                id="email"
                placeholder="Email"
                value={email}
                onChange={(e) => set_email(e.target.value)}
                required
            /><br/>
            <input
                id="passkey"
                type="password"
                placeholder="Passkey"
                value={passkey}
                onChange={(e) => set_passkey(e.target.value)}
                required
            /><br/>
            <input
                id="verif-passkey"
                type="password"
                placeholder="Verify Passkey"
                value={verif_passkey}
                onChange={(e) => set_verifyPasskey(e.target.value)}
                required
            /><br/>
            <div id="terms-container">
                <input type="checkbox" id="terms-checkbox" required/>
                <label htmlFor="terms-checkbox">
                    I agree to the <a href="/terms" target="_blank" rel="noopener noreferrer">Terms and Conditions</a>
                </label>
            </div>
            <button id="submit" type="submit" disabled={isLoading}>
                {isLoading ? "Sending..." : "Create Account"}
            </button>
        </form>
    );

    const renderVerification = () => (
        <form onSubmit={submitVerification}>
            <p>Please enter the verification code sent to {email}</p>
            <input
                type="text"
                placeholder="Verification Code"
                value={verificationCode}
                onChange={(e) => setVerificationCode(e.target.value.toUpperCase())}
                maxLength={6}
                required
            /><br/>
            <button type="submit" disabled={isLoading}>
                {isLoading ? "Verifying..." : "Verify Code"}
            </button>
            <button
                type="button"
                onClick={() => setVerificationStep('form')}
                disabled={isLoading}
            >
                Back to Form
            </button>
        </form>
    );

    return (
        <Fragment>
            <h1>Create Account</h1>
            <div id="form-container">
                {missingField && (
                    <p className="error-message">{missingField}</p>
                )}
                {verificationStep === 'form' ? renderForm() : renderVerification()}
            </div>
        </Fragment>
    );
}

export default function MyApp() {
    return <MakeForm />;
}