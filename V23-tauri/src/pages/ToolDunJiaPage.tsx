import { useState } from "react";
import CalcPage from "../components/CalcPage";
import ResultBox from "../components/ResultBox";
import { GRADES, GRADE_ORDER, calcReachableLevel, calcRequiredMaterials } from "../calculators/calcDunjia";

function Tab1() {
  const [grade,setGrade]=useState("黄阶"); const [level,setLevel]=useState("0");
  const [mats,setMats]=useState<Record<string,string>>({"黄阶":"0","玄阶":"0","地阶":"0","天阶":"0"});
  const [result,setResult]=useState("");

  const calc = () => {
    const materials: Record<string,number> = {};
    for (const g of GRADE_ORDER) materials[g] = parseInt(mats[g])||0;
    const r = calcReachableLevel(grade, parseInt(level)||0, materials);
    if (r.error) { setResult(`⚠️ ${r.error}`); return; }
    const lines = [`✅ 计算完成`,``,`${"=".repeat(45)}`,`起始状态: ${grade} Lv.${level}`,`可达状态: ${r.finalGrade} Lv.${r.finalLevel}`,`${"=".repeat(45)}`,``,`【材料使用汇总】`];
    for (const g of GRADE_ORDER) { if (r.usedMaterials![g]>0) lines.push(`  ${GRADES[g].material}: 使用 ${r.usedMaterials![g]}/${materials[g]} 个`); }
    setResult(lines.join("\n"));
  };

  return (
    <div className="card">
      <h3 className="section-title">初始遁甲状态</h3>
      <div className="grid-2">
        <div><label className="input-label">当前品阶</label><select className="select-field" value={grade} onChange={e=>setGrade(e.target.value)}>{GRADE_ORDER.map(g=><option key={g}>{g}</option>)}</select></div>
        <div><label className="input-label">当前等级</label><input className="input-field" value={level} onChange={e=>setLevel(e.target.value)}/></div>
      </div>
      <h3 className="section-title" style={{marginTop:10}}>持有材料</h3>
      {GRADE_ORDER.map(g=>(<div key={g} style={{marginBottom:6}}><label className="input-label">{GRADES[g].material}</label><input className="input-field" value={mats[g]} onChange={e=>setMats({...mats,[g]:e.target.value})}/></div>))}
      <button className="btn-primary" style={{marginTop:12}} onClick={calc}>▶  计算可达遁甲等级</button>
      <div style={{marginTop:10}}><ResultBox content={result}/></div>
    </div>
  );
}

function Tab2() {
  const [sg,setSg]=useState("黄阶"); const [sl,setSl]=useState("0");
  const [eg,setEg]=useState("天阶"); const [el,setEl]=useState("100");
  const [result,setResult]=useState("");

  const calc = () => {
    const r = calcRequiredMaterials(sg,parseInt(sl)||0,eg,parseInt(el)||100);
    if (r.error) { setResult(`⚠️ ${r.error}`); return; }
    const lines = [`✅ 计算完成`,``,`${"=".repeat(45)}`,`起始: ${sg} Lv.${sl} → 目标: ${eg} Lv.${el}`,`${"=".repeat(45)}`,``,`【材料需求汇总】`];
    let total = 0;
    for (const g of GRADE_ORDER) { const n = r.required![g]; if (n>0) { lines.push(`  ${GRADES[g].material}: ${n} 个`); total += n; } }
    lines.push(``,`  总计: ${total} 个材料`);
    setResult(lines.join("\n"));
  };

  return (
    <div className="card">
      <h3 className="section-title">目标遁甲状态</h3>
      <div className="grid-2">
        <div><label className="input-label">当前品阶</label><select className="select-field" value={sg} onChange={e=>setSg(e.target.value)}>{GRADE_ORDER.map(g=><option key={g}>{g}</option>)}</select></div>
        <div><label className="input-label">当前等级</label><input className="input-field" value={sl} onChange={e=>setSl(e.target.value)}/></div>
        <div><label className="input-label">目标品阶</label><select className="select-field" value={eg} onChange={e=>setEg(e.target.value)}>{GRADE_ORDER.map(g=><option key={g}>{g}</option>)}</select></div>
        <div><label className="input-label">目标等级</label><input className="input-field" value={el} onChange={e=>setEl(e.target.value)}/></div>
      </div>
      <button className="btn-primary btn-green" style={{marginTop:12}} onClick={calc}>▶  计算所需材料</button>
      <div style={{marginTop:10}}><ResultBox content={result}/></div>
    </div>
  );
}

export default function ToolDunJiaPage() {
  return <CalcPage title="🔮 遁甲（强运）养成计算器" subtitle="4个品阶体系 · 黄阶→玄阶→地阶→天阶 · 共398个材料满级" tab1Label="📊 根据材料计算等级" tab2Label="🎯 根据目标计算材料" tab1Content={<Tab1/>} tab2Content={<Tab2/>} infoTitle="使用说明" infoItems={["• 4个品阶体系：黄阶(36级) → 玄阶(49级) → 地阶(64级) → 天阶(100级)","• 4种材料独立，不可互换","• 天阶后期递增：81级后每级消耗逐步增加到18个"]} />;
}
