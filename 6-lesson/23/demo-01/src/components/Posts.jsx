const posts = [
  { id: 1, title: "Первый пост" },
  { id: 2, title: "Второй пост" },
  { id: 3, title: "Третий пост" },
];

export default function Posts() { 
  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>
          {post.title}
        </li>
      ))}
    </ul>
  );
}
