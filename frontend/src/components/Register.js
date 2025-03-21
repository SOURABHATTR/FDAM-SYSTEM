import React, { useState } from "react";
import { registerUser } from "../services/api"; // Use named import
import { useNavigate } from "react-router-dom";
import "./Register.css"; // Import CSS for styling

const Register = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const handleRegister = async (e) => {
        e.preventDefault();
        try {
            const response = await registerUser(username, password); // Call the function from API service

            if (response.status === 201) {
                alert("Registered Successfully! Balance: $1000");
                navigate("/login");
            }
        } catch (error) {
            alert("Registration failed. Try again.");
        }
    };

    return (
        <div className="register-container">
            <h2>Register</h2>
            <form onSubmit={handleRegister}>
                <input 
                    type="text" 
                    placeholder="Username" 
                    value={username}
                    onChange={(e) => setUsername(e.target.value)} 
                    required 
                />
                <input 
                    type="password" 
                    placeholder="Password" 
                    value={password}
                    onChange={(e) => setPassword(e.target.value)} 
                    required 
                />
                <button type="submit">Register</button>
            </form>
            <p>Already have an account? <a href="/login">Login here</a></p>
        </div>
    );
};

export default Register;
