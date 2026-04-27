/**
 * 占测养成计算引擎 - 移植自 calc_zhance.py
 * 3种品质：普通(1-8阶) → 玄(9-12阶) → 地(13-17阶)
 */

export const SERIES_CONFIG: Record<string,{mat1Name:string;mat2Name:string;tiers:number[]}> = {
  "普通":{mat1Name:"火灼兽骨",mat2Name:"无极灵石",tiers:[1,2,3,4,5,6,7,8]},
  "玄":{mat1Name:"火灼兽骨·玄",mat2Name:"无极灵石·玄",tiers:[9,10,11,12]},
  "地":{mat1Name:"火灼兽骨·地",mat2Name:"无极灵石·地",tiers:[13,14,15,16,17]},
};
export const SERIES_ORDER = ["普通","玄","地"];
export const TIER_MAX_LEVELS: Record<number,number> = {1:4,2:5,3:5,4:7,5:4,6:5,7:5,8:7,9:4,10:5,11:5,12:7,13:4,14:5,15:5,16:7,17:4};
export const ALL_TIERS = Array.from({length:17},(_,i)=>i+1);

const TIER_SERIES: Record<number,string> = {};
for (const [s,cfg] of Object.entries(SERIES_CONFIG)) { for (const t of cfg.tiers) TIER_SERIES[t] = s; }

let LEVEL_DATA: Record<string,{mat1:number;mat2:number;copper:number}> | null = null;
let dataLoadPromise: Promise<void> | null = null;

export async function ensureData() {
  if (LEVEL_DATA) return;
  if (dataLoadPromise) { await dataLoadPromise; return; }
  dataLoadPromise = (async () => {
    const resp = await fetch("/game_data/zhance_data.json");
    const json = await resp.json();
    LEVEL_DATA = {};
    for (const [k, v] of Object.entries(json.level_data as Record<string,any>)) {
      const [t, l] = k.split("_");
      LEVEL_DATA[`${t}_${l}`] = v as any;
    }
  })();
  await dataLoadPromise;
}

function getLevelInfo(tier:number, level:number) {
  return LEVEL_DATA?.[`${tier}_${level}`] ?? {mat1:0,mat2:0,copper:0};
}

export function calcByMaterials(startTier:number, startLevel:number, materials:Record<string,number>, copperAvailable:number) {
  if (!LEVEL_DATA) return {error:"数据未加载"};
  const used: Record<string,number> = {}; for (const s of SERIES_ORDER) { used[`${s}_mat1`]=0; used[`${s}_mat2`]=0; }
  let usedCopper = 0, currentTier = startTier, currentLevel = startLevel;
  const path: any[] = [];

  for (const tier of ALL_TIERS) {
    if (tier < startTier) continue;
    const series = TIER_SERIES[tier]; const tierMax = TIER_MAX_LEVELS[tier];
    const cfg = SERIES_CONFIG[series]; const fromLv = tier === startTier ? startLevel + 1 : 1;

    for (let lv = fromLv; lv <= tierMax; lv++) {
      const info = getLevelInfo(tier, lv);
      const m1Avail = (materials[`${series}_mat1`] ?? 0) - used[`${series}_mat1`];
      const m2Avail = (materials[`${series}_mat2`] ?? 0) - used[`${series}_mat2`];
      const cAvail = copperAvailable - usedCopper;

      if (m1Avail >= info.mat1 && m2Avail >= info.mat2 && cAvail >= info.copper) {
        used[`${series}_mat1`] += info.mat1; used[`${series}_mat2`] += info.mat2; usedCopper += info.copper;
        currentTier = tier; currentLevel = lv;
        path.push({tier,level:lv,mat1:info.mat1,mat2:info.mat2,copper:info.copper,mat1Name:cfg.mat1Name,mat2Name:cfg.mat2Name,series});
      } else {
        const reasons: string[] = [];
        if (m1Avail < info.mat1) reasons.push(`${cfg.mat1Name}不足`);
        if (m2Avail < info.mat2) reasons.push(`${cfg.mat2Name}不足`);
        if (cAvail < info.copper) reasons.push("铜钱不足");
        return {error:null,finalTier:currentTier,finalLevel:currentLevel,used,usedCopper,path,stoppedReason:`升${tier}阶${lv}重时: ${reasons.join("、")}`};
      }
    }
  }
  return {error:null,finalTier:currentTier,finalLevel:currentLevel,used,usedCopper,path,stoppedReason:"已达当前数据最高等级"};
}

export function calcByTarget(startTier:number, startLevel:number, targetTier:number, targetLevel:number) {
  if (!LEVEL_DATA) return {error:"数据未加载"};
  const required: Record<string,number> = {}; for (const s of SERIES_ORDER) { required[`${s}_mat1`]=0; required[`${s}_mat2`]=0; }
  let requiredCopper = 0; const path: any[] = [];

  for (const tier of ALL_TIERS) {
    if (tier < startTier || tier > targetTier) continue;
    const series = TIER_SERIES[tier]; const tierMax = TIER_MAX_LEVELS[tier]; const cfg = SERIES_CONFIG[series];
    const fromLv = tier === startTier ? startLevel + 1 : 1;
    const toLv = tier === targetTier ? targetLevel : tierMax;

    for (let lv = fromLv; lv <= toLv; lv++) {
      const info = getLevelInfo(tier, lv);
      required[`${series}_mat1`] += info.mat1; required[`${series}_mat2`] += info.mat2; requiredCopper += info.copper;
      path.push({tier,level:lv,mat1:info.mat1,mat2:info.mat2,copper:info.copper,mat1Name:cfg.mat1Name,mat2Name:cfg.mat2Name,series});
    }
  }
  return {error:null, required, requiredCopper, path};
}
