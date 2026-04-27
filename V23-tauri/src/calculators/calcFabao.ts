/**
 * 法宝升阶计算引擎 - 移植自 calc_fabao.py
 * 数据从 JSON 加载
 */

let _data: any = null;
let _loadPromise: Promise<void> | null = null;

async function ensureData() {
  if (_data) return;
  if (_loadPromise) { await _loadPromise; return; }
  _loadPromise = (async () => { const r = await fetch("/game_data/fabao_data.json"); _data = await r.json(); })();
  await _loadPromise;
}

export type Fabao = { name:string; grade:string; formation:string; chip:string; mat2:string };

export async function getFabaoList(): Promise<Fabao[]> {
  await ensureData();
  return _data.fabao_list.map((f:any) => ({name:f.name,grade:f.grade,formation:f.formation,chip:f.chip,mat2:f.mat2}));
}

export async function getCostTables(formation:string): Promise<{chipCost:number[];mat2Cost:number[]}> {
  await ensureData();
  const formTypes = _data.formation_types;
  if (formTypes[formation] === "SANCAI") {
    return { chipCost: _data.sancai_chip_cost, mat2Cost: _data.sancai_mat2_cost };
  }
  return { chipCost: _data.sixiang_cost, mat2Cost: new Array(100).fill(0) };
}

export function hasMat2(formation:string): boolean {
  return formation === "三才阵" || formation === "归藏阵";
}

export async function calcByMaterials(fabao:Fabao, curLevel:number, ownedChips:number, ownedMat2:number) {
  const {chipCost, mat2Cost} = await getCostTables(fabao.formation);
  const hasM2 = hasMat2(fabao.formation);
  let remChips = ownedChips, remMat2 = ownedMat2, reachLevel = curLevel;
  let stopReason = "";

  for (let lv = curLevel; lv < 100; lv++) {
    const cc = chipCost[lv], mc = mat2Cost[lv];
    if (remChips < cc) { stopReason = `碎片不足（需${cc}，剩余${remChips}）`; break; }
    if (hasM2 && mc > 0 && remMat2 < mc) { stopReason = `${fabao.mat2}不足（需${mc}，剩余${remMat2}）`; break; }
    remChips -= cc;
    if (hasM2 && mc > 0) remMat2 -= mc;
    reachLevel = lv + 1;
  }

  let nextInfo = null;
  if (reachLevel < 100) {
    const nc = chipCost[reachLevel], nm = mat2Cost[reachLevel];
    nextInfo = { nextChip:nc, chipGap:Math.max(0,nc-remChips), nextMat2:nm, mat2Gap:hasM2?Math.max(0,nm-remMat2):0 };
  }
  return { error:null, reachLevel, remainingChips:remChips, remainingMat2:remMat2, stopReason, hasMat2:hasM2, nextInfo };
}

export async function calcForTarget(fabao:Fabao, curLevel:number, tgtLevel:number) {
  if (tgtLevel <= curLevel) return {error:"目标阶数必须大于当前阶数"};
  const {chipCost, mat2Cost} = await getCostTables(fabao.formation);
  const hasM2 = hasMat2(fabao.formation);
  let totalChips = 0, totalMat2 = 0;
  const segments: {from:number;to:number;chips:number;mat2:number}[] = [];

  for (let lv = curLevel; lv < tgtLevel; lv++) {
    totalChips += chipCost[lv];
    totalMat2 += mat2Cost[lv];
  }

  let segStart = curLevel;
  while (segStart < tgtLevel) {
    const segEnd = Math.min(Math.ceil((segStart + 1) / 5) * 5, tgtLevel);
    let sc = 0, sm = 0;
    for (let lv = segStart; lv < segEnd; lv++) { sc += chipCost[lv]; sm += mat2Cost[lv]; }
    segments.push({from:segStart, to:segEnd-1, chips:sc, mat2:sm});
    segStart = segEnd;
  }

  return { error:null, totalChips, totalMat2, hasMat2:hasM2, segments };
}
