// frontend/src/api/fornitori.js
import client from "./client";

export const listFornitori = () => client.get("/api/fornitori");
