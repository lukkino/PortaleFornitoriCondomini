// frontend/src/components/Layout.jsx
import { useState, useEffect, useRef } from "react";
import { NavLink, useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../store/authStore";
import { useTheme } from "../store/themeStore";
import {
  LayoutDashboard,
  LogOut,
  ChevronLeft,
  ChevronRight,
  Sun,
  Moon,
  Building2,
  Menu,
  X,
} from "lucide-react";

const BASE_NAV_ITEMS = [
  { key: "dashboard", label: "Dashboard", Icon: LayoutDashboard, path: "/dashboard" },
];

const CONDOMINI_NAV_ITEM = { key: "condomini", label: "Condomini", Icon: Building2, path: "/condomini" };

const ROLE_LABELS = {
  admin: "Amministratore",
  condomino: "Condomino",
  fornitore: "Fornitore",
};

function SidebarContent({ collapsed, onNavClick, navItems }) {
  const { logoutUser } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logoutUser();
    navigate("/login");
  };

  return (
    <>
      <nav className="py-4 space-y-0.5 px-2 flex-1 overflow-y-auto">
        {navItems.map(({ key, label, Icon, path }) => (
          <NavLink
            key={key}
            to={path}
            onClick={onNavClick}
            className={({ isActive }) => `
              flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium
              transition-colors duration-150
              ${isActive
                ? "bg-primary text-primary-foreground"
                : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
              }
              ${collapsed ? "justify-center" : ""}
            `}
          >
            <Icon className="w-4 h-4 flex-shrink-0" />
            {!collapsed && <span className="flex-1">{label}</span>}
          </NavLink>
        ))}
      </nav>

      <div className="mx-2 border-t border-border" />

      <div className="px-2 py-3">
        <button
          onClick={handleLogout}
          className={`
            flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium w-full
            text-muted-foreground hover:bg-destructive/10 hover:text-destructive transition-colors
            ${collapsed ? "justify-center" : ""}
          `}
        >
          <LogOut className="w-4 h-4 flex-shrink-0" />
          {!collapsed && <span>Esci</span>}
        </button>
      </div>
    </>
  );
}

export default function Layout({ children, title }) {
  const { user } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const location = useLocation();
  const [collapsed, setCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const drawerRef = useRef(null);

  const navItems = [...BASE_NAV_ITEMS];
  if (user?.role === "admin" || user?.role === "condomino") {
    navItems.push(CONDOMINI_NAV_ITEM);
  }

  useEffect(() => {
    setMobileOpen(false);
  }, [location.pathname]);

  useEffect(() => {
    if (!mobileOpen) return;
    const handler = (e) => {
      if (drawerRef.current && !drawerRef.current.contains(e.target)) {
        setMobileOpen(false);
      }
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, [mobileOpen]);

  useEffect(() => {
    document.body.style.overflow = mobileOpen ? "hidden" : "";
    return () => { document.body.style.overflow = ""; };
  }, [mobileOpen]);

  return (
    <div className="flex min-h-screen bg-background text-foreground">
      <aside
        className={`
          hidden md:flex flex-col border-r border-border bg-card
          sticky top-0 h-screen
          transition-all duration-300
          ${collapsed ? "w-16" : "w-56"}
        `}
      >
        <div className={`flex items-center gap-3 px-4 py-5 border-b border-border flex-shrink-0 ${collapsed ? "justify-center" : ""}`}>
          <Building2 className="w-6 h-6 text-primary flex-shrink-0" />
          {!collapsed && (
            <span className="font-bold text-lg text-foreground leading-tight">Portale Condomini</span>
          )}
        </div>

        <SidebarContent collapsed={collapsed} onNavClick={undefined} navItems={navItems} />

        <div className="px-2 pb-3">
          <button
            onClick={() => setCollapsed(!collapsed)}
            className="flex items-center justify-center w-full px-3 py-2 rounded-xl text-muted-foreground hover:bg-accent transition-colors"
          >
            {collapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
          </button>
        </div>
      </aside>

      {mobileOpen && (
        <div className="fixed inset-0 bg-black/50 z-40 md:hidden"
          onClick={() => setMobileOpen(false)} />
      )}

      <div
        ref={drawerRef}
        className={`
          fixed top-0 left-0 h-full w-72 max-w-[85vw] z-50
          bg-card border-r border-border flex flex-col
          transition-transform duration-300 md:hidden
          ${mobileOpen ? "translate-x-0" : "-translate-x-full"}
        `}
      >
        <div className="flex items-center justify-between px-4 py-5 border-b border-border flex-shrink-0">
          <div className="flex items-center gap-3">
            <Building2 className="w-6 h-6 text-primary flex-shrink-0" />
            <span className="font-bold text-lg text-foreground">Portale Condomini</span>
          </div>
          <button
            onClick={() => setMobileOpen(false)}
            className="w-8 h-8 flex items-center justify-center rounded-xl hover:bg-accent transition-colors"
          >
            <X className="w-4 h-4 text-muted-foreground" />
          </button>
        </div>

        <SidebarContent collapsed={false} onNavClick={() => setMobileOpen(false)} navItems={navItems} />
      </div>

      <div className="flex-1 flex flex-col min-w-0">
        <header className="flex items-center justify-between px-4 md:px-6 py-3 md:py-4 border-b border-border bg-card sticky top-0 z-10">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setMobileOpen(true)}
              className="md:hidden w-9 h-9 flex items-center justify-center rounded-xl border border-border hover:bg-accent transition-colors"
            >
              <Menu className="w-4 h-4 text-muted-foreground" />
            </button>
            <h1 className="text-lg md:text-xl font-bold text-foreground">{title}</h1>
          </div>

          <div className="flex items-center gap-2 md:gap-3">
            <button
              onClick={toggleTheme}
              className="w-9 h-9 flex items-center justify-center rounded-xl border border-border hover:bg-accent transition-colors"
              title={theme === "dark" ? "Tema chiaro" : "Tema scuro"}
            >
              {theme === "dark" ? <Sun className="w-4 h-4 text-muted-foreground" /> : <Moon className="w-4 h-4 text-muted-foreground" />}
            </button>

            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center text-primary-foreground text-sm font-bold">
                {(user?.full_name || user?.email || "U")[0].toUpperCase()}
              </div>
              <div className="hidden md:flex flex-col leading-tight">
                <span className="text-sm font-medium text-foreground">{user?.full_name || user?.email}</span>
                {user?.role && <span className="text-xs text-muted-foreground">{ROLE_LABELS[user.role] || user.role}</span>}
              </div>
            </div>
          </div>
        </header>

        <main className="flex-1 p-4 md:p-6 overflow-auto">
          {children}
        </main>
      </div>
    </div>
  );
}
