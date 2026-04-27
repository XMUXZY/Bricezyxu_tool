import { useState, useEffect } from "react";
import CalcPage from "../components/CalcPage";
import ResultBox from "../components/ResultBox";
import { getGroupNames, getGroupGuardians, getGroupTicket, calcSimple, calcPrecise } from "../calculators/calcGuardian";

function Tab1() {
  const [groups,setGroups]=useState<string[]>([]); const [group,setGroup]=useState(""); const [curAvg,setCurAvg]=useState("0"); const [tgtAvg,setTgtAvg]=useState("5"); const [result,setResult]=useState("");
  useEffect(()=>{ getGroupNames().then(g=>{setGroups(g);setGroup(g[0]||"")}) },[]);

  const calc = async () => {
    const r = await calcSimple(group, parseFloat(curAvg)||0, parseFloat(tgtAvg)||5);
    if (r.error) { setResult(`⚠️ ${r.error}`); return; }
    const lines = [`【${r.groupName}组 养成计算】`,``,`当前平均: ${curAvg}星 → 目标: ${tgtAvg}星`,`使用: ${r.ticket}`,``,`━━━ 最常见方案 ━━━`,``];
    for (const d of r.details||[]) {
      if (d.gap===0) lines.push(`  ${d.name}(${d.quality}): 已达目标`);
      else lines.push(`  ${d.name}(${d.quality}, ${d.expPerTicket}残念/张): 缺口${d.need}，需${d.tickets.toLocaleString()}张`);
    }
    lines.push(``,`合计${r.ticket}：约 ${r.totalTickets?.toLocaleString()} 张（期望值）`);
    setResult(lines.join("\n"));
  };

  return (
    <div className="card">
      <h3 className="section-title">简单模式（平均星级）</h3>
      <div><label className="input-label">神仙谱组</label><select className="select-field" value={group} onChange={e=>setGroup(e.target.value)}>{groups.map(g=><option key={g}>{g}</option>)}</select></div>
      <div className="grid-2" style={{marginTop:8}}>
        <div><label className="input-label">当前平均星级(0~5)</label><input className="input-field" value={curAvg} onChange={e=>setCurAvg(e.target.value)}/></div>
        <div><label className="input-label">目标平均星级(0~5)</label><input className="input-field" value={tgtAvg} onChange={e=>setTgtAvg(e.target.value)}/></div>
      </div>
      <button className="btn-primary" style={{marginTop:12}} onClick={calc}>▶ 计算请神符消耗</button>
      <div style={{marginTop:10}}><ResultBox content={result}/></div>
    </div>
  );
}

function Tab2() {
  const [groups,setGroups]=useState<string[]>([]); const [group,setGroup]=useState(""); const [guardians,setGuardians]=useState<any[]>([]);
  const [curStars,setCurStars]=useState<number[]>([]); const [tgtStars,setTgtStars]=useState<number[]>([]); const [result,setResult]=useState("");

  useEffect(()=>{ getGroupNames().then(g=>{setGroups(g);if(g[0])changeGroup(g[0])}) },[]);
  const changeGroup = async (gn:string) => {
    setGroup(gn);
    const gs = await getGroupGuardians(gn);
    setGuardians(gs); setCurStars(gs.map(()=>0)); setTgtStars(gs.map(()=>5));
  };

  const calc = async () => {
    const r = await calcPrecise(group, curStars, tgtStars);
    if (r.error) { setResult(`⚠️ ${r.error}`); return; }
    const lines = [`【精确计算：${r.groupName}组】`,``];
    for (const d of r.details||[]) {
      if (d.gap===0) lines.push(`  ${d.name}: 已达目标`);
      else lines.push(`  ${d.name}: 缺口${d.need}，期望${d.tickets.toLocaleString()}张（${d.expPerTicket}残念/张）`);
    }
    lines.push(``,`合计${r.ticket}：精确 ${r.totalTickets?.toLocaleString()} 张`);
    setResult(lines.join("\n"));
  };

  const stars = [0,1,2,3,4,5];
  return (
    <div className="card">
      <h3 className="section-title">精确模式</h3>
      <div><label className="input-label">神仙谱组</label><select className="select-field" value={group} onChange={e=>changeGroup(e.target.value)}>{groups.map(g=><option key={g}>{g}</option>)}</select></div>
      {guardians.length>0 && (
        <div style={{marginTop:10}}>
          <div style={{display:"grid",gridTemplateColumns:"1fr 60px 60px 60px 60px",gap:4,fontSize:11,color:"#888",marginBottom:4}}>
            <span>守护神</span><span>品质</span><span>当前</span><span>目标</span><span></span>
          </div>
          {guardians.map((g,i)=>(
            <div key={g.name} style={{display:"grid",gridTemplateColumns:"1fr 60px 60px 60px",gap:4,alignItems:"center",marginBottom:4}}>
              <span style={{fontSize:12,color:"#e0e0e0"}}>{g.name}</span>
              <span style={{fontSize:11,color:"#888"}}>{g.quality}</span>
              <select className="select-field" style={{height:26,fontSize:11}} value={curStars[i]} onChange={e=>{const c=[...curStars];c[i]=parseInt(e.target.value);setCurStars(c)}}>{stars.map(s=><option key={s} value={s}>{s}</option>)}</select>
              <select className="select-field" style={{height:26,fontSize:11}} value={tgtStars[i]} onChange={e=>{const c=[...tgtStars];c[i]=parseInt(e.target.value);setTgtStars(c)}}>{stars.map(s=><option key={s} value={s}>{s}</option>)}</select>
            </div>
          ))}
        </div>
      )}
      <button className="btn-primary" style={{marginTop:12}} onClick={calc}>▶ 精确计算</button>
      <div style={{marginTop:10}}><ResultBox content={result}/></div>
    </div>
  );
}

export default function ToolGuardianPage() {
  return <CalcPage title="🛡️ 守护神养成计算器" subtitle="基于真实出货概率 + 幸运值保底 + 次数保底" tab1Label="📊 简单模式" tab2Label="🎯 精确模式" tab1Content={<Tab1/>} tab2Content={<Tab2/>} infoTitle="养成说明" infoItems={["• 总消耗 = 最慢到位守护神的独立需求（并行模型）","• 升星消耗残念：0→1星(20) / 1→2星(40) / 2→3星(80) / 3→4星(160)","• 每次请神获得 10 个残念","• 紫/金品质出货概率极低，建议配合精华"]} />;
}
