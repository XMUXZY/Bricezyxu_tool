import { BrowserRouter, Routes, Route, NavLink, useLocation } from "react-router-dom";
import HomePage from "./pages/HomePage";
import ToolBPage from "./pages/ToolBPage";
import ToolCPage from "./pages/ToolCPage";
import ToolDPage from "./pages/ToolDPage";
import ToolEPage from "./pages/ToolEPage";
import ToolStarMapPage from "./pages/ToolStarMapPage";
import ToolFengShuiPage from "./pages/ToolFengShuiPage";
import ToolGemGrindPage from "./pages/ToolGemGrindPage";
import ToolZhuLingPage from "./pages/ToolZhuLingPage";
import ToolDunJiaPage from "./pages/ToolDunJiaPage";
import ToolGuardianPage from "./pages/ToolGuardianPage";
import ToolZhanCePage from "./pages/ToolZhanCePage";
import ToolFaBaoPage from "./pages/ToolFaBaoPage";
import ToolBaihuStarPage from "./pages/ToolBaihuStarPage";
import ToolColorPage from "./pages/ToolColorPage";
import SettingsPage from "./pages/SettingsPage";

const NAV_ITEMS = [
  { path: "/", label: "首  页", icon: "🏠" },
  { path: "/color", label: "颜色解析", icon: "🎨" },
  { path: "/refining", label: "淬炼计算器", icon: "⚙️" },
  { path: "/reforge", label: "重铸计算器", icon: "⚔️" },
  { path: "/xinlu", label: "星录养成", icon: "⭐" },
  { path: "/shengshi", label: "圣石养成", icon: "💎" },
  { path: "/starmap", label: "青龙星图", icon: "☪️" },
  { path: "/fengshui", label: "风水录养成", icon: "🏔" },
  { path: "/gemgrind", label: "磨砺养成", icon: "⚒️" },
  { path: "/zhuling", label: "注灵养成", icon: "⚔️" },
  { path: "/dunjia", label: "遁甲养成", icon: "🔮" },
  { path: "/guardian", label: "守护神养成", icon: "🛡️" },
  { path: "/zhance", label: "占测养成", icon: "📜" },
  { path: "/fabao", label: "法宝升阶", icon: "🏺" },
  { path: "/baihu", label: "白虎星图", icon: "🐯" },
];

const BOTTOM_NAV = [
  { path: "/settings", label: "设  置", icon: "⚡" },
];

function NavButton({ path, label, icon }: { path: string; label: string; icon: string }) {
  return (
    <NavLink
      to={path}
      end={path === "/"}
      className={({ isActive }) => `nav-btn${isActive ? " active" : ""}`}
    >
      <span className="icon">{icon}</span>
      {label}
    </NavLink>
  );
}

function AppContent() {
  return (
    <div className="app-layout">
      <nav className="nav-sidebar">
        <div className="nav-header">
          <div className="logo">🎮</div>
          <div className="title">运营工具合集</div>
          <div className="subtitle">Game Ops Toolkit</div>
        </div>
        <div className="nav-items">
          {NAV_ITEMS.map((item) => (
            <NavButton key={item.path} {...item} />
          ))}
        </div>
        <div className="nav-bottom">
          {BOTTOM_NAV.map((item) => (
            <NavButton key={item.path} {...item} />
          ))}
          <div className="nav-version">v2.0.0</div>
        </div>
      </nav>
      <main className="content-area">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/color" element={<ToolColorPage />} />
          <Route path="/refining" element={<ToolBPage />} />
          <Route path="/reforge" element={<ToolCPage />} />
          <Route path="/xinlu" element={<ToolDPage />} />
          <Route path="/shengshi" element={<ToolEPage />} />
          <Route path="/starmap" element={<ToolStarMapPage />} />
          <Route path="/fengshui" element={<ToolFengShuiPage />} />
          <Route path="/gemgrind" element={<ToolGemGrindPage />} />
          <Route path="/zhuling" element={<ToolZhuLingPage />} />
          <Route path="/dunjia" element={<ToolDunJiaPage />} />
          <Route path="/guardian" element={<ToolGuardianPage />} />
          <Route path="/zhance" element={<ToolZhanCePage />} />
          <Route path="/fabao" element={<ToolFaBaoPage />} />
          <Route path="/baihu" element={<ToolBaihuStarPage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Routes>
      </main>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AppContent />
    </BrowserRouter>
  );
}
