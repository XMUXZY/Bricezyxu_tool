import { useState } from "react";
import CalcPage from "../components/CalcPage";
import ResultBox from "../components/ResultBox";
import { XINLU_CONFIG, XINLU_NAMES, calcByMaterials, calcForTarget } from "../calculators/calcXinlu";

function fmt(v:number):string { return v===Infinity?"∞":v>=10000?v.toLocaleString("en-US",{maximumFractionDigits:0}):v.toLocaleString("en-US",{maximumFractionDigits:1}); }

function Tab1() {
  const [xinlu,setXinlu]=useState("太微"); const [curC,setCurC]=useState("1"); const [curS,setCurS]=useState("0");
  const [low,setLow]=useState(""); const [mid,setMid]=useState(""); const [high,setHigh]=useState(""); const [guard,setGuard]=useState("");
  const [mult,setMult]=useState("1"); const [result,setResult]=useState("");

  const calc = () => {
    const cfg = XINLU_CONFIG[xinlu]; const m = mult==="8"?8:1;
    const cc=parseInt(curC)||1, cs=parseInt(curS)||0;
    let lm=low.trim()?parseFloat(low):Infinity, mm=mid.trim()?parseFloat(mid):Infinity, hm=high.trim()?parseFloat(high):Infinity, gm=guard.trim()?parseFloat(guard):Infinity;
    if (m>1) { if(lm!==Infinity)lm/=m; if(mm!==Infinity)mm/=m; if(hm!==Infinity)hm/=m; if(gm!==Infinity)gm/=m; }
    const r = calcByMaterials(xinlu,cc,cs,lm,mm,hm,gm);
    const lines = [`━━━ 星录养成模拟结果 ━━━`,``,`星录：${xinlu} | 最高${cfg.maxChong}重`,`计算方式：${m>1?"8个星官(材料平分)":"单个星官"}`,``,`▸ 可达等级：${r.chong}重${r.star}星`,`  从 ${cc}重${cs}星 出发`,``];
    lines.push("━ 单官期望消耗 ━");
    if (r.used.low>0) lines.push(`  ${cfg.lowMat}(低阶): ${fmt(r.used.low)}`);
    if (r.used.mid>0) lines.push(`  ${cfg.midMat}(中阶): ${fmt(r.used.mid)}`);
    if (r.used.high>0) lines.push(`  ${cfg.highMat}(高阶): ${fmt(r.used.high)}`);
    if (r.used.guard>0) lines.push(`  ${cfg.guard}(保级): ${fmt(r.used.guard)}`);
    if (m>1) {
      lines.push(``,`━ 8官总消耗 ━`);
      if (r.used.low>0) lines.push(`  ${cfg.lowMat}: ${fmt(r.used.low*8)}`);
      if (r.used.mid>0) lines.push(`  ${cfg.midMat}: ${fmt(r.used.mid*8)}`);
      if (r.used.high>0) lines.push(`  ${cfg.highMat}: ${fmt(r.used.high*8)}`);
      if (r.used.guard>0) lines.push(`  ${cfg.guard}: ${fmt(r.used.guard*8)}`);
    }
    lines.push(``,`💡 以上为期望值，建议备20-30%冗余`);
    setResult(lines.join("\n"));
  };

  const cfg = XINLU_CONFIG[xinlu];
  return (
    <div className="card">
      <h3 className="section-title">选择星录</h3>
      <select className="select-field" value={xinlu} onChange={e=>setXinlu(e.target.value)}>{XINLU_NAMES.map(n=><option key={n}>{n}</option>)}</select>
      <p style={{color:"#e94560",fontSize:11,margin:"6px 0"}}>最高{cfg.maxChong}重 | 解锁等级:{cfg.unlockLv} | 前置:{cfg.preReq}</p>
      <h3 className="section-title" style={{marginTop:10}}>当前状态</h3>
      <div className="grid-2">
        <div><label className="input-label">当前重数</label><input className="input-field" value={curC} onChange={e=>setCurC(e.target.value)}/></div>
        <div><label className="input-label">当前星级(0=未开始)</label><input className="input-field" value={curS} onChange={e=>setCurS(e.target.value)}/></div>
      </div>
      <h3 className="section-title" style={{marginTop:10}}>拥有材料（留空=无限）</h3>
      <div className="grid-2">
        <div><label className="input-label">{cfg.lowMat}(低阶)</label><input className="input-field" placeholder="留空=无限" value={low} onChange={e=>setLow(e.target.value)}/></div>
        <div><label className="input-label">{cfg.midMat}(中阶)</label><input className="input-field" placeholder="留空=无限" value={mid} onChange={e=>setMid(e.target.value)}/></div>
        <div><label className="input-label">{cfg.highMat}(高阶)</label><input className="input-field" placeholder="留空=无限" value={high} onChange={e=>setHigh(e.target.value)}/></div>
        <div><label className="input-label">{cfg.guard}(保级)</label><input className="input-field" placeholder="留空=无限" value={guard} onChange={e=>setGuard(e.target.value)}/></div>
      </div>
      <div style={{marginTop:8}}><label className="input-label">计算星官数量</label><select className="select-field" value={mult} onChange={e=>setMult(e.target.value)}><option value="1">1个星官</option><option value="8">8个星官(全部)</option></select></div>
      <button className="btn-primary btn-accent" style={{marginTop:12}} onClick={calc}>▶ 计算可达到的等级</button>
      <div style={{marginTop:10}}><ResultBox content={result}/></div>
    </div>
  );
}

