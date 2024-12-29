import React from "react";
import { useLocation } from "react-router-dom";

const ProfilePage: React.FC = () => {
  const { state } = useLocation();
  const user = state?.user;

  if (!user) {
    return <p>No user data found. Please verify your email.</p>;
  }

  return (
    <div>
      <h1>Welcome, {user.display_name}</h1>
      <p>Email: {user.email}</p>
      <p>First Name: {user.first_name}</p>
      <p>Last Name: {user.last_name}</p>
      {/* Add additional user information here */}
    </div>
  );
};

export default ProfilePage;
