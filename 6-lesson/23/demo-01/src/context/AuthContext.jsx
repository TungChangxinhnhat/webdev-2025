import { createContext, useContext, useEffect, useMemo, useState } from "react";

const API = (import.meta.env.VITE_API_URL || "").replace(/\/$/, "");
const Ctx = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem("token") || "");
  const [user, setUser] = useState(() => {
    try { return JSON.parse(localStorage.getItem("user") || "null"); }
    catch { return null; }
  });

  useEffect(() => {
    if (token) localStorage.setItem("token", token); else localStorage.removeItem("token");
    if (user) localStorage.setItem("user", JSON.stringify(user)); else localStorage.removeItem("user");
  }, [token, user]);

  async function login(email, password) {
    const res = await fetch(`${API}/auth/login`, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });
    if (!res.ok) throw new Error("Login failed");
    const data = await res.json();         // {access_token: "..."}
    const t = data.access_token || data.token || "";
    setToken(t);

    // Lấy thông tin người dùng (tùy backend: /auth/me)
    let me = { email, role: "user", is_author_verified: false };
    try {
      const meRes = await fetch(`${API}/auth/me`, { headers: { Authorization: `Bearer ${t}` } });
      if (meRes.ok) me = await meRes.json();
    } catch {}
    setUser(me);
    return me;
  }

  function logout() { setToken(""); setUser(null); }

  const value = useMemo(() => ({ token, user, login, logout }), [token, user]);
  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

export function useAuth() {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error("useAuth must be inside AuthProvider");
  return ctx;
}
