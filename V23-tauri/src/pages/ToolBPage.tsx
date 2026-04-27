import { useState } from "react";
import CalcPage from "../components/CalcPage";
import ResultBox from "../components/ResultBox";
import {
  MATERIAL_NAMES, MATERIAL2_NAME, REFINING_DATA,
  calcMaxLevel, calcMaterialsForTarget,
  toLowestMaterial, fromLowestMaterial, formatNum,
} from "../calculators/calcRefining";

function Tab1() {
  const [startLevel, setStartLevel] = useState("0");
  const [mat1Type, setMat1Type] = useState(0);
  const [mat1Count, setMat1Count] = useState("");
  const [mat2Count, setMat2Count] = useState("");
  const [result, setResult] = useState("");

  const calculate = () => {
    const sl = parseInt(startLevel) || 0;
    const hasMat1 = mat1Count.trim() !== "";
    const hasMat2 = mat2Count.trim() !== "";
    if (!hasMat1 && !hasMat2) { setResult("⚠️ 请至少输入一种材料的数量！"); return; }

    const m1Lowest = hasMat1 ? toLowestMaterial(parseFloat(mat1Count), mat1Type) : Infinity;
    const m2 = hasMat2 ? parseFloat(mat2Count) : Infinity;

    const r = calcMaxLevel(sl, mat1Type, m1Lowest, m2);
    const lines: string[] = [];
    lines.push(`最高可提升到：${r.currentLevel} 级`);
    lines.push(`从 ${sl} 级 → ${r.currentLevel} 级，共提升 ${r.currentLevel - sl} 级`);
    lines.push("━".repeat(36));

    if (hasMat1) {
      const used = fromLowestMaterial(r.usedMat1Lowest, mat1Type);
      lines.push(`消耗材料1：${formatNum(used)} ${MATERIAL_NAMES[mat1Type]}`);
    } else { lines.push("消耗材料1：无限"); }

    if (hasMat2) {
      lines.push(`消耗材料2：${formatNum(r.usedMat2)} ${MATERIAL2_NAME}`);
    } else { lines.push("消耗材料2：无限"); }

    const remMat1 = hasMat1 ? m1Lowest - r.usedMat1Lowest : null;
    const remMat2 = hasMat2 ? m2 - r.usedMat2 : null;
    if (remMat1 !== null && remMat1 > 0.0001) {
      lines.push(`剩余材料1：${formatNum(fromLowestMaterial(remMat1, mat1Type))} ${MATERIAL_NAMES[mat1Type]}`);
    }
    if (remMat2 !== null && remMat2 > 0.0001) {
      lines.push(`剩余材料2：${formatNum(remMat2)} ${MATERIAL2_NAME}`);
    }

    if (r.details.length > 0 && r.details.length <= 10) {
      lines.push("", "详细消耗：");
      for (const d of r.details) {
        lines.push(`  ${d.level}级：${MATERIAL_NAMES[d.mat1Type]}×${formatNum(d.mat1Count)}，${MATERIAL2_NAME}×${formatNum(d.mat2Count)}`);
      }
    } else if (r.details.length > 10) {
      lines.push("", `共消耗 ${r.details.length} 个等级的升级材料`);
    }

    setResult(lines.join("\n"));
  };

  return (
    <div className="card">
      <h3 className="section-title">📊 功能一：根据材料量计算可达成淬炼等级</h3>
      <div className="grid-2">
        <div>
          <label className="input-label">初始淬炼等级</label>
          <input className="input-field" value={startLevel} onChange={(e) => setStartLevel(e.target.value)} />
        </div>
        <div>
          <label className="input-label">材料1类型</label>
          <select className="select-field" value={mat1Type} onChange={(e) => setMat1Type(Number(e.target.value))}>
            <option value={0}>曜金矿石（最低级）</option>
            <option value={1}>九转菩提</option>
            <option value={2}>摩诃水晶</option>
            <option value={3}>诸法舍利（最高级）</option>
          </select>
        </div>
        <div>
          <label className="input-label">材料1数量</label>
          <input className="input-field" placeholder="留空=无限" value={mat1Count} onChange={(e) => setMat1Count(e.target.value)} />
        </div>
        <div>
          <label className="input-label">材料2（蚀日之晶）数量</label>
          <input className="input-field" placeholder="留空=无限" value={mat2Count} onChange={(e) => setMat2Count(e.target.value)} />
        </div>
      </div>
      <button className="btn-primary" style={{ marginTop: 12 }} onClick={calculate}>▶  计算可达成等级</button>
      <div style={{ marginTop: 10 }}><ResultBox content={result} /></div>
    </div>
  );
}

