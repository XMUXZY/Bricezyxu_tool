import { useState } from "react";
import CalcPage from "../components/CalcPage";
import ResultBox from "../components/ResultBox";
import { MAX_WEIGHT, MAX_LEVEL, MAT_NAMES, OFFICIALS, calcForTarget, calcByMaterials } from "../calculators/calcStarMap";

function fmt(v:number):string { return v===Infinity?"∞":v>=10000?v.toLocaleString("en-US",{maximumFractionDigits:0}):v>=100?v.toLocaleString("en-US",{maximumFractionDigits:1}):v.toLocaleString("en-US",{maximumFractionDigits:1}); }
function fmtState(w:number,l:number):string { return w===0&&l===0?"未激活":`${w}重${l}级`; }

function Tab1() {
  const [sw,setSw]=useState("1"); const [sl,setSl]=useState("0");
  const [tw,setTw]=useState("10"); const [tl,setTl]=useState("6");
  const [mult,setMult]=useState("7");
  const [result,setResult]=useState("");

  const calc = () => {
    const n = parseInt(mult)||7;
    const r = calcForTarget(parseInt(sw)||0, parseInt(sl)||0, parseInt(tw)||10, parseInt(tl)||6, n);
    if (r.error) { setResult(`⚠️ ${r.error}`); return; }
    const s = r.single!, t = r.total!;
    const lines = [
      `━━━ 青龙星图 区间消耗 ━━━`,``,
      `从 ${fmtState(parseInt(sw)||0,parseInt(sl)||0)} → ${fmtState(parseInt(tw)||10,parseInt(tl)||6)}`,
      `计算方式：${n}个星官`,``
    ];
    lines.push("━ 单官期望消耗 ━");
    if (s.low>0)     lines.push(`  ${MAT_NAMES.low}(1-4重): ${fmt(s.low)}`);
    if (s.mid>0)     lines.push(`  ${MAT_NAMES.mid}(5-7重): ${fmt(s.mid)}`);
    if (s.high>0)    lines.push(`  ${MAT_NAMES.high}(8-10重): ${fmt(s.high)}`);
    if (s.guard>0)   lines.push(`  ${MAT_NAMES.guard}(保级): ${fmt(s.guard)}`);
    if (s.crystal>0) lines.push(`  ${MAT_NAMES.crystal}(升重): ${s.crystal}`);

    if (n > 1) {
      lines.push(``,`━ ${n}官总消耗 ━`);
      if (t.low>0)     lines.push(`  ${MAT_NAMES.low}: ${fmt(t.low)}`);
      if (t.mid>0)     lines.push(`  ${MAT_NAMES.mid}: ${fmt(t.mid)}`);
      if (t.high>0)    lines.push(`  ${MAT_NAMES.high}: ${fmt(t.high)}`);
      if (t.guard>0)   lines.push(`  ${MAT_NAMES.guard}: ${fmt(t.guard)}`);
      if (t.crystal>0) lines.push(`  ${MAT_NAMES.crystal}: ${t.crystal}`);
    }
    lines.push(``,`💡 以上为概率增量公式精确期望值`);
    setResult(lines.join("\n"));
  };

  return (
    <div className="card">
      <h3 className="section-title">区间消耗计算</h3>
      <div className="grid-2">
        <div><label className="input-label">起始重数(0=未激活)</label><input className="input-field" value={sw} onChange={e=>setSw(e.target.value)}/></div>
        <div><label className="input-label">起始等级(0=刚升重)</label><input className="input-field" value={sl} onChange={e=>setSl(e.target.value)}/></div>
        <div><label className="input-label">目标重数(1~10)</label><input className="input-field" value={tw} onChange={e=>setTw(e.target.value)}/></div>
        <div><label className="input-label">目标等级(1~6)</label><input className="input-field" value={tl} onChange={e=>setTl(e.target.value)}/></div>
      </div>
      <div style={{marginTop:8}}>
        <label className="input-label">计算星官数量</label>
        <select className="select-field" value={mult} onChange={e=>setMult(e.target.value)}>
          <option value="1">1个星官</option>
          <option value="7">7个星官(全部)</option>
        </select>
      </div>
      <button className="btn-primary btn-green" style={{marginTop:12}} onClick={calc}>▶ 计算所需材料</button>
      <div style={{marginTop:10}}><ResultBox content={result}/></div>
    </div>
  );
}

