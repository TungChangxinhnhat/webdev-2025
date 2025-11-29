import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import CommentForm from "../components/CommentForm";
import { useAuth } from "../context/AuthContext";

const API = (import.meta.env.VITE_API_URL || "").replace(/\/$/, "");

export default function News() {
  const { id } = useParams();
  const { user } = useAuth();
  const [item, setItem] = useState(null);
  const [comments, setComments] = useState([]);

  async function load() {
    const res = await fetch(`${API}/api/news/${id}`);
    if (!res.ok) return;
    const data = await res.json();
    setItem(data);
    setComments(data.comments || []);
  }

  useEffect(() => { load(); }, [id]);

  if (!item) return <p>Loading…</p>;
  return (
    <div>
      <h2>{item.title}</h2>
      <p>{item.body}</p>
      <h4>Comments</h4>
      <ul>{comments.map(c => <li key={c.id}><b>{c.author?.email || c.author_name}:</b> {c.text}</li>)}</ul>
      {user ? <CommentForm newsId={item.id} onCreated={c => setComments(p => [...p, c])} /> : <p>Login to comment.</p>}
    </div>
  );
}
