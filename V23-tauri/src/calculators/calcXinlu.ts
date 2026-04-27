/**
 * 星录养成计算引擎 - 基于 星录养成数据_AI版v3.xlsx
 * 4部星录（太微/紫微/天市/启明），每部8星官，每重6星
 *
 * 数据说明：
 * - 锤炼消耗表以太微为基准，4部星录消耗规则完全相同（只是材料名不同）
 * - 特殊：天市21-22重概率仅5%，保级大幅上升
 * - 特殊：启明17-20重保级消耗急增（17:12, 18:21, 19:34, 20:49/次）
 * - 20重概率约28%（期望次数3.56），与其他重段差异大
 */

export const XINLU_CONFIG: Record<string,{maxChong:number;lowMat:string;midMat:string;highMat:string;guard:string;guardName:string;upgradeStone:string;unlockLv:number;preReq:string}> = {
  "太微":{maxChong:20,lowMat:"南明离火",midMat:"九幽玄火",highMat:"红莲业火",guard:"灵运石",guardName:"灵运石",upgradeStone:"升重石",unlockLv:0,preReq:"无"},
  "紫微":{maxChong:20,lowMat:"破军寒玉",midMat:"贪狼煞玉",highMat:"天府瑞玉",guard:"仙运石",guardName:"仙运石",upgradeStone:"紫微升重玉",unlockLv:108,preReq:"太微达7重"},
  "天市":{maxChong:22,lowMat:"通财幽泉",midMat:"朔雪寒泉",highMat:"星河神泉",guard:"吉运石",guardName:"吉运石",upgradeStone:"天市升重圭",unlockLv:220,preReq:"紫微达7重"},
  "启明":{maxChong:20,lowMat:"百炼赤金",midMat:"千锻精金",highMat:"万融庚金",guard:"福运石",guardName:"福运石",upgradeStone:"启明升重石",unlockLv:260,preReq:"天市达5重"},
};
export const XINLU_NAMES = Object.keys(XINLU_CONFIG);

/**
 * 锤炼数据表：[重数, 星级, 单次消耗量, 期望次数, 期望主材料, 保级消耗/次, 期望保级消耗]
 * 来源：Excel「锤炼消耗表」，4部星录消耗规则完全相同
 * 特殊重段的保级差异通过 getGuardData() 在运行时处理
 */
type ForgeKey = string;
interface ForgeEntry { expMat:number; guardPer:number; expGuard:number; expTries:number; }
const FORGE_DATA: Record<ForgeKey, ForgeEntry> = {};

