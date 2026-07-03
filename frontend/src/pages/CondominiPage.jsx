// frontend/src/pages/CondominiPage.jsx
import { useState, useEffect } from "react";
import Layout from "../components/Layout";
import { useAuth } from "../store/authStore";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "../components/ui/card";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import {
  listCondomini,
  createCondominio,
  listMembri,
  addMembro,
  removeMembro,
} from "../api/condomini";
import { Plus, Users, Trash2, ChevronDown, ChevronUp } from "lucide-react";

function MembriPanel({ condominioId }) {
  const [membri, setMembri] = useState([]);
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [adding, setAdding] = useState(false);

  const loadMembri = () => {
    setLoading(true);
    listMembri(condominioId)
      .then((res) => setMembri(res.data))
      .catch(() => setError("Impossibile caricare i membri"))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadMembri();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [condominioId]);

  const handleAdd = async (e) => {
    e.preventDefault();
    setError("");
    setAdding(true);
    try {
      await addMembro(condominioId, email);
      setEmail("");
      loadMembri();
    } catch (err) {
      setError(err.response?.data?.detail || "Errore durante l'aggiunta del condomino");
    } finally {
      setAdding(false);
    }
  };

  const handleRemove = async (userId) => {
    try {
      await removeMembro(condominioId, userId);
      loadMembri();
    } catch {
      setError("Errore durante la rimozione");
    }
  };

  return (
    <div className="mt-4 pt-4 border-t border-border space-y-3">
      <form onSubmit={handleAdd} className="flex gap-2">
        <Input
          type="email"
          placeholder="email@condomino.it"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="flex-1"
        />
        <Button type="submit" disabled={adding} size="sm">
          <Plus /> Aggiungi
        </Button>
      </form>

      {error && <p className="text-xs text-destructive">{error}</p>}

      {loading ? (
        <p className="text-xs text-muted-foreground">Caricamento membri...</p>
      ) : membri.length === 0 ? (
        <p className="text-xs text-muted-foreground">Nessun condomino associato.</p>
      ) : (
        <ul className="space-y-1.5">
          {membri.map((m) => (
            <li key={m.id} className="flex items-center justify-between text-sm px-3 py-1.5 rounded-lg bg-muted/50">
              <span>{m.full_name || m.email}</span>
              <button onClick={() => handleRemove(m.id)} className="text-muted-foreground hover:text-destructive transition">
                <Trash2 className="w-3.5 h-3.5" />
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

function CondominioCard({ condominio, isAdmin }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <Card>
      <CardHeader>
        <div className="flex items-start justify-between">
          <div>
            <CardTitle>{condominio.denominazione}</CardTitle>
            <CardDescription>
              CF {condominio.codice_fiscale} · {condominio.indirizzo}
            </CardDescription>
          </div>
          {isAdmin && (
            <button
              onClick={() => setExpanded(!expanded)}
              className="flex items-center gap-1 text-xs text-muted-foreground hover:text-foreground transition"
            >
              <Users className="w-3.5 h-3.5" />
              Membri
              {expanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
            </button>
          )}
        </div>
      </CardHeader>
      {isAdmin && expanded && (
        <CardContent>
          <MembriPanel condominioId={condominio.id} />
        </CardContent>
      )}
    </Card>
  );
}

export default function CondominiPage() {
  const { user } = useAuth();
  const isAdmin = user?.role === "admin";

  const [condomini, setCondomini] = useState([]);
  const [loading, setLoading] = useState(true);
  const [denominazione, setDenominazione] = useState("");
  const [codiceFiscale, setCodiceFiscale] = useState("");
  const [indirizzo, setIndirizzo] = useState("");
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState("");

  const loadCondomini = () => {
    setLoading(true);
    listCondomini()
      .then((res) => setCondomini(res.data))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadCondomini();
  }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    setError("");
    setCreating(true);
    try {
      await createCondominio(denominazione, codiceFiscale, indirizzo);
      setDenominazione("");
      setCodiceFiscale("");
      setIndirizzo("");
      loadCondomini();
    } catch (err) {
      setError(err.response?.data?.detail || "Errore durante la creazione del condominio");
    } finally {
      setCreating(false);
    }
  };

  return (
    <Layout title="Condomini">
      <div className="space-y-6 max-w-2xl">
        {isAdmin && (
          <Card>
            <CardHeader>
              <CardTitle>Nuovo condominio</CardTitle>
              <CardDescription>Registra un condominio che amministri.</CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleCreate} className="space-y-3">
                <div>
                  <Label htmlFor="denominazione">Denominazione</Label>
                  <Input
                    id="denominazione"
                    value={denominazione}
                    onChange={(e) => setDenominazione(e.target.value)}
                    placeholder="Condominio Via Roma 12"
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="codice_fiscale">Codice Fiscale</Label>
                  <Input
                    id="codice_fiscale"
                    value={codiceFiscale}
                    onChange={(e) => setCodiceFiscale(e.target.value)}
                    placeholder="12345678901"
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="indirizzo">Indirizzo</Label>
                  <Input
                    id="indirizzo"
                    value={indirizzo}
                    onChange={(e) => setIndirizzo(e.target.value)}
                    placeholder="Via Roma 12, Milano"
                    required
                  />
                </div>

                {error && (
                  <div className="text-sm text-destructive bg-destructive/10 px-3 py-2 rounded-lg">{error}</div>
                )}

                <Button type="submit" disabled={creating}>
                  <Plus /> {creating ? "Creazione..." : "Crea condominio"}
                </Button>
              </form>
            </CardContent>
          </Card>
        )}

        <div className="space-y-3">
          {loading ? (
            <p className="text-sm text-muted-foreground">Caricamento...</p>
          ) : condomini.length === 0 ? (
            <p className="text-sm text-muted-foreground">Nessun condominio da mostrare.</p>
          ) : (
            condomini.map((c) => <CondominioCard key={c.id} condominio={c} isAdmin={isAdmin} />)
          )}
        </div>
      </div>
    </Layout>
  );
}
