// frontend/src/pages/DashboardPage.jsx
import Layout from "../components/Layout";
import { useAuth } from "../store/authStore";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "../components/ui/card";

const ROLE_LABELS = {
  admin: "Amministratore",
  condomino: "Condomino",
  fornitore: "Fornitore",
};

export default function DashboardPage() {
  const { user } = useAuth();

  return (
    <Layout title="Dashboard">
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
    </Layout>
  );
}
