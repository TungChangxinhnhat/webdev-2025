import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Home from "./pages/Home";
import News from "./pages/News";
import Login from "./pages/Login";
import CreateNews from "./pages/CreateNews";
import { AuthProvider, useAuth } from "./context/AuthContext";
import { RequireAuthorVerified } from "./components/Guard";

function Menu() {
  const { user, logout } = useAuth();
  return (
    <nav style={{ display: "flex", gap: 12, marginBottom: 12 }}>
      <Link to="/">Home</Link>
      {!user && <Link to="/login">Login</Link>}
      {user && (<>
        <span>Hi, {user.email} ({user.role}{user.is_author_verified ? ", verified" : ""})</span>
        <button onClick={logout}>Logout</button>
      </>)}
      <RequireAuthorVerified><Link to="/create">Create</Link></RequireAuthorVerified>
    </nav>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Menu />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/news/:id" element={<News />} />
          <Route path="/login" element={<Login />} />
          <Route path="/create" element={<CreateNews />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