function Tab2() {
  const [startLevel, setStartLevel] = useState("0");
  const [targetLevel, setTargetLevel] = useState("98");
  const [result, setResult] = useState("");

  const calculate = () => {
    const sl = parseInt(startLevel) || 0;
    const tl = parseInt(targetLevel) || 98;
    if (sl >= tl) { setResult("⚠️ 目标等级必须大于初始等级！"); return; }
    if (tl > 98) { setResult("⚠️ 目标等级不能超过98！"); return; }

    const r = calcMaterialsForTarget(sl, tl);
    const totalHighest = r.fromLowest(r.totalMat1Lowest, r.highestMat1Type);

    const lines: string[] = [];
    lines.push(`从 ${sl} 级 → ${tl} 级`);
    lines.push(`需要提升 ${tl - sl} 级`);
    lines.push("━".repeat(36));
    lines.push(`所需材料1：${formatNum(totalHighest)} ${MATERIAL_NAMES[r.highestMat1Type]}`);
    lines.push(`所需材料2：${formatNum(r.totalMat2)} ${MATERIAL2_NAME}`);

    if (Object.keys(r.mat1TypeUsage).length > 1) {
      lines.push("", "材料1各类型需求：");
      for (let t = 0; t < 4; t++) {
        if ((r.mat1TypeUsage[t] || 0) > 0.0001) {
          lines.push(`  ${MATERIAL_NAMES[t]}：${formatNum(r.mat1TypeUsage[t])}`);
        }
      }
    }

    if (r.highestMat1Type > 0) {
      lines.push("", "低级换算：");
      for (let t = r.highestMat1Type - 1; t >= 0; t--) {
        const lower = r.fromLowest(r.totalMat1Lowest, t);
        lines.push(`  或需 ${MATERIAL_NAMES[t]}：${formatNum(lower)}`);
      }
    }

    setResult(lines.join("\n"));
  };

  return (
    <div className="card">
      <h3 className="section-title">🎯 功能二：根据目标等级计算所需材料</h3>
      <div className="grid-2">
        <div>
          <label className="input-label">初始淬炼等级</label>
          <input className="input-field" value={startLevel} onChange={(e) => setStartLevel(e.target.value)} />
        </div>
        <div>
          <label className="input-label">目标淬炼等级</label>
          <input className="input-field" value={targetLevel} onChange={(e) => setTargetLevel(e.target.value)} />
        </div>
      </div>
      <button className="btn-primary btn-green" style={{ marginTop: 12 }} onClick={calculate}>▶  计算所需材料</button>
      <div style={{ marginTop: 10 }}><ResultBox content={result} /></div>
    </div>
  );
}

export default function ToolBPage() {
  return (
    <CalcPage
      title="⚒️ 装备淬炼计算器"
      subtitle="支持材料→等级、等级→材料 双向计算"
      tab1Label="📊 根据材料计算等级"
      tab2Label="🎯 根据目标计算材料"
      tab1Content={<Tab1 />}
      tab2Content={<Tab2 />}
      infoTitle="材料转换规则"
      infoItems={[
        "• 5个低级材料 = 1个高级材料",
        "• 1个高级材料 = 5个低级材料",
        "",
        "材料等级（由低到高）：",
        "曜金矿石 < 九转菩提 < 摩诃水晶 < 诸法舍利",
      ]}
    />
  );
}
