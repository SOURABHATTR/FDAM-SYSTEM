import axios from "axios";

const API = axios.create({
    baseURL: "http://localhost:5000", 
    headers: { "Content-Type": "application/json" }
});

// ✅ Login User
export const loginUser = (username, password) =>
    API.post("/auth/login", { username, password });

// ✅ Register User
export const registerUser = (username, password) =>
    API.post("/auth/register", { username, password });

// ✅ Fetch All Transactions (Requires Authorization)
export const getTransactions = (token) =>
    API.get("/transactions/all", {
        headers: { Authorization: `Bearer ${token}` }
    });

// ✅ Report Fraud
export const reportFraud = (transactionId, reason, token) =>
    API.post("/fraud/report", { transactionId, reason }, {
        headers: { Authorization: `Bearer ${token}` }
    });

// ✅ Get User Details (Balance & Profile)
export const getUserDetails = (token) =>
    API.get("/users/me", {
        headers: { Authorization: `Bearer ${token}` }
    });

// ✅ Search Users
export const searchUsers = (query, token) =>
    API.get(`/users/search?query=${query}`, {
        headers: { Authorization: `Bearer ${token}` }
    });

// ✅ Make a Transaction (Transfers Money)
export const transferMoney = (sender, receiver, amount, token) =>
    API.post("/transactions/transfer", { sender, receiver, amount }, {
        headers: { Authorization: `Bearer ${token}` }
    });

export default API;
