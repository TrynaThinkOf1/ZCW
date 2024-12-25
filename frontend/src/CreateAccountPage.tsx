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

    const checkForm = () => {
        let nameCheck = true
        let emailCheck = true
        let passkeyCheck = true

        if (!(displayName && firstName && lastName)) {
            nameCheck = false
        }

        let re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!Boolean(re.test(email))) {
            emailCheck = false
        }

        if (passkey !== verif_passkey) {
            passkeyCheck = false
        }

        if (nameCheck && emailCheck && passkeyCheck) {
            return true
        }
        return false
    }

    const sendRequest = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault()

        if (!checkForm()) {
            alert("Form is Invalid")
        }
        else {
            const data = new FormData()

            data.append("displayName", displayName)
            data.append("firstName", firstName)
            data.append("lastName", lastName)
            data.append("email", email)
            data.append("passkey", passkey)

            const response = fetch("http://45.79.216.238:1/api/user/create", {
                method: "POST",
                body: data
            })
            .then(res => res.json())
                .then(res => console.log(res))
                .catch((error) => console.log(error))
        }
    }

  return (
      <Fragment>
          <h1>Create Account</h1>
          <div id="form-container">
              <form onSubmit={sendRequest}>
                  <input type="text" id="displayname" placeholder="Display Name" onChange={(e) => set_displayName(e.target.value)} required /><br/>
                  <input type="text" id="firstname" placeholder="First Name" onChange={(e) => set_firstName(e.target.value)} required /><br/>
                  <input type="text" id="lastname" placeholder="Last Name" onChange={(e) => set_lastName(e.target.value)} required /><br/>
                  <input type="text" id="email" placeholder="Email" onChange={(e) => set_email(e.target.value)} required /><br/>
                  <input id="passkey" type="password" placeholder="Passkey" onChange={(e) => set_passkey(e.target.value)} required /><br/>
                  <input id="verif-passkey" type="password" placeholder="Verify Passkey" onChange={(e) => set_verifyPasskey(e.target.value)} required /><br/>
                  <button id="submit">Create Account</button>
              </form>
          </div>
      </Fragment>
  )
}

export default function MyApp() {
  return (
      <MakeForm />
  );
}
