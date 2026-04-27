import { useState } from "react";
import CalcPage from "../components/CalcPage";
import ResultBox from "../components/ResultBox";
import { SET_ORDER, getSetInfo, getMatNames, calcByMaterials, calcByTarget } from "../calculators/calcZhuLing";

function Tab1() {
  const [setName,setSetName]=useState("神农"); const [startLv,setStartLv]=useState("0");
  const [matVals,setMatVals]=useState<Record<string,string>>({}); const [result,setResult]=useState("");
  const info = getSetInfo(setName);
  const mats = getMatNames(setName);
  const allMats = [...new Set([...mats.openMats, ...mats.refreshMats, mats.guardMat])];

  const calc = () => {
    const holdings: Record<string,number> = {};
    for (const m of allMats) holdings[m] = parseInt(matVals[m]||"")||0;
    const r = calcByMaterials(setName, parseInt(startLv)||0, holdings);
    if (r.error) { setResult(`⚠️ ${r.error}`); return; }
    const lines = [`✅ 计算完成`,``,`套装：${setName} (解锁Lv.${info?.unlockLv})`,`起始：Lv.${startLv} → 可达：Lv.${r.reachLv}`,`提升：${r.reachLv!-(parseInt(startLv)||0)} 级`,``,`【升级路径】`];
    for (const row of r.tableData||[]) {
      const openStr = `开启${row.openMat}×${row.openNeed}`;
      const refreshStr = `重刷${row.refreshMat}×${row.refreshNeed}`;
      const guardStr = `${row.guardMat}×${row.guardNeed}`;
      lines.push(`  Lv.${row.lv}: ${openStr} + ${refreshStr} + ${guardStr}  ${row.status}`);
    }
    if (r.reachLv===10) lines.push(``,`🎉 已满级！`);
    setResult(lines.join("\n"));
  };

  return (
    <div className="card">
      <h3 className="section-title">选择套装</h3>
      <div className="grid-2">
        <div><label className="input-label">注灵套装</label>
          <select className="select-field" value={setName} onChange={e=>{setSetName(e.target.value);setMatVals({})}}>
            {SET_ORDER.map(s=><option key={s}>{s}</option>)}
          </select>
        </div>
        <div><label className="input-label">起始等级(0-9)</label>
          <input className="input-field" value={startLv} onChange={e=>setStartLv(e.target.value)}/>
        </div>
      </div>
      {info && <p style={{color:"#e94560",fontSize:11,margin:"6px 0"}}>解锁等级: {info.unlockLv} | 保底材料: {mats.guardMat}</p>}
      <h3 className="section-title" style={{marginTop:10}}>持有材料</h3>
      {allMats.map(m=>(
        <div key={m} style={{marginBottom:6}}>
          <label className="input-label">{m}</label>
          <input className="input-field" value={matVals[m]||""} placeholder="0" onChange={e=>setMatVals({...matVals,[m]:e.target.value})}/>
        </div>
      ))}
      <button className="btn-primary" style={{marginTop:12}} onClick={calc}>▶ 计算可达等级</button>
      <div style={{marginTop:10}}><ResultBox content={result}/></div>
    </div>
  );
}

function Tab2() {
  const [setName,setSetName]=useState("神农"); const [sl,setSl]=useState("0"); const [tl,setTl]=useState("10");
  const [result,setResult]=useState("");
  const info = getSetInfo(setName);

  const calc = () => {
    const r = calcByTarget(setName, parseInt(sl)||0, parseInt(tl)||10);
    if (r.error) { setResult(`⚠️ ${r.error}`); return; }
    const lines = [`✅ 计算完成`,``,`套装：${setName} (解锁Lv.${r.unlockLv})`,`Lv.${sl} → Lv.${tl}`,``,`【总消耗汇总】(全11部位×期望次数)`];
    for (const [k,v] of Object.entries(r.totals!)) {
      lines.push(`  ${k}: ${v.toLocaleString()}`);
    }
    lines.push(``,`【逐级明细】`);
    for (const row of r.tableData||[]) {
      lines.push(`  Lv.${row.lv}: 开启${row.openMat}×${row.openNeed} + 重刷${row.refreshMat}×${row.refreshNeed} + ${row.guardMat}×${row.guardNeed}`);
    }
    setResult(lines.join("\n"));
  };

  return (
    <div className="card">
      <h3 className="section-title">目标注灵状态</h3>
      <div className="grid-2">
        <div><label className="input-label">注灵套装</label>
          <select className="select-field" value={setName} onChange={e=>setSetName(e.target.value)}>
            {SET_ORDER.map(s=><option key={s}>{s}</option>)}
          </select>
        </div>
        <div></div>
        <div><label className="input-label">起始等级(0-9)</label><input className="input-field" value={sl} onChange={e=>setSl(e.target.value)}/></div>
        <div><label className="input-label">目标等级(1-10)</label><input className="input-field" value={tl} onChange={e=>setTl(e.target.value)}/></div>
      </div>
      {info && <p style={{color:"#e94560",fontSize:11,margin:"6px 0"}}>解锁等级: {info.unlockLv}</p>}
      <button className="btn-primary btn-green" style={{marginTop:12}} onClick={calc}>▶ 计算所需材料</button>
      <div style={{marginTop:10}}><ResultBox content={result}/></div>
    </div>
  );
}

export default function ToolZhuLingPage() {
  return <CalcPage
    title="⚔️ 注灵养成计算器"
    subtitle="QQ华夏经典区 · 8套注灵 × 10级 × 11部位 · 期望值计算"
    tab1Label="📊 根据材料计算等级"
    tab2Label="🎯 根据目标计算材料"
    tab1Content={<Tab1/>}
    tab2Content={<Tab2/>}
    infoTitle="使用说明"
    infoItems={[
      "· 8套注灵：神农→女娲→伏羲→轩辕→鸿钧→混元→夸父→蚩尤",
      "· 每级消耗 = 开启材料(11部位) + 重刷主材料(期望) + 保底材料(期望)",
      "· 神农/女娲/伏羲/轩辕：1-5级和6-10级使用不同材料",
      "· 鸿钧/混元/夸父/蚩尤：开启和重刷使用同一主材料",
      "· 所有重刷消耗为使用保底材料的期望值（期望6次刷出）",
    ]}
  />;
}
