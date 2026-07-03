// frontend/src/pages/DashboardPage.jsx
import { useState, useEffect } from "react";
import Layout from "../components/Layout";
import { useAuth } from "../store/authStore";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "../components/ui/card";
import { listRichiestePreventivo } from "../api/richiestePreventivo";

const ROLE_LABELS = {
  admin: "Amministratore",
  condomino: "Condomino",
  fornitore: "Fornitore",
};

function RichiesteRicevute() {
  const [richieste, setRichieste] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    listRichiestePreventivo()
      .then((res) => setRichieste(res.data))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <p className="text-sm text-muted-foreground">Caricamento richieste...</p>;
  }

  if (richieste.length === 0) {
    return <p className="text-sm text-muted-foreground">Nessuna richiesta di preventivo ricevuta.</p>;
  }

  return (
    <div className="space-y-3">
      {richieste.map((r) => (
        <Card key={r.id}>
          <CardHeader>
            <CardTitle>{r.servizio.nome}</CardTitle>
            <CardDescription>
              Richiesto da {r.admin.full_name || r.admin.email} · {r.condominio.denominazione} — {r.condominio.indirizzo}
            </CardDescription>
          </CardHeader>
          {r.descrizione && (
            <CardContent>
              <p className="text-sm text-muted-foreground">{r.descrizione}</p>
            </CardContent>
          )}
        </Card>
      ))}
    </div>
  );
}

export default function DashboardPage() {
  const { user } = useAuth();

  return (
    <Layout title="Dashboard">
      <div className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>Benvenuto, {user?.full_name || user?.email}</CardTitle>
            <CardDescription>
              Sei registrato come {ROLE_LABELS[user?.role] || user?.role}.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground text-sm">
              Le funzionalità del portale (gestione fornitori e condomini) sono in arrivo.
            </p>
          </CardContent>
        </Card>

        {user?.role === "fornitore" && <RichiesteRicevute />}
      </div>
    </Layout>
  );
}
