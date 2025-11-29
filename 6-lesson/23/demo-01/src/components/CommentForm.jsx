import { useState } from "react";
import { useAuth } from "../context/AuthContext";

const API = (import.meta.env.VITE_API_URL || "").replace(/\/$/, "");

export default function CommentForm({ newsId, onCreated }) {
  const { token } = useAuth();
  const [text, setText] = useState("");

  async function submit(e) {
    e.preventDefault();
    if (!text.trim()) return;
    const res = await fetch(`${API}/api/news/${newsId}/comments`, {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
      body: JSON.stringify({ text }) // đổi 'text' → key backend yêu cầu nếu khác
    });
    if (res.ok) {
      const c = await res.json();
      setText("");
      onCreated && onCreated(c);
    } else {
      alert("Failed to post comment");
    }
  }

  return (
    <form onSubmit={submit} style={{ display: "flex", gap: 8 }}>
      <input value={text} onChange={e => setText(e.target.value)} placeholder="Your comment" />
      <button type="submit">Send</button>
    </form>
  );
}
