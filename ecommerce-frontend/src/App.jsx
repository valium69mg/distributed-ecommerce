import { Routes, Route, Navigate } from "react-router-dom";
import { useAuth } from "./hooks/useAuth";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";

function App() {
  const { isLoggedIn } = useAuth();

  return (
    <Routes>
      <Route
        path="/home"
        element={isLoggedIn ? <HomePage /> : <Navigate to="/login" />}
      />
      <Route
        path="/login"
        element={!isLoggedIn ? <LoginPage /> : <Navigate to="/home" />}
      />
      <Route path="/" element={<Navigate to={isLoggedIn ? "/home" : "/login"} />} />
    </Routes>
  );
}

export default App;
