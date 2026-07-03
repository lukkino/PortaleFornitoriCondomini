// frontend/src/api/auth.js
import client from "./client";

export const register = (payload) => client.post("/api/auth/register", payload);

// Il backend usa OAuth2PasswordRequestForm: si aspetta un body
// application/x-www-form-urlencoded con i campi username/password.
export const login = (email, password) => {
  const form = new URLSearchParams();
  form.append("username", email);
  form.append("password", password);
  return client.post("/api/auth/login", form, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
};

export const getMe = () => client.get("/api/auth/me");

export const refreshToken = (refresh_token) =>
  client.post("/api/auth/refresh", { refresh_token });

export const logout = (refresh_token) =>
  client.post("/api/auth/logout", { refresh_token });
