// frontend/src/api/servizi.js
import client from "./client";

export const listServiziPublic = () => client.get("/api/servizi/public");

export const listServizi = () => client.get("/api/servizi");

export const createServizio = (nome, descrizione) =>
  client.post("/api/servizi", { nome, descrizione: descrizione || null });
