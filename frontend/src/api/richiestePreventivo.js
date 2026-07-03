// frontend/src/api/richiestePreventivo.js
import client from "./client";

export const listRichiestePreventivo = () => client.get("/api/richieste-preventivo");

export const createRichiestaPreventivo = (servizio_id, condominio_id, descrizione) =>
  client.post("/api/richieste-preventivo", {
    servizio_id,
    condominio_id,
    descrizione: descrizione || null,
  });
