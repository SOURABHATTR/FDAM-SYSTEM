import React, { useState, useEffect } from "react";
import axios from "../services/api";
import "./Dashboard.css"; // Import CSS for styling

const Dashboard = () => {
    const [users, setUsers] = useState([]);
    const [balance, setBalance] = useState(0);
    const [search, setSearch] = useState("");

    useEffect(() => {
        axios.get("/users/me")
            .then((res) => setBalance(res.data.balance))
            .catch(() => alert("Error fetching user balance"));
    }, []);

    const searchUsers = () => {
        if (!search.trim()) return; // Prevent empty search requests
        axios.get(`/users/search?query=${search}`)
            .then((res) => setUsers(res.data))
            .catch(() => alert("Error fetching users"));
    };

    return (
        <div className="dashboard-container">
            <h2 className="dashboard-title">Welcome to Your Dashboard</h2>
            <p className="dashboard-balance">💰 Balance: <strong>${balance.toFixed(2)}</strong></p>

            <div className="search-bar">
                <input 
                    type="text" 
                    placeholder="Search users..." 
                    value={search}
                    onChange={(e) => setSearch(e.target.value)} 
                />
                <button onClick={searchUsers}>🔍 Search</button>
            </div>

            <ul className="user-list">
                {users.length > 0 ? users.map((user) => (
                    <li key={user.id}>{user.username}</li>
                )) : <p>No users found.</p>}
            </ul>
        </div>
    );
};

export default Dashboard;
