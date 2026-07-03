// frontend/src/pages/RegisterPage.jsx
import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import { register, getMe } from "../api/auth";
import { listCondominiPublic } from "../api/condomini";
import { listServiziPublic } from "../api/servizi";
import { useAuth } from "../store/authStore";
import { Eye, EyeOff, Building2 } from "lucide-react";

export default function RegisterPage() {
  const [email, setEmail] = useState("");
  const [fullName, setFullName] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("condomino");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { loginUser } = useAuth();
  const navigate = useNavigate();

  // Scheda anagrafica condomino
  const [nome, setNome] = useState("");
  const [cognome, setCognome] = useState("");
  const [codiceFiscale, setCodiceFiscale] = useState("");
  const [telefono, setTelefono] = useState("");
  const [pec, setPec] = useState("");
  const [condominioId, setCondominioId] = useState("");
  const [condomini, setCondomini] = useState([]);

  // Servizi offerti (fornitore)
  const [serviziOfferti, setServiziOfferti] = useState([]);
  const [servizi, setServizi] = useState([]);

  const isCondomino = role === "condomino";
  const isFornitore = role === "fornitore";

  useEffect(() => {
    if (!isCondomino) return;
    listCondominiPublic()
      .then((res) => setCondomini(res.data))
      .catch(() => setCondomini([]));
  }, [isCondomino]);

  useEffect(() => {
    if (!isFornitore) return;
    listServiziPublic()
      .then((res) => setServizi(res.data))
      .catch(() => setServizi([]));
  }, [isFornitore]);

  const toggleServizio = (id) => {
    setServiziOfferti((prev) =>
      prev.includes(id) ? prev.filter((s) => s !== id) : [...prev, id]
    );
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const payload = { email, password, role };
      if (isCondomino) {
        payload.nome = nome;
        payload.cognome = cognome;
        payload.codice_fiscale = codiceFiscale;
        payload.telefono = telefono;
        payload.pec = pec.trim() || null;
        payload.condominio_id = condominioId ? Number(condominioId) : null;
      } else {
        payload.full_name = fullName;
        if (isFornitore) {
          payload.servizio_ids = serviziOfferti;
        }
      }

      const res = await register(payload);
      const { access_token, refresh_token } = res.data;
      localStorage.setItem("access_token", access_token);
      const me = await getMe();
      loginUser(access_token, refresh_token, me.data);
      navigate("/dashboard");
    } catch (err) {
      setError(err.response?.data?.detail || "Errore durante la registrazione");
    } finally {
      setLoading(false);
    }
  };

  const inputClass = "w-full px-4 py-2.5 rounded-xl border border-input bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring transition text-sm";
  const labelClass = "block text-sm font-medium text-foreground mb-1.5";

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-background py-10">
      <div className="w-full max-w-md px-8 py-10 bg-card rounded-2xl shadow-lg border border-border">
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-3">
            <div className="w-12 h-12 rounded-2xl bg-primary/10 flex items-center justify-center">
              <Building2 className="w-6 h-6 text-primary" />
            </div>
          </div>
          <h1 className="text-2xl font-bold text-foreground">Crea un account</h1>
          <p className="text-muted-foreground text-sm mt-1">Registrati al portale</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className={labelClass}>Sei</label>
            <select value={role} onChange={e => setRole(e.target.value)} className={inputClass}>
              <option value="condomino">Condomino</option>
              <option value="fornitore">Fornitore</option>
              <option value="admin">Amministratore di condominio</option>
            </select>
          </div>

          <div>
            <label className={labelClass}>Email</label>
            <input type="email" value={email} onChange={e => setEmail(e.target.value)}
              placeholder="nome@esempio.com" required className={inputClass} />
          </div>

          {isCondomino ? (
            <>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className={labelClass}>Nome</label>
                  <input type="text" value={nome} onChange={e => setNome(e.target.value)}
                    placeholder="Mario" required className={inputClass} />
                </div>
                <div>
                  <label className={labelClass}>Cognome</label>
                  <input type="text" value={cognome} onChange={e => setCognome(e.target.value)}
                    placeholder="Rossi" required className={inputClass} />
                </div>
              </div>

              <div>
                <label className={labelClass}>Codice Fiscale</label>
                <input type="text" value={codiceFiscale} onChange={e => setCodiceFiscale(e.target.value)}
                  placeholder="RSSMRA80A01H501U" required className={inputClass} />
              </div>

              <div>
                <label className={labelClass}>Telefono</label>
                <input type="tel" value={telefono} onChange={e => setTelefono(e.target.value)}
                  placeholder="3331234567" required className={inputClass} />
              </div>

              <div>
                <label className={labelClass}>PEC (opzionale)</label>
                <input type="email" value={pec} onChange={e => setPec(e.target.value)}
                  placeholder="mario.rossi@pec.it" className={inputClass} />
              </div>

              <div>
                <label className={labelClass}>Condominio</label>
                <select value={condominioId} onChange={e => setCondominioId(e.target.value)} required className={inputClass}>
                  <option value="" disabled>Seleziona il tuo condominio</option>
                  {condomini.map((c) => (
                    <option key={c.id} value={c.id}>{c.denominazione} — {c.indirizzo}</option>
                  ))}
                </select>
              </div>
            </>
          ) : (
            <>
              <div>
                <label className={labelClass}>Nome e cognome</label>
                <input type="text" value={fullName} onChange={e => setFullName(e.target.value)}
                  placeholder="Mario Rossi" className={inputClass} />
              </div>

              {isFornitore && (
                <div>
                  <label className={labelClass}>Servizi offerti</label>
                  {servizi.length === 0 ? (
                    <p className="text-xs text-muted-foreground">Nessun servizio disponibile al momento.</p>
                  ) : (
                    <div className="space-y-2 max-h-48 overflow-y-auto rounded-xl border border-input p-3">
                      {servizi.map((s) => (
                        <label key={s.id} className="flex items-center gap-2 text-sm text-foreground cursor-pointer">
                          <input
                            type="checkbox"
                            checked={serviziOfferti.includes(s.id)}
                            onChange={() => toggleServizio(s.id)}
                          />
                          {s.nome}
                        </label>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </>
          )}

          <div>
            <label className={labelClass}>Password</label>
            <div className="relative">
              <input type={showPassword ? "text" : "password"} value={password}
                onChange={e => setPassword(e.target.value)}
                placeholder="••••••••" required className={`${inputClass} pr-10`} />
              <button type="button" onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition">
                {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
            <p className="text-xs text-muted-foreground mt-1.5">
              Almeno 8 caratteri, una maiuscola, una minuscola e un numero.
            </p>
          </div>

          {error && (
            <div className="text-sm text-destructive bg-destructive/10 px-4 py-2.5 rounded-xl">{error}</div>
          )}

          <button type="submit" disabled={loading}
            className="w-full py-2.5 px-4 bg-primary text-primary-foreground font-semibold rounded-xl hover:opacity-90 transition disabled:opacity-50 disabled:cursor-not-allowed text-sm">
            {loading ? "Registrazione in corso..." : "Registrati"}
          </button>
        </form>

        <p className="text-center text-sm text-muted-foreground mt-6">
          Hai già un account?{" "}
          <Link to="/login" className="text-primary font-semibold hover:underline">
            Accedi
          </Link>
        </p>
      </div>
    </div>
  );
}
