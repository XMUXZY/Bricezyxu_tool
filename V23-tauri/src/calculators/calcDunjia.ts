/**
 * 遁甲（强运）养成计算引擎 - 移植自 calc_dunjia.py
 */

export const GRADES: Record<string,{maxLevel:number;material:string}> = {
  "黄阶":{maxLevel:36,material:"古迹灵石"},
  "玄阶":{maxLevel:49,material:"古迹灵石·玄"},
  "地阶":{maxLevel:64,material:"古迹灵石·地"},
  "天阶":{maxLevel:100,material:"古迹灵石·天"},
};
export const GRADE_ORDER = ["黄阶","玄阶","地阶","天阶"];

const LEVEL_DATA: Record<string,[number,number,number]> = {};
// 黄阶 1-36
let ab = 55;
for (let lv = 1; lv <= 36; lv++) { LEVEL_DATA[`黄阶_${lv}`] = [ab, 1, lv]; ab += 110; }
// 玄阶 1-49
ab = 40;
for (let lv = 1; lv <= 49; lv++) { LEVEL_DATA[`玄阶_${lv}`] = [ab, 1, lv]; ab += 60 + (lv - 1) * 30; }
// 地阶 1-64
ab = 28;
for (let lv = 1; lv <= 64; lv++) { LEVEL_DATA[`地阶_${lv}`] = [ab, 1, lv]; ab += 14 + (lv - 1) * 36; }
// 天阶 1-100
ab = 1590; let cum = 0;
for (let lv = 1; lv <= 100; lv++) {
  let cost = 1;
  if (lv > 99) cost = 18; else if (lv > 97) cost = 16; else if (lv > 95) cost = 14;
  else if (lv > 93) cost = 12; else if (lv > 91) cost = 10; else if (lv > 89) cost = 8;
  else if (lv > 87) cost = 6; else if (lv > 85) cost = 4; else if (lv > 83) cost = 3;
  else if (lv > 81) cost = 2;
  cum += cost; LEVEL_DATA[`天阶_${lv}`] = [ab, cost, cum]; ab += 9222;
}

function getLevelCost(grade:string,level:number):number { return LEVEL_DATA[`${grade}_${level}`]?.[1] ?? 0; }
function getCumulativeCost(grade:string,level:number):number { return LEVEL_DATA[`${grade}_${level}`]?.[2] ?? 0; }
function getAbility(grade:string,level:number):number { return LEVEL_DATA[`${grade}_${level}`]?.[0] ?? 0; }

export function calcReachableLevel(startGrade:string, startLevel:number, materials:Record<string,number>) {
  if (!GRADES[startGrade]) return {error:`无效的品阶: ${startGrade}`};
  if (Object.values(materials).every(v=>v===0)) return {error:"请输入至少一种材料的数量"};

  const startIdx = GRADE_ORDER.indexOf(startGrade);
  let currentLevel = startLevel, gradeName = startGrade;
  const usedMaterials: Record<string,number> = {}; for (const g of GRADE_ORDER) usedMaterials[g] = 0;
  const path: string[][] = [];

  for (let gi = startIdx; gi < GRADE_ORDER.length; gi++) {
    gradeName = GRADE_ORDER[gi];
    const maxLv = GRADES[gradeName].maxLevel;
    const matName = GRADES[gradeName].material;
    const available = materials[gradeName] ?? 0;
    const fromLv = gi === startIdx ? currentLevel : 0;

    for (let lv = fromLv + 1; lv <= maxLv; lv++) {
      const cost = getLevelCost(gradeName, lv);
      if (usedMaterials[gradeName] + cost <= available) {
        usedMaterials[gradeName] += cost;
        currentLevel = lv;
        path.push([gradeName,`Lv.${lv}`,String(getAbility(gradeName,lv)),`${matName} ×${cost}`,String(getCumulativeCost(gradeName,lv)),String(usedMaterials[gradeName])]);
      } else break;
    }
    if (currentLevel < maxLv) break;
    if (gi < GRADE_ORDER.length - 1) { currentLevel = 0; path.push([`【${gradeName}满级】`,"→",`进阶到${GRADE_ORDER[gi+1]}`,"无额外消耗","-","-"]); }
  }

  return {error:null, finalGrade:gradeName, finalLevel:currentLevel, usedMaterials, path};
}

export function calcRequiredMaterials(startGrade:string, startLevel:number, endGrade:string, endLevel:number) {
  if (!GRADES[startGrade] || !GRADES[endGrade]) return {error:"无效的品阶"};
  const startIdx = GRADE_ORDER.indexOf(startGrade), endIdx = GRADE_ORDER.indexOf(endGrade);
  if (endIdx < startIdx || (endIdx === startIdx && endLevel <= startLevel)) return {error:"目标等级必须高于当前等级"};

  const required: Record<string,number> = {}; for (const g of GRADE_ORDER) required[g] = 0;
  const path: string[][] = [];

  for (let gi = startIdx; gi <= endIdx; gi++) {
    const gn = GRADE_ORDER[gi];
    const maxLv = GRADES[gn].maxLevel, matName = GRADES[gn].material;
    const fromLv = gi === startIdx ? startLevel : 0;
    const toLv = gi === endIdx ? endLevel : maxLv;

    for (let lv = fromLv + 1; lv <= toLv; lv++) {
      const cost = getLevelCost(gn, lv);
      required[gn] += cost;
      path.push([gn,`Lv.${lv}`,String(getAbility(gn,lv)),`${matName} ×${cost}`,String(getCumulativeCost(gn,lv)),String(required[gn])]);
    }
    if (gi < endIdx) path.push([`【${gn}满级】`,"→",`进阶到${GRADE_ORDER[gi+1]}`,"无额外消耗","-","-"]);
  }

  return {error:null, required, path};
}
