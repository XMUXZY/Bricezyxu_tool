import { useState } from "react";

export default function SettingsPage() {
  const [updateStatus, setUpdateStatus] = useState("");
  const [checking, setChecking] = useState(false);

  const checkUpdate = async () => {
    setChecking(true);
    setUpdateStatus("正在检查更新...");
    try {
      const { check } = await import("@tauri-apps/plugin-updater");
      const update = await check();
      if (update) {
        setUpdateStatus(`发现新版本 ${update.version}！正在下载...`);
        await update.downloadAndInstall();
        setUpdateStatus("更新完成！重启应用后生效。");
        const { relaunch } = await import("@tauri-apps/plugin-process");
        setTimeout(() => relaunch(), 1500);
      } else {
        setUpdateStatus("✅ 当前已是最新版本");
      }
    } catch (e: any) {
      const msg = e?.toString?.() || "";
      if (msg.includes("fetch") || msg.includes("network") || msg.includes("connect")) {
        setUpdateStatus("⚠️ 无法连接更新服务器，请检查网络");
      } else {
        setUpdateStatus(`⚠️ ${msg}`);
      }
    }
    setChecking(false);
  };

  return (
    <div className="page-container">
      <h1 className="page-title">⚡ 设置</h1>

      <div className="card" style={{ marginTop: 15 }}>
        <h3 className="section-title">🔄 版本更新</h3>
        <div style={{ display: "flex", alignItems: "center", gap: 12, padding: "8px 0" }}>
          <button className="btn-primary" style={{ width: 160, height: 36 }} onClick={checkUpdate} disabled={checking}>
            {checking ? "检查中..." : "🔍 检查更新"}
          </button>
          {updateStatus && <span style={{ fontSize: 13, color: updateStatus.startsWith("✅") ? "#4ade80" : updateStatus.startsWith("⚠") ? "#fbbf24" : "#e0e0e0" }}>{updateStatus}</span>}
        </div>
      </div>

      <div className="card">
        <h3 className="section-title">💡 关于</h3>
        <div style={{ textAlign: "center", padding: "15px 0" }}>
          <div style={{ fontSize: 16, fontWeight: "bold", color: "#fff" }}>🎮 游戏运营工具合集</div>
          <div style={{ fontSize: 13, color: "#888", marginTop: 5 }}>版本 2.0.0</div>
          <div style={{ fontSize: 12, color: "#888", marginTop: 10, lineHeight: 1.6 }}>
            基于 React + Tauri 构建的模块化桌面工具集<br/>
            QQ华夏经典区运营专用
          </div>
        </div>
      </div>
    </div>
  );
}
