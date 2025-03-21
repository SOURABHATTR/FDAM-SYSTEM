import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./components/Home";
import Login from "./components/Login";
import Register from "./components/Register";
import Dashboard from "./components/Dashboard";
import { isAuthenticated } from "./services/auth";  // Check if user is authenticated

const App = () => {
    return (
        <Router>
            <Navbar />  {/* Add Navbar on top */}
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route 
                    path="/dashboard" 
                    element={isAuthenticated() ? <Dashboard /> : <Navigate to="/register" />} 
                />
            </Routes>
        </Router>
    );
};

export default App;
