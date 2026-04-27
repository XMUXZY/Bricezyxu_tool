import { useState } from "react";
import CalcPage from "../components/CalcPage";
import ResultBox from "../components/ResultBox";
import { MAP_ORDER, MAP_POINTS, POINTS, calcMapTarget, calcMapByMaterials, getMapMaterials } from "../calculators/calcFengShui";

function Tab1() {
  const [map, setMap] = useState("北郡");
  const [startS, setStartS] = useState("1");
  const [targetS, setTargetS] = useState("6");
  const [result, setResult] = useState("");

  const calc = () => {
    const ss = parseInt(startS) || 1, ts = parseInt(targetS) || 6;
    if (ss < 1 || ss > 6 || ts < 1 || ts > 6) { setResult("⚠️ 星级范围 1~6"); return; }
    if (ts <= ss) { setResult("⚠️ 目标星级必须大于起始星级"); return; }
    // 用户输入1~6星，内部映射为0~5下标
    const pids = MAP_POINTS[map] || [];
    const r = calcMapTarget(map, ss - 1, ts - 1);

    const lines = [`━━━ 目标规划结果 ━━━`, ``, `宝图：${map} · ${pids.length}个风水点`, `从 ${ss}星 → ${ts}星`, ``];
    lines.push("各点明细：");
    for (const d of r.details) {
      let s = `  ${d.name}：${d.mainMat} ×${d.mainCost}`;
      if (d.subMat && d.subCost > 0) s += ` + ${d.subMat} ×${d.subCost}`;
      lines.push(s);
    }
    lines.push("", "━━ 材料汇总 ━━");
    for (const [name, cnt] of Object.entries(r.matSummary).sort()) {
      lines.push(`  ${name}: ${cnt.toLocaleString()}`);
    }
    setResult(lines.join("\n"));
  };

  return (
    <div className="card">
      <h3 className="section-title">选择宝图</h3>
      <select className="select-field" value={map} onChange={e => setMap(e.target.value)}>
        {MAP_ORDER.map(m => <option key={m}>{m}</option>)}
      </select>
      <div className="grid-2" style={{ marginTop: 10 }}>
        <div><label className="input-label">起始星级(1~5)</label><input className="input-field" value={startS} onChange={e => setStartS(e.target.value)} /></div>
        <div><label className="input-label">目标星级(2~6)</label><input className="input-field" value={targetS} onChange={e => setTargetS(e.target.value)} /></div>
      </div>
      <button className="btn-primary btn-green" style={{ marginTop: 12 }} onClick={calc}>▶ 计算所需材料</button>
      <div style={{ marginTop: 10 }}><ResultBox content={result} /></div>
    </div>
  );
}

function Tab2() {
  const [map, setMap] = useState("北郡");
  const [curS, setCurS] = useState("1");
  const [matInputs, setMatInputs] = useState<Record<string, string>>({});
  const [result, setResult] = useState("");
  const mats = getMapMaterials(map);

  const calc = () => {
    const cs = parseInt(curS) || 1;
    if (cs < 1 || cs > 6) { setResult("⚠️ 星级范围 1~6"); return; }
    const amounts: Record<string, number> = {};
    for (const m of mats) {
      const v = parseInt(matInputs[m] || "");
      if (!isNaN(v)) amounts[m] = v;
    }
    if (Object.keys(amounts).length === 0) { setResult("⚠️ 请输入材料数量"); return; }

    // 用户输入1~6星，内部映射为0~5
    const r = calcMapByMaterials(map, cs - 1, amounts);
    const lines = [`━━━ 资源评估结果 ━━━`, ``, `宝图：${map}`, `从 ${cs}星 出发`, ``];
    for (const res of r.results) {
      const displayStar = res.reachStar + 1; // 内部0~5 → 显示1~6
      const usedStr = Object.entries(res.used).map(([k, v]) => `${k}×${v}`).join(" + ");
      lines.push(`  ${res.name}: 可达${displayStar}星${usedStr ? " (消耗 " + usedStr + ")" : ""}`);
    }
    lines.push("", "━━ 剩余材料 ━━");
    for (const m of mats) {
      if ((r.remaining[m] ?? 0) > 0) lines.push(`  ${m}: ${r.remaining[m]}`);
    }
    setResult(lines.join("\n"));
  };

  return (
    <div className="card">
      <h3 className="section-title">资源评估</h3>
      <select className="select-field" value={map} onChange={e => { setMap(e.target.value); setMatInputs({}) }}>
        {MAP_ORDER.map(m => <option key={m}>{m}</option>)}
      </select>
      <div style={{ marginTop: 8 }}><label className="input-label">当前星级(1~5)</label><input className="input-field" value={curS} onChange={e => setCurS(e.target.value)} /></div>
      <h3 className="section-title" style={{ marginTop: 10 }}>持有材料</h3>
      {mats.map(m => (
        <div key={m} style={{ marginBottom: 6 }}>
          <label className="input-label">{m}</label>
          <input className="input-field" placeholder="数量" value={matInputs[m] || ""} onChange={e => setMatInputs({ ...matInputs, [m]: e.target.value })} />
        </div>
      ))}
      <button className="btn-primary" style={{ marginTop: 12 }} onClick={calc}>▶ 计算可达星级</button>
      <div style={{ marginTop: 10 }}><ResultBox content={result} /></div>
    </div>
  );
}

export default function ToolFengShuiPage() {
  return <CalcPage
    title="🏔 风水录养成计算器"
    subtitle="QQ华夏经典区 · 4张宝图 · 24个风水点 · 含卡点消耗"
    tab1Label="🎯 目标规划（算材料）"
    tab2Label="📊 资源评估（算可达星级）"
    tab1Content={<Tab1 />}
    tab2Content={<Tab2 />}
    infoTitle="养成说明"
    infoItems={[
      "· 4张宝图：北郡 / 琅琊盆地 / 昆仑 / 轩辕",
      "· 每张宝图含6个风水点，各点独立升级(1→6星)",
      "· 北郡各点有2星卡点（额外消耗神兽石）",
      "· 满星总消耗：北郡2,364 / 琅琊4,113+5,484 / 昆仑6,520+5,216 / 轩辕15,480+7,740",
    ]}
  />;
}
