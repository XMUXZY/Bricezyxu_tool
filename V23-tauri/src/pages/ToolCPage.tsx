import { useState } from "react";
import CalcPage from "../components/CalcPage";
import ResultBox from "../components/ResultBox";
import { MATERIAL_B_NAME, EQUIPMENT_COUNT, formatNum, calcReforgeByMaterials, calcMaterialsForTarget } from "../calculators/calcReforge";

const MAT_TYPES = ["不灭离炎","青璃焰光","冥雷寒铁","辉光玄铁","坠影紫晶","绯云玄晶"];

function Tab1() {
  const [initLevel,setInitLevel] = useState("0");
  const [initStage,setInitStage] = useState("0");
  const [matType,setMatType] = useState("不灭离炎");
  const [matA,setMatA] = useState("");
  const [matB,setMatB] = useState("");
  const [result,setResult] = useState("");

  const calc = () => {
    const il = parseInt(initLevel)||0, is_ = parseInt(initStage)||0;
    const hasA = matA.trim()!=="", hasB = matB.trim()!=="";
    if (!hasA && !hasB) { setResult("⚠️ 材料A和B不能同时为空"); return; }
    const ra = hasA ? parseFloat(matA) : Infinity;
    const rb = hasB ? parseFloat(matB) : Infinity;
    const r = calcReforgeByMaterials(il, is_, matType, ra, rb);
    if (r.error) { setResult(`⚠️ ${r.error}`); return; }
    const lines = [`━━━ 重铸结果 ━━━`,``,`最高可达到：${r.currentLevel} 级 ${r.currentStage} 阶段`,`(从 ${il} 级 ${is_} 阶段出发)`,``,`━━━ 累计消耗 ━━━`,`材料A (${matType}): ${formatNum(r.totalUsedA!)}`,`材料B (${MATERIAL_B_NAME}): ${formatNum(r.totalUsedB!)}`,``];
    if (r.remainingA !== Infinity && r.remainingA! > 0.0001) lines.push(`剩余材料A: ${formatNum(r.remainingA!)}`);
    if (r.remainingB !== Infinity && r.remainingB! > 0.0001) lines.push(`剩余材料B: ${formatNum(r.remainingB!)}`);
    lines.push(``,`(以上为 ${EQUIPMENT_COUNT} 件装备的总消耗)`);
    setResult(lines.join("\n"));
  };

  return (
    <div className="card">
      <h3 className="section-title">📊 根据材料计算可达重铸等级</h3>
      <div className="grid-2">
        <div><label className="input-label">初始等级 (0-30)</label><input className="input-field" value={initLevel} onChange={e=>setInitLevel(e.target.value)}/></div>
        <div><label className="input-label">初始阶段 (0-5)</label><input className="input-field" value={initStage} onChange={e=>setInitStage(e.target.value)}/></div>
        <div><label className="input-label">重铸材料A类型</label><select className="select-field" value={matType} onChange={e=>setMatType(e.target.value)}>{MAT_TYPES.map(m=><option key={m}>{m}</option>)}</select></div>
        <div></div>
        <div><label className="input-label">材料A数量</label><input className="input-field" placeholder="留空=无限" value={matA} onChange={e=>setMatA(e.target.value)}/></div>
        <div><label className="input-label">保底材料B数量</label><input className="input-field" placeholder="留空=无限" value={matB} onChange={e=>setMatB(e.target.value)}/></div>
      </div>
      <button className="btn-primary" style={{marginTop:12}} onClick={calc}>▶  计算可达到的重铸等级</button>
      <div style={{marginTop:10}}><ResultBox content={result}/></div>
    </div>
  );
}

function Tab2() {
  const [sl,setSl] = useState("0"); const [ss,setSs] = useState("0");
  const [tl,setTl] = useState("30"); const [ts,setTs] = useState("0");
  const [matType,setMatType] = useState("不灭离炎");
  const [result,setResult] = useState("");

  const calc = () => {
    const r = calcMaterialsForTarget(parseInt(sl)||0, parseInt(ss)||0, parseInt(tl)||30, parseInt(ts)||0, matType);
    if (r.error) { setResult(`⚠️ ${r.error}`); return; }
    const lines = [`━━━ 材料需求 ━━━`,``,`从 ${sl} 级 ${ss} 阶段 → ${tl} 级 ${ts} 阶段`,`共需提升 ${r.stagesCount} 个阶段`,``,`┌─────────────────────────────┐`,`│ 各材料原始需求 (×${EQUIPMENT_COUNT}件)       │`,`├─────────────────────────────┤`];
    for (const [name,amt] of Object.entries(r.totalMaterials!)) { if (amt > 0.0001) lines.push(`│ ${name}  ${formatNum(amt)}`); }
    lines.push(`└─────────────────────────────┘`);
    if (r.convertedTotal! > 0.0001) lines.push(``,`▸ 转换为 [${matType}] 总计: ${formatNum(r.convertedTotal!)}`);
    lines.push(``,`(以上为 ${EQUIPMENT_COUNT} 件装备的总消耗)`);
    setResult(lines.join("\n"));
  };

  return (
    <div className="card">
      <h3 className="section-title">🎯 根据目标计算所需材料</h3>
      <div className="grid-2">
        <div><label className="input-label">初始等级</label><input className="input-field" value={sl} onChange={e=>setSl(e.target.value)}/></div>
        <div><label className="input-label">初始阶段</label><input className="input-field" value={ss} onChange={e=>setSs(e.target.value)}/></div>
        <div><label className="input-label">目标等级</label><input className="input-field" value={tl} onChange={e=>setTl(e.target.value)}/></div>
        <div><label className="input-label">目标阶段</label><input className="input-field" value={ts} onChange={e=>setTs(e.target.value)}/></div>
        <div><label className="input-label">基准材料类型</label><select className="select-field" value={matType} onChange={e=>setMatType(e.target.value)}>{MAT_TYPES.map(m=><option key={m}>{m}</option>)}</select></div>
      </div>
      <button className="btn-primary btn-green" style={{marginTop:12}} onClick={calc}>▶  计算所需材料</button>
      <div style={{marginTop:10}}><ResultBox content={result}/></div>
    </div>
  );
}

export default function ToolCPage() {
  return <CalcPage title="⚔️ 装备重铸计算器" subtitle={`支持 ${EQUIPMENT_COUNT} 件装备同时重铸 · 等级 0-30 · 阶段 0-5`} tab1Label="📊 根据材料计算等级" tab2Label="🎯 根据目标计算材料" tab1Content={<Tab1/>} tab2Content={<Tab2/>} infoTitle="材料转换关系" infoItems={["· 青璃焰光 = 不灭离炎 × 3","· 冥雷寒铁 = 不灭离炎 × 9","· 辉光玄铁 = 不灭离炎 × 27","· 坠影紫晶和绯云玄晶不可转换",``,`⚠ 所有消耗量已 × ${EQUIPMENT_COUNT}（${EQUIPMENT_COUNT} 件装备）`]} />;
}