function Tab2() {
  const [xinlu,setXinlu]=useState("太微"); const [sc,setSc]=useState("1"); const [ss,setSs]=useState("0");
  const [tc,setTc]=useState("20"); const [ts,setTs]=useState("6"); const [mult,setMult]=useState("1"); const [result,setResult]=useState("");

  const calc = () => {
    const cfg = XINLU_CONFIG[xinlu]; const m = mult==="8"?8:1;
    const r = calcForTarget(xinlu,parseInt(sc)||1,parseInt(ss)||0,parseInt(tc)||20,parseInt(ts)||6);
    if (r.error) { setResult(`⚠️ ${r.error}`); return; }
    const u = r.used!;
    const lines = [`━━━ 星录材料需求汇总 ━━━`,``,`星录：${xinlu} | 最高${cfg.maxChong}重`,`范围：${sc}重${ss}星 → ${tc}重${ts}星`,`计算方式：${m>1?"8个星官":"单个星官"}`,``];
    lines.push("━ 单官期望消耗 ━");
    if (u.low>0) lines.push(`  ${cfg.lowMat}(低阶): ${fmt(u.low)}`);
    if (u.mid>0) lines.push(`  ${cfg.midMat}(中阶): ${fmt(u.mid)}`);
    if (u.high>0) lines.push(`  ${cfg.highMat}(高阶): ${fmt(u.high)}`);
    if (u.guard>0) lines.push(`  ${cfg.guard}(保级): ${fmt(u.guard)}`);
    if (m>1) { lines.push(``,`━ 8官总消耗 ━`);
      if (u.low>0) lines.push(`  ${cfg.lowMat}: ${fmt(u.low*8)}`);
      if (u.mid>0) lines.push(`  ${cfg.midMat}: ${fmt(u.mid*8)}`);
      if (u.high>0) lines.push(`  ${cfg.highMat}: ${fmt(u.high*8)}`);
      if (u.guard>0) lines.push(`  ${cfg.guard}: ${fmt(u.guard*8)}`);
    }
    setResult(lines.join("\n"));
  };

  return (
    <div className="card">
      <h3 className="section-title">选择星录</h3>
      <select className="select-field" value={xinlu} onChange={e=>setXinlu(e.target.value)}>{XINLU_NAMES.map(n=><option key={n}>{n}</option>)}</select>
      <div className="grid-2" style={{marginTop:10}}>
        <div><label className="input-label">起始重数</label><input className="input-field" value={sc} onChange={e=>setSc(e.target.value)}/></div>
        <div><label className="input-label">起始星级</label><input className="input-field" value={ss} onChange={e=>setSs(e.target.value)}/></div>
        <div><label className="input-label">目标重数</label><input className="input-field" value={tc} onChange={e=>setTc(e.target.value)}/></div>
        <div><label className="input-label">目标星级</label><input className="input-field" value={ts} onChange={e=>setTs(e.target.value)}/></div>
      </div>
      <div style={{marginTop:8}}><label className="input-label">计算星官数量</label><select className="select-field" value={mult} onChange={e=>setMult(e.target.value)}><option value="1">1个星官</option><option value="8">8个星官(全部)</option></select></div>
      <button className="btn-primary btn-accent" style={{marginTop:12}} onClick={calc}>▶ 计算所需材料</button>
      <div style={{marginTop:10}}><ResultBox content={result}/></div>
    </div>
  );
}

export default function ToolDPage() {
  return <CalcPage title="⭐ 星录养成计算器" subtitle="QQ华夏手游 · 4部星录 × 8星官 · 概率期望计算" tab1Label="📊 根据材料算可达等级" tab2Label="🎯 根据目标算所需材料" tab1Content={<Tab1/>} tab2Content={<Tab2/>} infoTitle="养成说明" infoItems={["· 4部星录：太微→紫微→天市→启明，按解锁顺序依次开放","· 每重有6个星级（1→6星），全部打通后可升重","· 锤炼为概率制：结果为期望消耗（含概率增量保底）","· 20重概率约28%（期望3.56次），20重1星无需保级","· 天市最高22重，21-22重概率仅5%，保级大幅上升","· 启明17-20重保级消耗急增（17:12, 18:21, 19:34, 20:49/次）","· 建议在期望值基础上备20-30%冗余"]} />;
}
