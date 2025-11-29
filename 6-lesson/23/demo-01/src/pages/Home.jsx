import { useEffect, useState } from "react";
import NewsCard from "../components/NewsCard";

const API = (import.meta.env.VITE_API_URL || "").replace(/\/$/, "");

export default function Home() {
  const [list, setList] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      setLoading(true);
      const res = await fetch(`${API}/api/news`);
      setList(res.ok ? await res.json() : []);
      setLoading(false);
    })();
  }, []);

  if (loading) return <p>Loading…</p>;
  return <div>{list.map(n => <NewsCard key={n.id} item={n} />)}</div>;
}
