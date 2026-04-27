export default function SettingsPage() {
  return (
    <div className="page-container">
      <h1 className="page-title">⚡ 设置</h1>
      <div className="card" style={{ marginTop: 15 }}>
        <h3 className="section-title">🎨 外观设置</h3>
        <div style={{ display: "flex", alignItems: "center", padding: "8px 0" }}>
          <span style={{ width: 120, fontSize: 14 }}>主题模式</span>
          <select className="select-field" style={{ width: 160 }} defaultValue="dark">
            <option value="dark">深色</option>
            <option value="light">浅色</option>
          </select>
        </div>
      </div>

      <div className="card">
        <h3 className="section-title">💡 关于</h3>
        <div style={{ textAlign: "center", padding: "15px 0" }}>
          <div style={{ fontSize: 16, fontWeight: "bold", color: "#fff" }}>🎮 游戏运营工具合集</div>
          <div style={{ fontSize: 13, color: "#888", marginTop: 5 }}>版本 2.0.0</div>
          <div style={{ fontSize: 12, color: "#888", marginTop: 10, lineHeight: 1.6 }}>
            基于 React + Tauri 构建的模块化桌面工具集<br/>
            从 Python + CustomTkinter 改造而来<br/>
            可随时扩展新的运营工具模块
          </div>
        </div>
      </div>
    </div>
  );
}
