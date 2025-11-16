import { useMutation } from "@tanstack/react-query";
import axios from "axios";

export function useLogin() {
  return useMutation({
    mutationFn: async ({ email, password }) => {
      const res = await axios.post(
        `http://localhost:3000/auth/login`, // replace with your users-host:users-port
        { email, password }
      );
      return res.data; 
    },
    onSuccess: (data) => {
      localStorage.setItem("token", data.token);
    },
  });
}