function Tab2() {
  const [sw,setSw]=useState("1"); const [sl,setSl]=useState("0");
  const [low,setLow]=useState(""); const [mid,setMid]=useState(""); const [high,setHigh]=useState(""); const [guard,setGuard]=useState("");
  const [mult,setMult]=useState("7");
  const [result,setResult]=useState("");

  const calc = () => {
    const n = parseInt(mult)||7;
    const mats = {
      low: low.trim() ? parseFloat(low) : Infinity,
      mid: mid.trim() ? parseFloat(mid) : Infinity,
      high: high.trim() ? parseFloat(high) : Infinity,
      guard: guard.trim() ? parseFloat(guard) : Infinity,
    };
    if (Object.values(mats).every(v=>v===Infinity)) { setResult("⚠️ 请至少输入一种材料的数量"); return; }
    const r = calcByMaterials(parseInt(sw)||0, parseInt(sl)||0, mats, n);
    if (r.error) { setResult(`⚠️ ${r.error}`); return; }
    const lines = [
      `━━━ 青龙星图 材料反推 ━━━`,``,
      `起点：${fmtState(parseInt(sw)||0,parseInt(sl)||0)}`,
      `计算方式：${n}个星官（材料平分）`,``,
      `🎯 可达：${fmtState(r.reachedW, r.reachedL)}`,``
    ];
    lines.push("━ 单官期望消耗 ━");
    const s = r.singleUsed;
    if (s.low>0)   lines.push(`  ${MAT_NAMES.low}: ${fmt(s.low)}`);
    if (s.mid>0)   lines.push(`  ${MAT_NAMES.mid}: ${fmt(s.mid)}`);
    if (s.high>0)  lines.push(`  ${MAT_NAMES.high}: ${fmt(s.high)}`);
    if (s.guard>0) lines.push(`  ${MAT_NAMES.guard}: ${fmt(s.guard)}`);

    if (n > 1) {
      lines.push(``,`━ ${n}官总消耗 ━`);
      const t = r.totalUsed;
      if (t.low>0)   lines.push(`  ${MAT_NAMES.low}: ${fmt(t.low)}`);
      if (t.mid>0)   lines.push(`  ${MAT_NAMES.mid}: ${fmt(t.mid)}`);
      if (t.high>0)  lines.push(`  ${MAT_NAMES.high}: ${fmt(t.high)}`);
      if (t.guard>0) lines.push(`  ${MAT_NAMES.guard}: ${fmt(t.guard)}`);
    }
    setResult(lines.join("\n"));
  };

  return (
    <div className="card">
      <h3 className="section-title">材料反推可达等级</h3>
      <div className="grid-2">
        <div><label className="input-label">当前重数(0=未激活)</label><input className="input-field" value={sw} onChange={e=>setSw(e.target.value)}/></div>
        <div><label className="input-label">当前等级(0=刚升重)</label><input className="input-field" value={sl} onChange={e=>setSl(e.target.value)}/></div>
      </div>
      <h3 className="section-title" style={{marginTop:10}}>拥有材料（留空=无限）</h3>
      <div className="grid-2">
        <div><label className="input-label">{MAT_NAMES.low}(1-4重)</label><input className="input-field" placeholder="留空=无限" value={low} onChange={e=>setLow(e.target.value)}/></div>
        <div><label className="input-label">{MAT_NAMES.mid}(5-7重)</label><input className="input-field" placeholder="留空=无限" value={mid} onChange={e=>setMid(e.target.value)}/></div>
        <div><label className="input-label">{MAT_NAMES.high}(8-10重)</label><input className="input-field" placeholder="留空=无限" value={high} onChange={e=>setHigh(e.target.value)}/></div>
        <div><label className="input-label">{MAT_NAMES.guard}(保级)</label><input className="input-field" placeholder="留空=无限" value={guard} onChange={e=>setGuard(e.target.value)}/></div>
      </div>
      <div style={{marginTop:8}}>
        <label className="input-label">计算星官数量</label>
        <select className="select-field" value={mult} onChange={e=>setMult(e.target.value)}>
          <option value="1">1个星官</option>
          <option value="7">7个星官(全部)</option>
        </select>
      </div>
      <button className="btn-primary btn-accent" style={{marginTop:12}} onClick={calc}>▶ 计算可达等级</button>
      <div style={{marginTop:10}}><ResultBox content={result}/></div>
    </div>
  );
}

export default function ToolStarMapPage() {
  return <CalcPage
    title="☪️ 青龙星图计算器"
    subtitle="QQ华夏手游 · 7个星官 × 10重6级 · 概率增量公式精确期望值"
    tab1Label="🎯 区间消耗计算"
    tab2Label="📦 材料反推等级"
    tab1Content={<Tab1/>}
    tab2Content={<Tab2/>}
    infoTitle="养成说明"
    infoItems={[
      "· 7个星官，每个10重×6级，各星官独立养成",
      "· 升重消耗青龙碎晶：升至X重需 X×10 颗/星官",
      "· 锤炼材料分段：碧木(1-4重) → 云隐(5-7重) → 龙威(8-10重)",
      "· 保级材料（青龙之灵）全段消耗，1级也需消耗",
      "· 概率机制：初始70%~30%，失败+15%，上限100%",
      "· 本表期望值基于概率增量公式精确计算，误差<0.1%",
    ]}
  />;
}
