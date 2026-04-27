import { useState, useEffect } from "react";
import CalcPage from "../components/CalcPage";
import ResultBox from "../components/ResultBox";
import { Fabao, getFabaoList, hasMat2, calcByMaterials, calcForTarget } from "../calculators/calcFabao";

const FORMATIONS = ["四象阵","八卦两仪阵","三才阵","归藏阵"];

function Tab1() {
  const [allFabao,setAllFabao]=useState<Fabao[]>([]); const [formation,setFormation]=useState("四象阵");
  const [fabao,setFabao]=useState<Fabao|null>(null); const [curLv,setCurLv]=useState("0"); const [chips,setChips]=useState("0"); const [mat2,setMat2]=useState("0");
  const [result,setResult]=useState("");

  useEffect(()=>{ getFabaoList().then(setAllFabao) },[]);
  const filtered = allFabao.filter(f=>f.formation===formation);
  useEffect(()=>{ if(filtered.length>0 && !fabao) setFabao(filtered[0]) },[filtered]);

  const calc = async () => {
    if (!fabao) return;
    const r = await calcByMaterials(fabao, parseInt(curLv)||0, parseInt(chips)||0, parseInt(mat2)||0);
    if (r.error) { setResult(`⚠️ ${r.error}`); return; }
    const lines = [`✅ 计算完成`,``,`法宝: ${fabao.name}（${formation}）`,`起始: ${curLv}阶 → 可达: ${r.reachLevel}阶`,`共提升: ${r.reachLevel!-(parseInt(curLv)||0)} 阶`,``,`剩余碎片: ${r.remainingChips?.toLocaleString()}`];
    if (r.hasMat2) lines.push(`剩余${fabao.mat2}: ${r.remainingMat2?.toLocaleString()}`);
    if (r.stopReason) lines.push(``,`停止原因: ${r.stopReason}`);
    if (r.reachLevel!>=100) lines.push(``,`🎉 已满阶!`);
    setResult(lines.join("\n"));
  };

  return (
    <div className="card">
      <h3 className="section-title">选择法宝</h3>
      <div className="grid-2">
        <div><label className="input-label">法阵类型</label><select className="select-field" value={formation} onChange={e=>{setFormation(e.target.value);setFabao(null)}}>{FORMATIONS.map(f=><option key={f}>{f}</option>)}</select></div>
        <div><label className="input-label">法宝名称</label><select className="select-field" value={fabao?.name||""} onChange={e=>setFabao(filtered.find(f=>f.name===e.target.value)||null)}>{filtered.map(f=><option key={f.name}>{f.name}</option>)}</select></div>
      </div>
      <div className="grid-2" style={{marginTop:8}}>
        <div><label className="input-label">当前阶数(0~99)</label><input className="input-field" value={curLv} onChange={e=>setCurLv(e.target.value)}/></div>
        <div><label className="input-label">持有碎片</label><input className="input-field" value={chips} onChange={e=>setChips(e.target.value)}/></div>
        {hasMat2(formation) && <div><label className="input-label">持有{fabao?.mat2||"第二材料"}</label><input className="input-field" value={mat2} onChange={e=>setMat2(e.target.value)}/></div>}
      </div>
      <button className="btn-primary" style={{marginTop:12}} onClick={calc}>▶ 计算可达阶数</button>
      <div style={{marginTop:10}}><ResultBox content={result}/></div>
    </div>
  );
}

function Tab2() {
  const [allFabao,setAllFabao]=useState<Fabao[]>([]); const [formation,setFormation]=useState("四象阵");
  const [fabao,setFabao]=useState<Fabao|null>(null); const [curLv,setCurLv]=useState("0"); const [tgtLv,setTgtLv]=useState("100");
  const [result,setResult]=useState("");

  useEffect(()=>{ getFabaoList().then(setAllFabao) },[]);
  const filtered = allFabao.filter(f=>f.formation===formation);
  useEffect(()=>{ if(filtered.length>0 && !fabao) setFabao(filtered[0]) },[filtered]);

  const calc = async () => {
    if (!fabao) return;
    const r = await calcForTarget(fabao, parseInt(curLv)||0, parseInt(tgtLv)||100);
    if (r.error) { setResult(`⚠️ ${r.error}`); return; }
    const lines = [`✅ 计算完成`,``,`法宝: ${fabao.name}（${formation}）`,`${curLv}阶 → ${tgtLv}阶`,``,`🏆 所需材料总计:`,`  ${fabao.chip}: ${r.totalChips?.toLocaleString()} 个`];
    if (r.hasMat2) lines.push(`  ${fabao.mat2}: ${r.totalMat2?.toLocaleString()} 个`);
    if (r.segments && r.segments.length>0) {
      lines.push(``,`【分段消耗】`);
      for (const s of r.segments) { let l = `  ${s.from}~${s.to}阶: 碎片 ${s.chips}`; if (r.hasMat2 && s.mat2>0) l += ` + ${fabao.mat2} ${s.mat2}`; lines.push(l); }
    }
    setResult(lines.join("\n"));
  };

  return (
    <div className="card">
      <h3 className="section-title">选择法宝</h3>
      <div className="grid-2">
        <div><label className="input-label">法阵类型</label><select className="select-field" value={formation} onChange={e=>{setFormation(e.target.value);setFabao(null)}}>{FORMATIONS.map(f=><option key={f}>{f}</option>)}</select></div>
        <div><label className="input-label">法宝名称</label><select className="select-field" value={fabao?.name||""} onChange={e=>setFabao(filtered.find(f=>f.name===e.target.value)||null)}>{filtered.map(f=><option key={f.name}>{f.name}</option>)}</select></div>
      </div>
      <div className="grid-2" style={{marginTop:8}}>
        <div><label className="input-label">当前阶数</label><input className="input-field" value={curLv} onChange={e=>setCurLv(e.target.value)}/></div>
        <div><label className="input-label">目标阶数</label><input className="input-field" value={tgtLv} onChange={e=>setTgtLv(e.target.value)}/></div>
      </div>
      <button className="btn-primary btn-green" style={{marginTop:12}} onClick={calc}>▶ 计算所需材料</button>
      <div style={{marginTop:10}}><ResultBox content={result}/></div>
    </div>
  );
}

export default function ToolFaBaoPage() {
  return <CalcPage title="🏺 法宝升阶计算器" subtitle="四象阵 · 八卦两仪阵 · 三才阵 · 归藏阵 · 0~100阶" tab1Label="📦 材料→可达阶数" tab2Label="🎯 目标→所需材料" tab1Content={<Tab1/>} tab2Content={<Tab2/>} infoTitle="使用说明" infoItems={["• 升阶成功率 100%，无失败风险","• 四象阵/八卦两仪阵：满阶共需 1,780 碎片","• 三才阵/归藏阵：20阶起需要第二材料"]} />;
}
