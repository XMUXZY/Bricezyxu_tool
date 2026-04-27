import { useState, useEffect } from "react";
import CalcPage from "../components/CalcPage";
import ResultBox from "../components/ResultBox";
import { SLOTS, ensureData, calcByMaterials, calcForTarget } from "../calculators/calcShengShi";

function fmt(v: number): string {
  if (v === Infinity) return "∞";
  return v >= 10000 ? v.toLocaleString("en-US", { maximumFractionDigits: 0 })
    : v.toLocaleString("en-US", { maximumFractionDigits: 1 });
}

function Tab1() {
  const [slot, setSlot] = useState(SLOTS[0].label);
  const [curLv, setCurLv] = useState("0");
  const [jf, setJf] = useState("");
  const [item, setItem] = useState("");
  const [result, setResult] = useState("");
  const [ready, setReady] = useState(false);
  useEffect(() => { ensureData().then(() => setReady(true)) }, []);
  const s = SLOTS.find(x => x.label === slot)!;

  const calc = async () => {
    if (!ready) { setResult("数据加载中…"); return; }
    const jfVal = jf.trim() ? parseFloat(jf) : Infinity;
    const itemVal = item.trim() ? parseFloat(item) : Infinity;
    const r = await calcByMaterials(slot, parseInt(curLv) || 0, jfVal, itemVal);
    const lines = [
      `━━━ 养成模拟结果 ━━━`, ``,
      `槽位：${slot}`, `可达等级：${r.level}级 (上限 ${s.maxLv})`,
      `从 ${curLv}级 出发，共推进 ${r.steps} 级`, ``,
      "━ 累计消耗(期望) ━", `  积分: ${fmt(r.totalJf)}`,
    ];
    if (s.hasItem) lines.push(`  ${s.itemName}: ${fmt(r.totalItem)}`);
    if (r.remainingJf !== Infinity && r.remainingJf > 0) lines.push(``, `剩余积分: ${fmt(r.remainingJf)}`);
    if (s.hasItem && r.remainingItem !== Infinity && r.remainingItem > 0) lines.push(`剩余${s.itemName}: ${fmt(r.remainingItem)}`);
    if (r.level >= s.maxLv) lines.push(``, `🎉 已满级！`);
    setResult(lines.join("\n"));
  };

  return (
    <div className="card">
      <h3 className="section-title">选择槽位</h3>
      <select className="select-field" value={slot} onChange={e => setSlot(e.target.value)}>
        {SLOTS.map(s => <option key={s.label} value={s.label}>{s.label} - {s.desc}</option>)}
      </select>
      <div className="grid-2" style={{ marginTop: 10 }}>
        <div><label className="input-label">当前等级</label><input className="input-field" value={curLv} onChange={e => setCurLv(e.target.value)} /></div>
        <div><label className="input-label">积分数量</label><input className="input-field" placeholder="留空=无限" value={jf} onChange={e => setJf(e.target.value)} /></div>
        {s.hasItem && <div><label className="input-label">{s.itemName}数量</label><input className="input-field" placeholder="留空=无限" value={item} onChange={e => setItem(e.target.value)} /></div>}
      </div>
      <button className="btn-primary btn-accent" style={{ marginTop: 12 }} onClick={calc}>▶ 计算可达等级</button>
      <div style={{ marginTop: 10 }}><ResultBox content={result} /></div>
    </div>
  );
}

function Tab2() {
  const [slot, setSlot] = useState(SLOTS[0].label);
  const [startLv, setStartLv] = useState("0");
  const [targetLv, setTargetLv] = useState("");
  const [result, setResult] = useState("");
  const [ready, setReady] = useState(false);
  useEffect(() => { ensureData().then(() => setReady(true)) }, []);
  const s = SLOTS.find(x => x.label === slot)!;

  const calc = async () => {
    if (!ready) { setResult("数据加载中…"); return; }
    const tgt = parseInt(targetLv) || s.maxLv;
    const sl = parseInt(startLv) || 0;
    if (tgt <= sl) { setResult("⚠️ 目标等级必须大于起始等级"); return; }
    if (tgt > s.maxLv) { setResult(`⚠️ ${s.label}最高${s.maxLv}级`); return; }
    const r = await calcForTarget(slot, sl, tgt);
    const lines = [
      `━━━ 材料需求汇总 ━━━`, ``,
      `槽位：${slot}`, `${sl}级 → ${tgt}级`, ``,
      `━ 所需材料(期望) ━`, `  积分总计: ${r.totalJf.toLocaleString()}`,
    ];
    if (s.hasItem) lines.push(`  ${s.itemName}总计: ${r.totalItem.toLocaleString()}`);
    setResult(lines.join("\n"));
  };

  return (
    <div className="card">
      <h3 className="section-title">等级范围</h3>
      <div className="grid-2">
        <div><label className="input-label">槽位</label>
          <select className="select-field" value={slot} onChange={e => { setSlot(e.target.value); setTargetLv("") }}>
            {SLOTS.map(s => <option key={s.label} value={s.label}>{s.label}</option>)}
          </select>
        </div>
        <div></div>
        <div><label className="input-label">起始等级</label><input className="input-field" value={startLv} onChange={e => setStartLv(e.target.value)} /></div>
        <div><label className="input-label">目标等级</label><input className="input-field" placeholder={String(s.maxLv)} value={targetLv} onChange={e => setTargetLv(e.target.value)} /></div>
      </div>
      <button className="btn-primary btn-green" style={{ marginTop: 12 }} onClick={calc}>▶ 计算所需材料</button>
      <div style={{ marginTop: 10 }}><ResultBox content={result} /></div>
    </div>
  );
}

export default function ToolEPage() {
  return <CalcPage
    title="💎 圣石养成计算器"
    subtitle="QQ华夏经典区 · 11件装备 × 3槽位 · 含10%暴击期望"
    tab1Label="📊 根据材料算可达等级"
    tab2Label="🎯 根据目标算所需材料"
    tab1Content={<Tab1 />}
    tab2Content={<Tab2 />}
    infoTitle="养成说明"
    infoItems={[
      "· 11件装备，每件3个槽位：圣石/玄石/罡石",
      "· 暴击机制：三类石头均有10%概率暴击3倍经验（期望×1.2）",
      "· 圣石(栏位1)：最高120级，只消耗积分，满级约206,904积分",
      "· 玄石(栏位2)：最高360级，积分+同系圣石，满级约185,533积分+62,595圣石",
      "· 罡石(栏位3)：最高150级，积分+罡石道具，满级约6,320积分+15,123道具",
      "· 所有消耗为含暴击修正的期望值",
    ]}
  />;
}
