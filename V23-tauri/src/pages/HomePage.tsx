export default function HomePage() {
  const hour = new Date().getHours();
  const greeting =
    hour < 6 ? "夜深了" : hour < 12 ? "上午好" : hour < 14 ? "中午好" : hour < 18 ? "下午好" : "晚上好";

  return (
    <div className="page-container">
      <div className="banner">
        <h1>{greeting}，欢迎使用游戏运营工具合集 👋</h1>
        <p>这里集成了日常运营所需的各类实用工具，助你高效完成工作。</p>
      </div>

      <h2 className="page-title" style={{ fontSize: 16, marginTop: 10 }}>ℹ️ 系统信息</h2>
      <div className="card" style={{ marginTop: 10 }}>
        <InfoRow label="应用版本" value="v2.0.0" />
        <InfoRow label="框架" value="React + Tauri" />
        <InfoRow label="主题" value="深色模式" />
        <InfoRow label="当前时间" value={new Date().toLocaleString("zh-CN")} />
      </div>

      <h2 className="page-title" style={{ fontSize: 16, marginTop: 20 }}>🧰 工具概览</h2>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))", gap: 10, marginTop: 10 }}>
        {tools.map((t) => (
          <div key={t.name} className="card" style={{ padding: "12px 16px", cursor: "default" }}>
            <span style={{ fontSize: 20 }}>{t.icon}</span>
            <div style={{ fontSize: 13, fontWeight: "bold", color: "#fff", marginTop: 4 }}>{t.name}</div>
            <div style={{ fontSize: 11, color: "#888", marginTop: 2 }}>{t.desc}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

function InfoRow({ label, value }: { label: string; value: string }) {
  return (
    <div style={{ display: "flex", padding: "6px 0" }}>
      <span style={{ width: 120, color: "#888", fontSize: 13 }}>{label}</span>
      <span style={{ fontSize: 13 }}>{value}</span>
    </div>
  );
}

const tools = [
  { icon: "🎨", name: "颜色解析", desc: "文字颜色代码预览" },
  { icon: "⚙️", name: "淬炼计算器", desc: "装备淬炼材料计算" },
  { icon: "⚔️", name: "重铸计算器", desc: "装备重铸材料计算" },
  { icon: "⭐", name: "星录养成", desc: "4部星录期望消耗" },
  { icon: "💎", name: "圣石养成", desc: "圣石/玄石/罡石计算" },
  { icon: "☪️", name: "星图养成", desc: "升重+锤炼消耗计算" },
  { icon: "🏔", name: "风水录养成", desc: "4张宝图材料计算" },
  { icon: "⚒️", name: "磨砺养成", desc: "宝石磨砺期望消耗" },
  { icon: "⚔️", name: "注灵养成", desc: "注灵套装材料计算" },
  { icon: "🔮", name: "遁甲养成", desc: "强运材料计算" },
  { icon: "🛡️", name: "守护神养成", desc: "请神符期望消耗" },
  { icon: "📜", name: "占测养成", desc: "占测材料计算" },
  { icon: "🏺", name: "法宝升阶", desc: "法宝碎片计算" },
  { icon: "🐯", name: "白虎星图", desc: "白虎锤炼消耗" },
];
