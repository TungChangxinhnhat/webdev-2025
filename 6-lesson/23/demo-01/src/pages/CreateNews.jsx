import { useState } from "react";
import { useAuth } from "../context/AuthContext";
const API = (import.meta.env.VITE_API_URL || "").replace(/\/$/, "");

export default function CreateNews() {
  const { token } = useAuth();
  const [title, setTitle] = useState("");
  const [body, setBody] = useState("");
  const [msg, setMsg] = useState("");

  async function submit(e) {
    e.preventDefault();
    const res = await fetch(`${API}/api/news`, {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
      body: JSON.stringify({ title, body })
    });
    setMsg(res.ok ? "Created!" : "Failed");
    if (res.ok) { setTitle(""); setBody(""); }
  }

  return (
    <form onSubmit={submit} style={{ display: "grid", gap: 8, maxWidth: 480 }}>
      <input value={title} onChange={e => setTitle(e.target.value)} placeholder="Title" />
      <textarea rows={6} value={body} onChange={e => setBody(e.target.value)} placeholder="Body" />
      <button type="submit">Create</button>
      {msg && <em>{msg}</em>}
    </form>
  );
}
