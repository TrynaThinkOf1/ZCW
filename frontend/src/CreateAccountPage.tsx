import {Fragment} from "react";
import {useState} from "react";
import './CreateAccountPage.css';

function MakeForm() {
    const [displayName, set_displayName] = useState<string>("");
    const [firstName, set_firstName] = useState<string>("");
    const [lastName, set_lastName] = useState<string>("");
    const [email, set_email] = useState<string>("");
    const [passkey, set_passkey] = useState<string>("");
    const [verif_passkey, set_verifyPasskey] = useState<string>("");

    const [missingField, set_missingField] = useState<string | null>(null);

    const checkForm = () => {
        if (!displayName) {
            console.log("missing display name");
            set_missingField("Please add a Display Name");
            return false
        }
        if (!firstName) {
            console.log("missing first name");
            set_missingField("Please add a First Name");
            return false
        }
        if (!lastName) {
            console.log("missing last name");
            set_missingField("Please add a Last Name");
            return false
        }
        let re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!Boolean(re.test(email))) {
            console.log("missing valid email address");
            set_missingField("Please add a valid Email Address");
            return false
        }
        if (!passkey || passkey !== verif_passkey) {
            console.log("missing passkey or passkeys dont match");
            if (passkey !== verif_passkey) {
                set_missingField("Passkeys don't match");
                return false
            }
            set_missingField("Please enter a Passkey");
            return false
        }

        set_missingField(null);
        return true
    }

    const sendRequest = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault()

        if (!checkForm()) {
            return;
        }

        event.preventDefault()
        const data = new FormData()

        data.append("displayName", displayName)
        data.append("firstName", firstName)
        data.append("lastName", lastName)
        data.append("email", email)
        data.append("passkey", passkey)

        const response = fetch("http://172.20.10.2:5000/api/user/create", {
            method: "POST",
            body: data
        })
        .then(res => res.json())
            .then(res => console.log(res))
            .catch((error) => console.log(error))

    }

  return (
      <Fragment>
          <h1>Create Account</h1>
          <div id="form-container">
              <form onSubmit={sendRequest}>
                  <input type="text" id="displayname" placeholder="Display Name"
                         onChange={(e) => set_displayName(e.target.value)} required/><br/>
                  <input type="text" id="firstname" placeholder="First Name"
                         onChange={(e) => set_firstName(e.target.value)} required/><br/>
                  <input type="text" id="lastname" placeholder="Last Name"
                         onChange={(e) => set_lastName(e.target.value)} required/><br/>
                  <input type="text" id="email" placeholder="Email" onChange={(e) => set_email(e.target.value)}
                         required/><br/>
                  <input id="passkey" type="password" placeholder="Passkey"
                         onChange={(e) => set_passkey(e.target.value)} required/><br/>
                  <input id="verif-passkey" type="password" placeholder="Verify Passkey"
                         onChange={(e) => set_verifyPasskey(e.target.value)} required/><br/>
                  {missingField && (<p className="error-message">{missingField}</p>)}
                  <div id="terms-container">
                      <input type="checkbox" id="terms-checkbox"/>
                      <label htmlFor="terms-checkbox">
                          I agree to the <a href="/terms" target="_blank" rel="noopener noreferrer">Terms and
                          Conditions</a>
                      </label>
                  </div>
                  <button id="submit" formNoValidate>Create Account</button>
              </form>
          </div>
      </Fragment>
  )
}

export default function MyApp() {
    return (
        <MakeForm/>
    );
}
