import React, {Fragment} from "react";
import { useLocation, Link } from "react-router-dom";

const ProfilePage: React.FC = () => {
  const { state } = useLocation();
  const user = state?.user;

  if (!user) {
    return <Fragment><p>No user data found. </p><Link to="/login">Login</Link></Fragment>;
  }

  const renderProfile = () => {
      return (
          <div id="outer-container">
              <div className="profile">
                  <img
                      src={`data:image/jpeg;base64,${user.pfp}`}
                      alt="Profile"
                      style={{width: "150px", height: "150px", borderRadius: "50%"}}
                  />
              </div>
          </div>
      )
  }
  return renderProfile();
};

export default ProfilePage;
