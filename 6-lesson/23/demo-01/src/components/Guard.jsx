import { useAuth } from "../context/AuthContext";

export function RequireLogin({ children }) {
  const { user } = useAuth();
  return user ? children : null;
}

export function RequireRoles({ roles = [], children }) {
  const { user } = useAuth();
  if (!user) return null;
  return roles.includes(user.role) ? children : null;
}

export function RequireAuthorVerified({ children }) {
  const { user } = useAuth();
  if (!user || !user.is_author_verified) return null;
  return children;
}
