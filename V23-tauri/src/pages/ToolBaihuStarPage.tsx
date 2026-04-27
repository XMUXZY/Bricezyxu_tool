import { useState, useEffect } from "react";
import CalcPage from "../components/CalcPage";
import ResultBox from "../components/ResultBox";
import { getOfficialNames, calcMaterialCost, calcMaxReachable } from "../calculators/calcBaihuStar";

function Tab1() {
  const [officials,setOfficials]=useState<string[]>([]); const [off,setOff]=useState(""); const [curW,setCurW]=useState("0"); const [curL,setCurL]=useState("0"); const [tgtW,setTgtW]=useState("10"); const [tgtL,setTgtL]=useState("6"); const [result,setResult]=useState("");
  useEffect(()=>{ getOfficialNames().then(n=>{setOfficials(n);setOff(n[0]||"")}) },[]);

  const calc = async () => {
    const r = await calcMaterialCost(off, parseInt(curW)||0, parseInt(curL)||0, parseInt(tgtW)||10, parseInt(tgtL)||6);
    if (r.error) { setResult(`⚠️ ${r.error}`); return; }
    const cs = r.curState![0]>0?`${r.curState![0]}重${r.curState![1]}级`:"未开始";
    const lines = [`━━━ 白虎星图锤炼消耗 ━━━`,``,`星官：${r.officialName}`,`从 ${cs} → ${r.tgtState![0]}重${r.tgtState![1]}级`,``,`锤炼材料（${r.hammerMaterial}）`,`  期望消耗：${r.totalHammer?.toLocaleString()} 个`,`  向上取整：${Math.ceil(r.totalHammer!).toLocaleString()} 个`,``,`保底材料（${r.guaranteeMaterial}）`,`  期望消耗：${r.totalGuarantee?.toLocaleString()} 个`,`  向上取整：${Math.ceil(r.totalGuarantee!).toLocaleString()} 个`];
    setResult(lines.join("\n"));
  };

  return (
    <div className="card">
      <h3 className="section-title">选择星官</h3>
      <select className="select-field" value={off} onChange={e=>setOff(e.target.value)}>{officials.map(n=><option key={n}>{n}</option>)}</select>
      <div className="grid-2" style={{marginTop:10}}>
        <div><label className="input-label">当前重数(0=未开始)</label><input className="input-field" value={curW} onChange={e=>setCurW(e.target.value)}/></div>
        <div><label className="input-label">当前等级(0=未开始)</label><input className="input-field" value={curL} onChange={e=>setCurL(e.target.value)}/></div>
        <div><label className="input-label">目标重数(1~10)</label><input className="input-field" value={tgtW} onChange={e=>setTgtW(e.target.value)}/></div>
        <div><label className="input-label">目标等级(1~6)</label><input className="input-field" value={tgtL} onChange={e=>setTgtL(e.target.value)}/></div>
      </div>
      <button className="btn-primary" style={{marginTop:12}} onClick={calc}>▶ 计算材料消耗</button>
      <div style={{marginTop:10}}><ResultBox content={result}/></div>
    </div>
  );
}

function Tab2() {
  const [officials,setOfficials]=useState<string[]>([]); const [off,setOff]=useState(""); const [curW,setCurW]=useState("0"); const [curL,setCurL]=useState("0"); const [hh,setHh]=useState("10000"); const [hg,setHg]=useState("5000"); const [result,setResult]=useState("");
  useEffect(()=>{ getOfficialNames().then(n=>{setOfficials(n);setOff(n[0]||"")}) },[]);

  const calc = async () => {
    const r = await calcMaxReachable(off, parseInt(curW)||0, parseInt(curL)||0, parseFloat(hh)||0, parseFloat(hg)||0);
    if (r.error) { setResult(`⚠️ ${r.error}`); return; }
    const cs = r.curState![0]>0?`${r.curState![0]}重${r.curState![1]}级`:"未开始";
    const ms = r.maxState![0]>0?`${r.maxState![0]}重${r.maxState![1]}级`:"未开始";
    const lines = [`━━━ 白虎星图材料反推 ━━━`,``,`星官：${r.officialName}`,`当前：${cs}`,``,`🎯 可达：${ms}  (共提升 ${r.levelsGained} 级)`,``,`消耗 ${r.hammerMaterial}：${r.usedHammer?.toLocaleString()}`,`消耗 ${r.guaranteeMaterial}：${r.usedGuarantee?.toLocaleString()}`,``,`剩余 ${r.hammerMaterial}：${r.remainingHammer?.toLocaleString()}`,`剩余 ${r.guaranteeMaterial}：${r.remainingGuarantee?.toLocaleString()}`,``,`瓶颈：${r.limitingFactor}`];
    setResult(lines.join("\n"));
  };

  return (
    <div className="card">
      <h3 className="section-title">选择星官</h3>
      <select className="select-field" value={off} onChange={e=>setOff(e.target.value)}>{officials.map(n=><option key={n}>{n}</option>)}</select>
      <div className="grid-2" style={{marginTop:10}}>
        <div><label className="input-label">当前重数</label><input className="input-field" value={curW} onChange={e=>setCurW(e.target.value)}/></div>
        <div><label className="input-label">当前等级</label><input className="input-field" value={curL} onChange={e=>setCurL(e.target.value)}/></div>
        <div><label className="input-label">锤炼材料数量</label><input className="input-field" value={hh} onChange={e=>setHh(e.target.value)}/></div>
        <div><label className="input-label">保底材料(白虎之灵)</label><input className="input-field" value={hg} onChange={e=>setHg(e.target.value)}/></div>
      </div>
      <button className="btn-primary" style={{marginTop:12}} onClick={calc}>▶ 计算可达等级</button>
      <div style={{marginTop:10}}><ResultBox content={result}/></div>
    </div>
  );
}

export default function ToolBaihuStarPage() {
  return <CalcPage title="🐯 白虎星图锤炼计算器" subtitle="奎木狼 / 胃土雉 / 娄金星官 · 默认使用保底材料" tab1Label="🎯 根据目标计算消耗" tab2Label="📦 根据材料反推等级" tab1Content={<Tab1/>} tab2Content={<Tab2/>} infoTitle="锤炼说明" infoItems={["• 白虎星图3个星官，每个10重×6级","• 每次锤炼消耗锤炼材料 + 保底材料","• 计算结果为期望值（基于保底期望次数）"]} />;
}
