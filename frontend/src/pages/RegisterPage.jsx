// frontend/src/pages/RegisterPage.jsx
import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { register, getMe } from "../api/auth";
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

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await register(email, password, fullName, role);
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

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-background">
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
            <label className="block text-sm font-medium text-foreground mb-1.5">Nome e cognome</label>
            <input type="text" value={fullName} onChange={e => setFullName(e.target.value)}
              placeholder="Mario Rossi" className={inputClass} />
          </div>

          <div>
            <label className="block text-sm font-medium text-foreground mb-1.5">Email</label>
            <input type="email" value={email} onChange={e => setEmail(e.target.value)}
              placeholder="nome@esempio.com" required className={inputClass} />
          </div>

          <div>
            <label className="block text-sm font-medium text-foreground mb-1.5">Sei</label>
            <select value={role} onChange={e => setRole(e.target.value)} className={inputClass}>
              <option value="condomino">Condomino</option>
              <option value="fornitore">Fornitore</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-foreground mb-1.5">Password</label>
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
