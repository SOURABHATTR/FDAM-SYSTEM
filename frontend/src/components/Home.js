import React from "react";
import { Link } from "react-router-dom";

const Home = () => {
    return (
        <div>
            <h2>Welcome to FDAM System</h2>
            <Link to="/login">Go to Login</Link>
        </div>
    );
};

export default Home;
