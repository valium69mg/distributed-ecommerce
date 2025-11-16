import { useMutation } from "@tanstack/react-query";
import { useAuth } from "./useAuth"; // your custom hook to access AuthContext

export function useLogout() {
  const { logout } = useAuth();

  return useMutation({
    mutationFn: async () => {
      localStorage.removeItem("token");
    },
    onSuccess: () => {
      logout();
    },
  });
}
