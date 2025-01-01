import React from "react";
import { useLocation, Link, useNavigate } from "react-router-dom";
import SettingsLogo from "../assets/settings_logo.svg"

const ProfilePage: React.FC = () => {
  const { state } = useLocation();
  const navigate = useNavigate();
  const user = state?.user;
  const pfp = state?.pfp;

  const renderProfile = () => {
    if (!user) {
      return (
        <div id="outer-container">
          <h2>User Not Found</h2>
          <p>You need to log in to access this page.</p>
          <Link to="/login">Go to Login Page</Link>
        </div>
      );
    }

    return (
      <div className={""}>
        {/* Settings Button */}
        <button
          className={""}
          onClick={() => navigate("/settings", { state: { user, pfp } })}
          >
            <img className={""} src={SettingsLogo} alt="Settings Logo" />
        </button>

        <div className={""}>
          <div className={""}>
            <img
              src={`data:image/${user.pfpFormat || "jpeg"};base64,${pfp}`}
              alt="Profile"
              className={""}
            />
            <h2>{user.first_name} {user.last_name}, UID: {user.id}</h2>
            <div className={""}>
              <h3>Bio</h3>
              <p>{user.bio}</p>
            </div>
          </div>
          <div className={""}>
            <h1>{user.display_name}</h1>
            <div className={""}>
              <p>This is where posts would be.</p>
            </div>
          </div>
        </div>
      </div>
    );
  };

  return renderProfile();
};

export default ProfilePage;
