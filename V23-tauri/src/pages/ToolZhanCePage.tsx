import { useState, useEffect } from "react";
import CalcPage from "../components/CalcPage";
import ResultBox from "../components/ResultBox";
import { SERIES_CONFIG, SERIES_ORDER, TIER_MAX_LEVELS, ALL_TIERS, ensureData, calcByMaterials, calcByTarget } from "../calculators/calcZhance";

function Tab1() {
  const [tier,setTier]=useState("1"); const [level,setLevel]=useState("0");
  const [mats,setMats]=useState<Record<string,string>>({}); const [copper,setCopper]=useState("99999999");
  const [result,setResult]=useState(""); const [ready,setReady]=useState(false);
  useEffect(()=>{ ensureData().then(()=>setReady(true)) },[]);

  const calc = () => {
    if (!ready) { setResult("数据加载中…"); return; }
    const materials: Record<string,number> = {};
    for (const s of SERIES_ORDER) { materials[`${s}_mat1`]=parseInt(mats[`${s}_mat1`]||"")||0; materials[`${s}_mat2`]=parseInt(mats[`${s}_mat2`]||"")||0; }
    const r = calcByMaterials(parseInt(tier)||1, parseInt(level)||0, materials, parseInt(copper)||99999999);
    if (r.error) { setResult(`⚠️ ${r.error}`); return; }
    const lines = [`✅ 计算完成`,``,`起始: ${tier}阶${level}重`,`可达: ${r.finalTier}阶${r.finalLevel}重`,``,"【材料使用汇总】"];
    for (const s of SERIES_ORDER) {
      const cfg = SERIES_CONFIG[s]; const m1 = r.used?.[`${s}_mat1`]||0; const m2 = r.used?.[`${s}_mat2`]||0;
      if (m1>0) lines.push(`  ${cfg.mat1Name}: ${m1.toLocaleString()}`);
      if (m2>0) lines.push(`  ${cfg.mat2Name}: ${m2}`);
    }
    lines.push(`  铜钱: ${r.usedCopper?.toLocaleString()}`);
    if (r.stoppedReason) lines.push(``,`⏹ ${r.stoppedReason}`);
    setResult(lines.join("\n"));
  };

  const tierMax = TIER_MAX_LEVELS[parseInt(tier)||1]||4;
  return (
    <div className="card">
      <h3 className="section-title">当前占测状态</h3>
      <div className="grid-2">
        <div><label className="input-label">当前阶数</label><select className="select-field" value={tier} onChange={e=>setTier(e.target.value)}>{ALL_TIERS.map(t=><option key={t} value={t}>{t}</option>)}</select></div>
        <div><label className="input-label">当前重数</label><select className="select-field" value={level} onChange={e=>setLevel(e.target.value)}><option value="0">0</option>{Array.from({length:tierMax},(_,i)=><option key={i+1} value={i+1}>{i+1}</option>)}</select></div>
      </div>
      <h3 className="section-title" style={{marginTop:10}}>持有材料</h3>
      {SERIES_ORDER.map(s=>{const cfg=SERIES_CONFIG[s];return(
        <div key={s} className="grid-2" style={{marginBottom:6}}>
          <div><label className="input-label">{cfg.mat1Name}</label><input className="input-field" value={mats[`${s}_mat1`]||""} placeholder="0" onChange={e=>setMats({...mats,[`${s}_mat1`]:e.target.value})}/></div>
          <div><label className="input-label">{cfg.mat2Name}</label><input className="input-field" value={mats[`${s}_mat2`]||""} placeholder="0" onChange={e=>setMats({...mats,[`${s}_mat2`]:e.target.value})}/></div>
        </div>
      )})}
      <div><label className="input-label">铜钱</label><input className="input-field" value={copper} onChange={e=>setCopper(e.target.value)}/></div>
      <button className="btn-primary" style={{marginTop:12}} onClick={calc}>▶ 计算可达阶数</button>
      <div style={{marginTop:10}}><ResultBox content={result}/></div>
    </div>
  );
}

function Tab2() {
  const [st,setSt]=useState("1"); const [sl,setSl]=useState("0"); const [tt,setTt]=useState("17"); const [tl,setTl]=useState("4");
  const [result,setResult]=useState(""); const [ready,setReady]=useState(false);
  useEffect(()=>{ ensureData().then(()=>setReady(true)) },[]);

  const calc = () => {
    if (!ready) { setResult("数据加载中…"); return; }
    const r = calcByTarget(parseInt(st)||1, parseInt(sl)||0, parseInt(tt)||17, parseInt(tl)||4);
    if (r.error) { setResult(`⚠️ ${r.error}`); return; }
    const lines = [`✅ 计算完成`,``,`${st}阶${sl}重 → ${tt}阶${tl}重`,``,"【材料需求汇总】"];
    let total = 0;
    for (const s of SERIES_ORDER) { const cfg=SERIES_CONFIG[s]; const m1=r.required?.[`${s}_mat1`]||0; const m2=r.required?.[`${s}_mat2`]||0;
      if (m1>0) { lines.push(`  ${cfg.mat1Name}: ${m1.toLocaleString()}`); total+=m1; }
      if (m2>0) { lines.push(`  ${cfg.mat2Name}: ${m2}`); total+=m2; }
    }
    lines.push(`  铜钱: ${r.requiredCopper?.toLocaleString()}`);
    lines.push(``,`  材料总计: ${total.toLocaleString()}`);
    setResult(lines.join("\n"));
  };

  return (
    <div className="card">
      <h3 className="section-title">目标占测状态</h3>
      <div className="grid-2">
        <div><label className="input-label">起始阶数</label><select className="select-field" value={st} onChange={e=>setSt(e.target.value)}>{ALL_TIERS.map(t=><option key={t} value={t}>{t}</option>)}</select></div>
        <div><label className="input-label">起始重数</label><input className="input-field" value={sl} onChange={e=>setSl(e.target.value)}/></div>
        <div><label className="input-label">目标阶数</label><select className="select-field" value={tt} onChange={e=>setTt(e.target.value)}>{ALL_TIERS.map(t=><option key={t} value={t}>{t}</option>)}</select></div>
        <div><label className="input-label">目标重数</label><input className="input-field" value={tl} onChange={e=>setTl(e.target.value)}/></div>
      </div>
      <button className="btn-primary btn-green" style={{marginTop:12}} onClick={calc}>▶ 计算所需材料</button>
      <div style={{marginTop:10}}><ResultBox content={result}/></div>
    </div>
  );
}

export default function ToolZhanCePage() {
  return <CalcPage title="📜 占测养成计算器" subtitle="3种品质 · 普通→玄→地 · 17阶4重满级" tab1Label="📊 材料→可达等级" tab2Label="🎯 目标→所需材料" tab1Content={<Tab1/>} tab2Content={<Tab2/>} infoTitle="使用说明" infoItems={["• 普通(1-8阶): 火灼兽骨 + 无极灵石","• 玄(9-12阶): 火灼兽骨·玄 + 无极灵石·玄","• 地(13-17阶): 火灼兽骨·地 + 无极灵石·地"]} />;
}