// RAW: [重数, 星级, 单次消耗, 期望次数, 期望主材料, 保级/次, 期望保级]
const RAW: [number,number,number,number,number,number,number][] = [
  [1,1,1,1.18,1.2,1,1.2],[1,2,1,1.18,1.2,1,1.2],[1,3,2,1.33,2.7,1,1.3],[1,4,2,1.33,2.7,1,1.3],[1,5,3,1.54,4.6,1,1.5],[1,6,3,1.54,4.6,1,1.5],
  [2,1,1,1.18,1.2,2,2.4],[2,2,1,1.18,1.2,2,2.4],[2,3,2,1.33,2.7,2,2.7],[2,4,2,1.33,2.7,2,2.7],[2,5,3,1.54,4.6,2,3.1],[2,6,3,1.54,4.6,2,3.1],
  [3,1,1,1.18,1.2,3,3.5],[3,2,1,1.18,1.2,3,3.5],[3,3,2,1.33,2.7,3,4],[3,4,2,1.33,2.7,3,4],[3,5,3,1.54,4.6,3,4.6],[3,6,3,1.54,4.6,3,4.6],
  [4,1,1,1.18,1.2,4,4.7],[4,2,1,1.18,1.2,4,4.7],[4,3,2,1.33,2.7,4,5.3],[4,4,2,1.33,2.7,4,5.3],[4,5,3,1.54,4.6,4,6.2],[4,6,3,1.54,4.6,4,6.2],
  [5,1,1,1.18,1.2,5,5.9],[5,2,1,1.18,1.2,5,5.9],[5,3,2,1.33,2.7,5,6.7],[5,4,2,1.33,2.7,5,6.7],[5,5,3,1.54,4.6,5,7.7],[5,6,3,1.54,4.6,5,7.7],
  [6,1,5,2,10,3,6],[6,2,5,2,10,3,6],[6,3,10,2.5,25,3,7.5],[6,4,10,2.5,25,3,7.5],[6,5,15,3.33,50,3,10],[6,6,15,3.33,50,3,10],
  [7,1,15,2,30,4,8],[7,2,15,2,30,4,8],[7,3,20,2.5,50,4,10],[7,4,20,2.5,50,4,10],[7,5,25,3.33,83.2,4,13.3],[7,6,25,3.33,83.2,4,13.3],
  [8,1,25,2,50,5,10],[8,2,25,2,50,5,10],[8,3,30,2.5,75,5,12.5],[8,4,30,2.5,75,5,12.5],[8,5,35,3.33,116.5,5,16.6],[8,6,35,3.33,116.5,5,16.6],
  [9,1,35,2.5,87.5,6,15],[9,2,35,2.5,87.5,6,15],[9,3,40,3.33,133.2,6,20],[9,4,40,3.33,133.2,6,20],[9,5,45,5,225,6,30],[9,6,45,5,225,6,30],
  [10,1,40,2.5,100,7,17.5],[10,2,40,2.5,100,7,17.5],[10,3,45,3.33,149.8,7,23.3],[10,4,45,3.33,149.8,7,23.3],[10,5,50,5,250,7,35],[10,6,50,5,250,7,35],
  [11,1,10,6.67,66.7,4,26.7],[11,2,10,6.67,66.7,4,26.7],[11,3,15,6.67,100,4,26.7],[11,4,15,6.67,100,4,26.7],[11,5,20,6.67,133.4,4,26.7],[11,6,20,6.67,133.4,4,26.7],
  [12,1,15,6.67,100,5,33.4],[12,2,15,6.67,100,5,33.4],[12,3,20,6.67,133.4,5,33.4],[12,4,20,6.67,133.4,5,33.4],[12,5,25,6.67,166.8,5,33.4],[12,6,25,6.67,166.8,5,33.4],
  [13,1,20,6.67,133.4,6,40],[13,2,20,6.67,133.4,6,40],[13,3,25,6.67,166.8,6,40],[13,4,25,6.67,166.8,6,40],[13,5,30,6.67,200.1,6,40],[13,6,30,6.67,200.1,6,40],
  [14,1,25,10,250,7,70],[14,2,25,10,250,7,70],[14,3,30,10,300,7,70],[14,4,30,10,300,7,70],[14,5,35,10,350,7,70],[14,6,35,10,350,7,70],
  [15,1,30,10,300,8,80],[15,2,30,10,300,8,80],[15,3,35,10,350,8,80],[15,4,35,10,350,8,80],[15,5,40,10,400,8,80],[15,6,40,10,400,8,80],
  [16,1,5,10,50,8,80],[16,2,5,10,50,8,80],[16,3,10,10,100,8,80],[16,4,10,10,100,8,80],[16,5,15,10,150,8,80],[16,6,15,10,150,8,80],
  [17,1,5,10,50,9,90],[17,2,5,10,50,9,90],[17,3,10,10,100,9,90],[17,4,10,10,100,9,90],[17,5,20,10,200,9,90],[17,6,20,10,200,9,90],
  [18,1,5,10,50,10,100],[18,2,5,10,50,10,100],[18,3,15,10,150,10,100],[18,4,15,10,150,10,100],[18,5,20,10,200,10,100],[18,6,20,10,200,10,100],
  [19,1,10,20,200,11,220],[19,2,10,20,200,11,220],[19,3,15,20,300,11,220],[19,4,15,20,300,11,220],[19,5,20,20,400,11,220],[19,6,20,20,400,11,220],
  // 20重：概率约28%，期望次数3.56，20重1星保级=0
  [20,1,10,3.56,35.556,0,0],[20,2,10,3.56,35.556,12,42.6673],[20,3,15,3.56,53.3341,12,42.6673],[20,4,15,3.56,53.3341,12,42.6673],[20,5,25,3.56,88.8901,12,42.6673],[20,6,25,3.56,88.8901,12,42.6673],
  // 天市 21-22重：概率仅5%，保级大幅上升
  [21,1,15,20,300,20,400],[21,2,15,20,300,20,400],[21,3,20,20,400,25,500],[21,4,20,20,400,25,500],[21,5,25,20,500,30,600],[21,6,25,20,500,30,600],
  [22,1,20,20,400,25,500],[22,2,20,20,400,25,500],[22,3,25,20,500,30,600],[22,4,25,20,500,30,600],[22,5,30,20,600,40,800],[22,6,30,20,600,40,800],
];
for (const r of RAW) {
  FORGE_DATA[`${r[0]}_${r[1]}`] = { expMat: r[4], guardPer: r[5], expGuard: r[6], expTries: r[3] };
}

