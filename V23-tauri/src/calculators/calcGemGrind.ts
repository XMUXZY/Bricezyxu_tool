/**
 * 宝石磨砺养成计算引擎 - 移植自 calc_gem_grind.py
 */

interface GrindRow { level:number; stage:number; mat:string; qty:number; prob:number; acc:number; unlock?:string; }

const GRIND_POS12: GrindRow[] = [
  {level:1,stage:1,mat:"青暗紫砂",qty:4,prob:100,acc:5},{level:2,stage:1,mat:"青暗紫砂",qty:8,prob:100,acc:5},
  {level:3,stage:1,mat:"青暗紫砂",qty:8,prob:100,acc:5},{level:4,stage:1,mat:"青暗紫砂",qty:16,prob:100,acc:5},
  {level:5,stage:1,mat:"青暗紫砂",qty:16,prob:90,acc:5},{level:6,stage:1,mat:"青暗紫砂",qty:24,prob:90,acc:5},
  {level:7,stage:1,mat:"青暗紫砂",qty:24,prob:90,acc:5},{level:8,stage:1,mat:"青暗紫砂",qty:32,prob:90,acc:5},
  {level:9,stage:1,mat:"青暗紫砂",qty:32,prob:80,acc:4},{level:10,stage:1,mat:"青暗紫砂",qty:40,prob:80,acc:4,unlock:"玩家等级≥210"},
  {level:11,stage:1,mat:"青暗紫砂",qty:40,prob:80,acc:4},{level:12,stage:1,mat:"青暗紫砂",qty:48,prob:80,acc:4},
  {level:13,stage:1,mat:"青暗紫砂",qty:48,prob:70,acc:3},{level:14,stage:1,mat:"青暗紫砂",qty:56,prob:70,acc:3},
  {level:15,stage:1,mat:"青暗紫砂",qty:56,prob:70,acc:3},{level:16,stage:1,mat:"青暗紫砂",qty:64,prob:60,acc:2},
  {level:17,stage:1,mat:"青暗紫砂",qty:64,prob:60,acc:2},{level:18,stage:1,mat:"青暗紫砂",qty:72,prob:60,acc:2},
  {level:19,stage:1,mat:"青暗紫砂",qty:72,prob:50,acc:2},{level:20,stage:1,mat:"青暗紫砂",qty:80,prob:50,acc:2},
  {level:21,stage:2,mat:"墨紫玉砂",qty:4,prob:80,acc:4},{level:22,stage:2,mat:"墨紫玉砂",qty:8,prob:80,acc:4},
  {level:23,stage:2,mat:"墨紫玉砂",qty:8,prob:70,acc:3},{level:24,stage:2,mat:"墨紫玉砂",qty:16,prob:70,acc:3},
  {level:25,stage:2,mat:"墨紫玉砂",qty:16,prob:70,acc:3},{level:26,stage:2,mat:"墨紫玉砂",qty:24,prob:60,acc:2},
  {level:27,stage:2,mat:"墨紫玉砂",qty:24,prob:60,acc:2},{level:28,stage:2,mat:"墨紫玉砂",qty:32,prob:50,acc:2},
  {level:29,stage:2,mat:"墨紫玉砂",qty:40,prob:40,acc:2},
  {level:30,stage:3,mat:"琉璃灵砂",qty:4,prob:60,acc:5},{level:31,stage:3,mat:"琉璃灵砂",qty:4,prob:60,acc:5},
  {level:32,stage:3,mat:"琉璃灵砂",qty:8,prob:50,acc:5},{level:33,stage:3,mat:"琉璃灵砂",qty:8,prob:45,acc:4},
  {level:34,stage:3,mat:"琉璃灵砂",qty:16,prob:45,acc:4},{level:35,stage:3,mat:"琉璃灵砂",qty:16,prob:40,acc:4},
  {level:36,stage:3,mat:"琉璃灵砂",qty:24,prob:35,acc:3},{level:37,stage:3,mat:"琉璃灵砂",qty:24,prob:30,acc:3},
  {level:38,stage:3,mat:"琉璃灵砂",qty:32,prob:25,acc:3},{level:39,stage:3,mat:"琉璃灵砂",qty:32,prob:20,acc:3},
  {level:40,stage:3,mat:"琉璃灵砂",qty:40,prob:20,acc:3},
];

const POS3_MAP: Record<string,string> = {"青暗紫砂":"邃夜黑砂","墨紫玉砂":"乌金玉砂","琉璃灵砂":"黑曜灵砂"};
const GRIND_POS3: GrindRow[] = GRIND_POS12.map(r => ({...r, mat: POS3_MAP[r.mat] ?? r.mat}));

export const COPPER_PER_LEVEL = 10000;
export const MAX_LEVEL = 40;
export function getData(isPos3:boolean) { return isPos3 ? GRIND_POS3 : GRIND_POS12; }

export function calcByMaterials(curLv:number, isPos3:boolean, useExpected:boolean, mats:Record<string,number>, copper:number) {
  const data = getData(isPos3);
  let lv = curLv;
  const remMats = {...mats}; let remCopper = copper;
  const usedMats: Record<string,number> = {}; for (const k in mats) usedMats[k] = 0;
  let usedCopper = 0;

  for (const row of data) {
    if (lv >= row.level) continue;
    const costQty = useExpected && row.prob < 100 ? row.qty / (row.prob / 100) : row.qty;
    if (remMats[row.mat] !== Infinity && remMats[row.mat] < costQty) break;
    if (remCopper !== Infinity && remCopper < COPPER_PER_LEVEL) break;
    if (remMats[row.mat] !== Infinity) { remMats[row.mat] -= costQty; usedMats[row.mat] = (usedMats[row.mat]??0) + costQty; }
    if (remCopper !== Infinity) { remCopper -= COPPER_PER_LEVEL; usedCopper += COPPER_PER_LEVEL; }
    lv = row.level;
  }
  return { error:null, finalLevel:lv, usedMats, usedCopper };
}

export function calcForTarget(startLv:number, targetLv:number, isPos3:boolean) {
  if (targetLv <= startLv) return {error:"目标等级必须大于起始等级"};
  const data = getData(isPos3);
  const detMats: Record<string,number> = {}, expMats: Record<string,number> = {};
  let totalCopper = 0;

  for (const row of data) {
    if (row.level <= startLv || row.level > targetLv) continue;
    detMats[row.mat] = (detMats[row.mat]??0) + row.qty;
    totalCopper += COPPER_PER_LEVEL;
    const expQty = row.prob >= 100 ? row.qty : row.qty / (row.prob / 100);
    expMats[row.mat] = (expMats[row.mat]??0) + expQty;
  }
  return { error:null, detMats, expMats, totalCopper };
}
