// frontend/src/pages/FornitoriPage.jsx
import { useState, useEffect } from "react";
import Layout from "../components/Layout";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "../components/ui/card";
import { listFornitori } from "../api/fornitori";

export default function FornitoriPage() {
  const [fornitori, setFornitori] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    listFornitori()
      .then((res) => setFornitori(res.data))
      .finally(() => setLoading(false));
  }, []);

  return (
    <Layout title="Fornitori">
      <div className="space-y-3 max-w-2xl">
        {loading ? (
          <p className="text-sm text-muted-foreground">Caricamento...</p>
        ) : fornitori.length === 0 ? (
          <p className="text-sm text-muted-foreground">Nessun fornitore registrato.</p>
        ) : (
          fornitori.map((f) => (
            <Card key={f.id}>
              <CardHeader>
                <CardTitle>{f.full_name || f.email}</CardTitle>
                <CardDescription>{f.email}</CardDescription>
              </CardHeader>
              <CardContent>
                {f.servizi_offerti.length === 0 ? (
                  <p className="text-xs text-muted-foreground">Nessun servizio dichiarato.</p>
                ) : (
                  <div className="flex flex-wrap gap-1.5">
                    {f.servizi_offerti.map((s) => (
                      <span key={s.id} className="text-xs px-2 py-1 rounded-full bg-muted text-muted-foreground">
                        {s.nome}
                      </span>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </Layout>
  );
}
