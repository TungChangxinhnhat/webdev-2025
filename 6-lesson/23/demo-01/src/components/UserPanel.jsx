import { useState } from "react";

export default function UserPanel({ isLoading }) {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [hasNotifications] = useState(true);

  if (isLoading) {
    return <p>Загрузка...</p>;
  }

  return (
    <div>
      <h1>{isLoggedIn ? "Личный кабинет" : "Гость"}</h1>

      {isLoggedIn && (
        <p>
          У вас {hasNotifications ? "есть новые уведомления" : "нет новых уведомлений"}
        </p>
      )}

      <button onClick={() => setIsLoggedIn(!isLoggedIn)}>
        {isLoggedIn ? "Выйти" : "Войти"}
      </button>
    </div>
  );
}
