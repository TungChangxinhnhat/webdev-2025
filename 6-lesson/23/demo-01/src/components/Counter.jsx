import { useState } from "react";
import styles from '../styles/Button.module.css';

export default function Counter() {
  const [count, setCount] = useState(0);

  function handleClick() {
    setCount(count + 1);
  }

  return (
    <button className={styles.button} onClick={handleClick}>
      Нажато {count} раз
    </button>
  );
}
