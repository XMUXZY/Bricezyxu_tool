/**
 * 白虎星图锤炼计算引擎 - 移植自 calc_baihu_star.py
 * 从 JSON 加载数据
 */

let _data: any = null;
let _loadPromise: Promise<void> | null = null;

async function ensureData() {
  if (_data) return;
  if (_loadPromise) { await _loadPromise; return; }
  _loadPromise = (async () => { const r = await fetch("/game_data/baihu_star_data.json"); _data = await r.json(); })();
  await _loadPromise;
}

export async function getOfficialNames(): Promise<string[]> {
  await ensureData();
  return _data.officials.map((o:any) => o.name);
}

function findOfficial(name:string) { return _data.officials.find((o:any) => o.name === name); }
function getLevelInfo(officialName:string, weight:number, level:number) {
  const off = findOfficial(officialName);
  if (!off) return null;
  return off.levels.find((lv:any) => lv.weight === weight && lv.level === level);
}

function stateToIndex(w:number,l:number):number { return w===0&&l===0 ? 0 : (w-1)*_data.max_level+l; }
function indexToState(idx:number):[number,number] {
  if (idx<=0) return [0,0];
  return [Math.floor((idx-1)/_data.max_level)+1, (idx-1)%_data.max_level+1];
}

export async function calcMaterialCost(officialName:string, curW:number, curL:number, tgtW:number, tgtL:number) {
  await ensureData();
  const off = findOfficial(officialName);
  if (!off) return {error:`未找到星官: ${officialName}`};

  const curIdx = stateToIndex(curW,curL), tgtIdx = stateToIndex(tgtW,tgtL);
  if (tgtIdx <= curIdx) return {error:"目标必须高于当前状态"};

  let totalHammer = 0, totalGuarantee = 0;
  const details: any[] = [];

  for (let idx = curIdx+1; idx <= tgtIdx; idx++) {
    const [w,l] = indexToState(idx);
    const info = getLevelInfo(officialName, w, l);
    if (!info) return {error:`找不到 ${officialName} ${w}重${l}级的数据`};

    const hTotal = info.hammer_cost * info.expected_tries;
    const gTotal = info.guarantee_cost * info.expected_tries;
    totalHammer += hTotal; totalGuarantee += gTotal;
    details.push({weight:w,level:l,hammerPer:info.hammer_cost,guaranteePer:info.guarantee_cost,baseRate:info.base_rate,tries:Math.round(info.expected_tries*100)/100,hammerTotal:Math.round(hTotal*10)/10,guaranteeTotal:Math.round(gTotal*10)/10});
  }

  return {error:null, officialName, hammerMaterial:off.hammer_material, guaranteeMaterial:_data.guarantee_material,
    curState:[curW,curL], tgtState:[tgtW,tgtL], totalHammer:Math.round(totalHammer*10)/10, totalGuarantee:Math.round(totalGuarantee*10)/10, details};
}

export async function calcMaxReachable(officialName:string, curW:number, curL:number, heldHammer:number, heldGuarantee:number) {
  await ensureData();
  const off = findOfficial(officialName);
  if (!off) return {error:`未找到星官: ${officialName}`};

  const curIdx = stateToIndex(curW,curL);
  const maxIdx = stateToIndex(_data.max_weight, _data.max_level);
  let remainH = heldHammer, remainG = heldGuarantee, usedH = 0, usedG = 0, reachedIdx = curIdx;
  const details: any[] = [];
  let limiting = "已满级";

  for (let idx = curIdx+1; idx <= maxIdx; idx++) {
    const [w,l] = indexToState(idx);
    const info = getLevelInfo(officialName, w, l);
    if (!info) break;

    const hNeed = info.hammer_cost * info.expected_tries;
    const gNeed = info.guarantee_cost * info.expected_tries;

    if (remainH < hNeed) { limiting = off.hammer_material; break; }
    if (remainG < gNeed) { limiting = _data.guarantee_material; break; }

    remainH -= hNeed; remainG -= gNeed; usedH += hNeed; usedG += gNeed; reachedIdx = idx;
    details.push({weight:w,level:l,hammerTotal:Math.round(hNeed*10)/10,guaranteeTotal:Math.round(gNeed*10)/10,tries:Math.round(info.expected_tries*100)/100});
  }

  const [rw,rl] = indexToState(reachedIdx);
  return {error:null, officialName, hammerMaterial:off.hammer_material, guaranteeMaterial:_data.guarantee_material,
    curState:[curW,curL], maxState:[rw,rl], usedHammer:Math.round(usedH*10)/10, usedGuarantee:Math.round(usedG*10)/10,
    remainingHammer:Math.round(remainH*10)/10, remainingGuarantee:Math.round(remainG*10)/10, levelsGained:reachedIdx-curIdx, details, limitingFactor:limiting};
}
