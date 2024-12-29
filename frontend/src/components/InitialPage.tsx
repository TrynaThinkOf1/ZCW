import React from 'react';
import { useNavigate } from 'react-router-dom';

const IndexPage: React.FC = () => {
    const navigate = useNavigate();

    const handleCreateClick = () => {
        navigate("/create-account");
    };

    const handleLoginClick = () => {
        navigate("/login");
    };

    return (
        <div id="outer-container">
            <div>
                <button onClick={handleCreateClick}>Create Account</button><br/>
                <button onClick={handleLoginClick}>Login</button>
            </div>
        </div>
    );
};

export default IndexPage;