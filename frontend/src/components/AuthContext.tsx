import { createContext } from "react";
import { useEffect, useState } from "react";
import LoginDialog from "./login-dialog";

type AuthContextProviderProps = {
  user?: AuthenticatedUser | null;
  children: React.ReactNode;
};

export type AuthContextProps = {
  user: AuthenticatedUser | null;
};

export type AuthenticatedUser = {
  id: string;
  first_name: string;
  last_name: string;
  username: string;
};

export const AuthContext = createContext<AuthContextProps>({
  user: null,
});
export function AuthContextProvider(props: AuthContextProviderProps) {
  const [user, setUser] = useState<AuthenticatedUser | null>(null);

  useEffect(() => {
    const fetchUser = async () => {
      const res = await fetch("/api/profile");
      if (!res.ok) {
        console.warn("Failed to get user");
        return null;
      }
      const data = await res.json();
      setUser(data);
    };

    fetchUser();
  }, []);

  if (user === null) {
    return <LoginDialog />;
  }

  return <AuthContext.Provider value={{ user }}>{props.children}</AuthContext.Provider>;
}
