// frontend/src/api/condomini.js
import client from "./client";

export const listCondomini = () => client.get("/api/condomini");

export const listCondominiPublic = () => client.get("/api/condomini/public");

export const createCondominio = (denominazione, codice_fiscale, indirizzo) =>
  client.post("/api/condomini", { denominazione, codice_fiscale, indirizzo });

export const getCondominio = (id) => client.get(`/api/condomini/${id}`);

export const updateCondominio = (id, payload) =>
  client.put(`/api/condomini/${id}`, payload);

export const deleteCondominio = (id) => client.delete(`/api/condomini/${id}`);

export const listMembri = (id) => client.get(`/api/condomini/${id}/membri`);

export const addMembro = (id, email) =>
  client.post(`/api/condomini/${id}/membri`, { email });

export const removeMembro = (id, userId) =>
  client.delete(`/api/condomini/${id}/membri/${userId}`);