/**
 * 启明17-20重保级消耗/次特殊覆盖表
 * 来源：Excel「星录基础信息」备注 + 「总消耗汇总」备注
 */
const QIMING_GUARD_PER: Record<number, number> = { 17: 12, 18: 21, 19: 34, 20: 49 };

function getMatTier(chong:number):"low"|"mid"|"high" { return chong<=10?"low":chong<=15?"mid":"high"; }

/**
 * 获取某星录某重某星的期望主材料消耗
 * 主材料消耗4部星录完全相同
 */
function getExpMat(chong:number, star:number):number {
  return FORGE_DATA[`${chong}_${star}`]?.expMat ?? 0;
}

/**
 * 获取某星录某重某星的期望保级消耗
 * 太微/紫微使用基准表数据
 * 天市使用基准表数据（21-22重已在RAW中体现）
 * 启明17-20重有特殊保级覆盖
 */
function getExpGuard(xinlu:string, chong:number, star:number):number {
  const entry = FORGE_DATA[`${chong}_${star}`];
  if (!entry) return 0;

  if (xinlu === "启明" && QIMING_GUARD_PER[chong] !== undefined) {
    const guardPerTry = QIMING_GUARD_PER[chong];
    return Math.round(entry.expTries * guardPerTry * 10000) / 10000;
  }

  return entry.expGuard;
}

export function calcByMaterials(xinlu:string, curChong:number, curStar:number, lowMat:number, midMat:number, highMat:number, guard:number) {
  const cfg = XINLU_CONFIG[xinlu];
  const used = {low:0,mid:0,high:0,guard:0};
  let chong = curChong, star = curStar, stopped = false;

  while (chong <= cfg.maxChong && !stopped) {
    if (chong > 20 && xinlu !== "天市") break;
    const startStar = star < 6 ? star + 1 : 7;
    for (let s = startStar; s <= 6; s++) {
      if (!FORGE_DATA[`${chong}_${s}`]) { stopped = true; break; }
      const expMat = getExpMat(chong, s);
      const expGuardVal = getExpGuard(xinlu, chong, s);
      const tier = getMatTier(chong);
      const pool = {low:lowMat,mid:midMat,high:highMat};
      if (pool[tier] !== Infinity && pool[tier] < expMat) { stopped = true; break; }
      if (guard !== Infinity && guard < expGuardVal) { stopped = true; break; }
      if (pool[tier] !== Infinity) {
        if (tier==="low") lowMat -= expMat; else if (tier==="mid") midMat -= expMat; else highMat -= expMat;
      }
      if (guard !== Infinity) guard -= expGuardVal;
      used[tier] += expMat; used.guard += expGuardVal; star = s;
    }
    if (stopped) break;
    if (star === 6 && chong < cfg.maxChong) { chong++; star = 0; }
    else break;
  }
  return {chong, star, used};
}

export function calcForTarget(xinlu:string, startChong:number, startStar:number, targetChong:number, targetStar:number) {
  const cfg = XINLU_CONFIG[xinlu];
  if (targetChong > cfg.maxChong) return {error:`${xinlu}最高${cfg.maxChong}重`, used:null};
  if (targetChong > 20 && xinlu !== "天市") return {error:`${xinlu}最高20重`, used:null};
  const used = {low:0,mid:0,high:0,guard:0};
  let chong = startChong, star = startStar;

  while (true) {
    if (chong > targetChong) break;
    if (chong === targetChong && star >= targetStar) break;
    const nextStar = star + 1;
    if (nextStar <= 6) {
      const endStar = chong < targetChong ? 6 : targetStar;
      for (let s = nextStar; s <= endStar; s++) {
        if (!FORGE_DATA[`${chong}_${s}`]) break;
        const tier = getMatTier(chong);
        used[tier] += getExpMat(chong, s);
        used.guard += getExpGuard(xinlu, chong, s);
      }
      star = endStar;
      if (chong === targetChong) break;
      if (star === 6 && chong < targetChong) { chong++; star = 0; } else break;
    } else if (star === 6) {
      if (chong < targetChong) { chong++; star = 0; } else break;
    } else break;
  }
  return {error:null, used};
}
