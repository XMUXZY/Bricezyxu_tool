import { useState } from "react";
import CalcPage from "../components/CalcPage";
import ResultBox from "../components/ResultBox";
import { getGroupNames, getGroup, calcSimple, calcPrecise } from "../calculators/calcGuardian";

function Tab1() {
  const [groupName,setGroupName]=useState("四值功曹");
  const [curAvg,setCurAvg]=useState("0"); const [tgtAvg,setTgtAvg]=useState("5");
  const [result,setResult]=useState("");

  const calc = () => {
    const r = calcSimple(groupName, parseFloat(curAvg)||0, parseFloat(tgtAvg)||5);
    if (r.error) { setResult(`⚠️ ${r.error}`); return; }
    const lines = [
      `━━━ ${r.groupName} 快速计算 ━━━`,``,
      `输入：${r.inputCurAvg}星 → ${r.inputTgtAvg}星`,
      `实际分布均值：${r.curActualAvg}星 → ${r.tgtActualAvg}星`,
    ];
    const curDev = Math.abs(r.inputCurAvg! - r.curActualAvg!);
    const tgtDev = Math.abs(r.inputTgtAvg! - r.tgtActualAvg!);
    if (curDev > 0.25 || tgtDev > 0.25) {
      lines.push(`⚠️ 实际分布与输入有偏差（高品质神出货极低所致）`);
    }
    lines.push(``,`🎯 期望消耗：${r.fu?.toLocaleString()} 张${r.ticket}`,``,`━ 最常见星级分布 ━`);
    for (const d of r.details!) {
      lines.push(`  ${d.name}(${d.quality}): ${d.curStar}★→${d.tgtStar}★  缺口${d.need}残念  [${d.expPerFu}残念/张]`);
    }
    lines.push(``,`💡 含精华流转，精华优先补贴高品质守护神`);
    setResult(lines.join("\n"));
  };

  return (
    <div className="card">
      <h3 className="section-title">快速计算（平均星级）</h3>
      <div><label className="input-label">神仙谱组</label>
        <select className="select-field" value={groupName} onChange={e=>setGroupName(e.target.value)}>
          {getGroupNames().map(g=><option key={g}>{g}</option>)}
        </select>
      </div>
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
  const [groupName,setGroupName]=useState("四值功曹");
  const group = getGroup(groupName);
  const [curStars,setCurStars]=useState<number[]>(group?.gods.map(()=>0)||[]);
  const [tgtStars,setTgtStars]=useState<number[]>(group?.gods.map(()=>5)||[]);
  const [result,setResult]=useState("");

  const changeGroup = (name:string) => {
    setGroupName(name);
    const g = getGroup(name);
    if (g) { setCurStars(g.gods.map(()=>0)); setTgtStars(g.gods.map(()=>5)); }
  };

  const calc = () => {
    const r = calcPrecise(groupName, curStars, tgtStars);
    if (r.error) { setResult(`⚠️ ${r.error}`); return; }
    const lines = [`━━━ ${r.groupName} 精细计算 ━━━`,``];
    for (const d of r.details!) {
      if (d.need === 0) lines.push(`  ${d.name}(${d.quality}): 已达目标`);
      else lines.push(`  ${d.name}(${d.quality}): ${d.curStar}★→${d.tgtStar}★  缺口${d.need}残念  [${d.expPerFu}残念/张, 精华单价${d.jinghua}]`);
    }
    lines.push(``,`🎯 期望消耗：${r.fu?.toLocaleString()} 张${r.ticket}`,``,`💡 含精华流转（满5星后残念→精华→补贴高品质神）`);
    setResult(lines.join("\n"));
  };

  const stars = [0,1,2,3,4,5];
  return (
    <div className="card">
      <h3 className="section-title">精细计算（逐神星级）</h3>
      <div><label className="input-label">神仙谱组</label>
        <select className="select-field" value={groupName} onChange={e=>changeGroup(e.target.value)}>
          {getGroupNames().map(g=><option key={g}>{g}</option>)}
        </select>
      </div>
      {group && (
        <div style={{marginTop:10}}>
          <div style={{display:"grid",gridTemplateColumns:"1fr 60px 60px 60px",gap:4,fontSize:11,color:"#888",marginBottom:4}}>
            <span>守护神</span><span>品质</span><span>当前</span><span>目标</span>
          </div>
          {group.gods.map((g,i)=>(
            <div key={g.name} style={{display:"grid",gridTemplateColumns:"1fr 60px 60px 60px",gap:4,alignItems:"center",marginBottom:4}}>
              <span style={{fontSize:12,color:"#e0e0e0"}}>{g.name}</span>
              <span style={{fontSize:11,color:"#888"}}>{g.quality}</span>
              <select className="select-field" style={{height:26,fontSize:11}} value={curStars[i]} onChange={e=>{const c=[...curStars];c[i]=parseInt(e.target.value);setCurStars(c)}}>
                {stars.map(s=><option key={s} value={s}>{s}★</option>)}
              </select>
              <select className="select-field" style={{height:26,fontSize:11}} value={tgtStars[i]} onChange={e=>{const c=[...tgtStars];c[i]=parseInt(e.target.value);setTgtStars(c)}}>
                {stars.map(s=><option key={s} value={s}>{s}★</option>)}
              </select>
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
  return <CalcPage
    title="🛡️ 守护神养成计算器"
    subtitle="6个神仙谱组 · 含精华流转 · 逐张步进期望算法"
    tab1Label="📊 快速计算"
    tab2Label="🎯 精细计算"
    tab1Content={<Tab1/>}
    tab2Content={<Tab2/>}
    infoTitle="养成说明"
    infoItems={[
      "· 6个神仙谱组，各组独立，通过请神符获取守护神残念",
      "· 升星消耗残念：0→1(20) / 1→2(40) / 2→3(80) / 3→4(160) / 4→5(自动)",
      "· 精华流转：满5星后多余残念→精华→补贴组内高品质神",
      "· 快速模式：输入平均星级，自动生成最常见分布",
      "· 精细模式：逐个设置每个守护神的当前/目标星级",
      "· 全满5星参考：四值385张 / 日直609张 / 九歌880张 / 云海1,084张 / 五德1,352张 / 天元1,012张",
    ]}
  />;
}
