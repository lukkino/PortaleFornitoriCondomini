// frontend/src/pages/ServiziPage.jsx
import { useState, useEffect } from "react";
import Layout from "../components/Layout";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "../components/ui/card";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { listServizi, createServizio } from "../api/servizi";
import { listCondomini } from "../api/condomini";
import { createRichiestaPreventivo } from "../api/richiestePreventivo";
import { Plus, Send } from "lucide-react";

function RichiediPreventivoForm({ servizio, condomini }) {
  const [open, setOpen] = useState(false);
  const [condominioId, setCondominioId] = useState("");
  const [descrizione, setDescrizione] = useState("");
  const [sending, setSending] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess(false);
    setSending(true);
    try {
      await createRichiestaPreventivo(servizio.id, Number(condominioId), descrizione);
      setSuccess(true);
      setDescrizione("");
      setCondominioId("");
    } catch (err) {
      setError(err.response?.data?.detail || "Errore durante l'invio della richiesta");
    } finally {
      setSending(false);
    }
  };

  if (condomini.length === 0) {
    return <p className="text-xs text-muted-foreground">Crea prima un condominio per poter richiedere un preventivo.</p>;
  }

  if (!open) {
    return (
      <button
        onClick={() => setOpen(true)}
        className="flex items-center gap-1 text-xs text-muted-foreground hover:text-foreground transition"
      >
        <Send className="w-3.5 h-3.5" /> Richiedi preventivo
      </button>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="mt-1 space-y-2">
      <select
        value={condominioId}
        onChange={(e) => setCondominioId(e.target.value)}
        required
        className="w-full px-3 py-2 rounded-lg border border-input bg-background text-foreground text-sm"
      >
        <option value="" disabled>Seleziona condominio</option>
        {condomini.map((c) => (
          <option key={c.id} value={c.id}>{c.denominazione}</option>
        ))}
      </select>
      <textarea
        value={descrizione}
        onChange={(e) => setDescrizione(e.target.value)}
        placeholder="Descrizione (opzionale)"
        rows={2}
        className="w-full px-3 py-2 rounded-lg border border-input bg-background text-foreground text-sm placeholder:text-muted-foreground"
      />
      {error && <p className="text-xs text-destructive">{error}</p>}
      {success && <p className="text-xs text-green-600">Richiesta inviata ai fornitori registrati per questo servizio.</p>}
      <div className="flex gap-2">
        <Button type="submit" size="sm" disabled={sending}>
          {sending ? "Invio..." : "Invia richiesta"}
        </Button>
        <Button type="button" size="sm" variant="ghost" onClick={() => setOpen(false)}>
          Annulla
        </Button>
      </div>
    </form>
  );
}

export default function ServiziPage() {
  const [servizi, setServizi] = useState([]);
  const [condomini, setCondomini] = useState([]);
  const [loading, setLoading] = useState(true);
  const [nome, setNome] = useState("");
  const [descrizione, setDescrizione] = useState("");
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState("");

  const loadServizi = () => {
    setLoading(true);
    listServizi()
      .then((res) => setServizi(res.data))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadServizi();
    listCondomini().then((res) => setCondomini(res.data)).catch(() => setCondomini([]));
  }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    setError("");
    setCreating(true);
    try {
      await createServizio(nome, descrizione);
      setNome("");
      setDescrizione("");
      loadServizi();
    } catch (err) {
      setError(err.response?.data?.detail || "Errore durante la creazione del servizio");
    } finally {
      setCreating(false);
    }
  };

  return (
    <Layout title="Servizi">
      <div className="space-y-6 max-w-2xl">
        <Card>
          <CardHeader>
            <CardTitle>Nuovo servizio</CardTitle>
            <CardDescription>Aggiungi un servizio al catalogo condiviso tra gli amministratori.</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleCreate} className="space-y-3">
              <div>
                <Label htmlFor="nome_servizio">Nome</Label>
                <Input
                  id="nome_servizio"
                  value={nome}
                  onChange={(e) => setNome(e.target.value)}
                  placeholder="Pulizie scale"
                  required
                />
              </div>
              <div>
                <Label htmlFor="descrizione_servizio">Descrizione (opzionale)</Label>
                <Input
                  id="descrizione_servizio"
                  value={descrizione}
                  onChange={(e) => setDescrizione(e.target.value)}
                  placeholder="Pulizia settimanale delle parti comuni"
                />
              </div>
              {error && (
                <div className="text-sm text-destructive bg-destructive/10 px-3 py-2 rounded-lg">{error}</div>
              )}
              <Button type="submit" disabled={creating}>
                <Plus /> {creating ? "Creazione..." : "Crea servizio"}
              </Button>
            </form>
          </CardContent>
        </Card>

        <div className="space-y-3">
          {loading ? (
            <p className="text-sm text-muted-foreground">Caricamento...</p>
          ) : servizi.length === 0 ? (
            <p className="text-sm text-muted-foreground">Nessun servizio nel catalogo.</p>
          ) : (
            servizi.map((s) => (
              <Card key={s.id}>
                <CardHeader>
                  <CardTitle>{s.nome}</CardTitle>
                  {s.descrizione && <CardDescription>{s.descrizione}</CardDescription>}
                </CardHeader>
                <CardContent>
                  <RichiediPreventivoForm servizio={s} condomini={condomini} />
                </CardContent>
              </Card>
            ))
          )}
        </div>
      </div>
    </Layout>
  );
}
