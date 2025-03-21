export const isAuthenticated = () => {
    return localStorage.getItem("token") !== null;  // If token exists, user is authenticated
};
