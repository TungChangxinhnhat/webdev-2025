import { Link } from "react-router-dom";
import styles from "../styles/app.module.css";

export default function NewsCard({ item }) {
  return (
    <article className={styles.card}>
      <h3><Link to={`/news/${item.id}`}>{item.title}</Link></h3>
      <p>{item.body?.slice(0, 140)}{item.body?.length > 140 ? "…" : ""}</p>
      <Link to={`/news/${item.id}`}>Read more →</Link>
    </article>
  );
}
