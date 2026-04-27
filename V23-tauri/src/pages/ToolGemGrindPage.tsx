import { useState } from "react";
import CalcPage from "../components/CalcPage";
import ResultBox from "../components/ResultBox";
import { MAX_LEVEL, COPPER_PER_LEVEL, getData, calcByMaterials, calcForTarget } from "../calculators/calcGemGrind";

function fmt(n:number):string { return n>=10000?n.toLocaleString("en-US",{maximumFractionDigits:0}):n>=100?n.toLocaleString("en-US",{maximumFractionDigits:1}):n.toFixed(1); }

function Tab1() {
  const [curLv,setCurLv]=useState("0"); const [pos,setPos]=useState("12"); const [mode,setMode]=useState("exp");
  const [matVals,setMatVals]=useState<Record<string,string>>({}); const [copper,setCopper]=useState("");
  const [result,setResult]=useState("");

  const isPos3 = pos==="3";
  const matNames = isPos3 ? ["邃夜黑砂","乌金玉砂","黑曜灵砂"] : ["青暗紫砂","墨紫玉砂","琉璃灵砂"];

  const calc = () => {
    const mats: Record<string,number> = {};
    for (const m of matNames) mats[m] = matVals[m]?.trim() ? parseFloat(matVals[m]) : Infinity;
    const c = copper.trim() ? parseFloat(copper)*10000 : Infinity;
    const r = calcByMaterials(parseInt(curLv)||0, isPos3, mode==="exp", mats, c);
    if (r.error) { setResult(`⚠️ ${r.error}`); return; }
    const lines = [`✅ 计算完成`,``,`起始: ${curLv}级 → 可达: ${r.finalLevel}级`,`提升: ${r.finalLevel-(parseInt(curLv)||0)}级`,`镶嵌位: ${isPos3?"位置3":"位置1/2"} | 模式: ${mode==="exp"?"期望值":"确定值"}`,``,"【累计消耗】"];
    for (const [k,v] of Object.entries(r.usedMats)) { if (v>0) lines.push(`  ${k}: ${fmt(v)}`); }
    if (r.usedCopper>0) lines.push(`  铜钱: ${fmt(r.usedCopper)} (${fmt(r.usedCopper/10000)}万)`);
    setResult(lines.join("\n"));
  };

  return (
    <div className="card">
      <h3 className="section-title">当前磨砺状态</h3>
      <div className="grid-2">
        <div><label className="input-label">当前等级(0~40)</label><input className="input-field" value={curLv} onChange={e=>setCurLv(e.target.value)}/></div>
        <div><label className="input-label">镶嵌位置</label><select className="select-field" value={pos} onChange={e=>setPos(e.target.value)}><option value="12">位置1/2</option><option value="3">位置3</option></select></div>
        <div><label className="input-label">计算模式</label><select className="select-field" value={mode} onChange={e=>setMode(e.target.value)}><option value="exp">期望值（含概率修正）</option><option value="det">确定值（不考虑失败）</option></select></div>
      </div>
      <h3 className="section-title" style={{marginTop:10}}>拥有材料（留空=无限）</h3>
      {matNames.map(m=>(<div key={m} style={{marginBottom:6}}><label className="input-label">{m}</label><input className="input-field" placeholder="留空=不限" value={matVals[m]||""} onChange={e=>setMatVals({...matVals,[m]:e.target.value})}/></div>))}
      <div><label className="input-label">铜钱(万)</label><input className="input-field" placeholder="留空=不限" value={copper} onChange={e=>setCopper(e.target.value)}/></div>
      <button className="btn-primary" style={{marginTop:12}} onClick={calc}>▶ 计算可达等级</button>
      <div style={{marginTop:10}}><ResultBox content={result}/></div>
    </div>
  );
}

function Tab2() {
  const [startLv,setStartLv]=useState("0"); const [targetLv,setTargetLv]=useState("40"); const [pos,setPos]=useState("12");
  const [result,setResult]=useState("");

  const calc = () => {
    const r = calcForTarget(parseInt(startLv)||0, parseInt(targetLv)||40, pos==="3");
    if (r.error) { setResult(`⚠️ ${r.error}`); return; }
    const lines = [`✅ 计算完成`,``,`Lv.${startLv} → Lv.${targetLv}`,``,`【确定消耗】(不考虑失败)`];
    for (const [k,v] of Object.entries(r.detMats!)) lines.push(`  ${k}: ${v}`);
    lines.push(`  铜钱: ${r.totalCopper!.toLocaleString()} (${(r.totalCopper!/10000).toFixed(1)}万)`,``,`【期望消耗】(含失败概率)`);
    for (const [k,v] of Object.entries(r.expMats!)) { const d = r.detMats![k]||0; lines.push(`  ${k}: ${fmt(v)} (+${fmt(v-d)})`); }
    setResult(lines.join("\n"));
  };

  return (
    <div className="card">
      <h3 className="section-title">目标设定</h3>
      <div className="grid-2">
        <div><label className="input-label">起始等级</label><input className="input-field" value={startLv} onChange={e=>setStartLv(e.target.value)}/></div>
        <div><label className="input-label">目标等级</label><input className="input-field" value={targetLv} onChange={e=>setTargetLv(e.target.value)}/></div>
        <div><label className="input-label">镶嵌位置</label><select className="select-field" value={pos} onChange={e=>setPos(e.target.value)}><option value="12">位置1/2</option><option value="3">位置3</option></select></div>
      </div>
      <button className="btn-primary btn-green" style={{marginTop:12}} onClick={calc}>▶ 计算所需材料</button>
      <div style={{marginTop:10}}><ResultBox content={result}/></div>
    </div>
  );
}

export default function ToolGemGrindPage() {
  return <CalcPage title="⚒️ 宝石磨砺养成计算器" subtitle="QQ华夏手游 · 40级上限 · 含成功率期望值计算" tab1Label="📊 根据材料算可达等级" tab2Label="🎯 根据目标算所需材料" tab1Content={<Tab1/>} tab2Content={<Tab2/>} infoTitle="磨砺规则" infoItems={["· 磨砺共40级，分3个材料阶段（1-20 / 21-29 / 30-40）","· 每次升级消耗铜钱10000 + 对应材料","· Lv1-4必成功，Lv5起有失败概率","· 期望值 = 单次消耗量 ÷ 成功率"]} />;
}
