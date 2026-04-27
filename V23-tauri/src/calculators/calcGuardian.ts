/**
 * 守护神养成计算引擎 - 基于 守护神养成计算器开发说明_v4_final
 * 6个神仙谱组，含精华流转的逐张步进算法
 */

// 升星残念累计表
const STAR_CUM: Record<number,number> = {0:0, 1:20, 2:60, 3:140, 4:300, 5:300};

interface God { name:string; quality:string; weight:number; jinghua:number; expPerFu:number; }
interface Group { id:number; name:string; ticket:string; gods:God[]; }

const GROUPS: Group[] = [
  {id:1, name:"四值功曹", ticket:"四值请神符", gods:[
    {name:"值时功曹",quality:"蓝",weight:30,jinghua:2,expPerFu:4.918033},
    {name:"值日功曹",quality:"蓝绿",weight:15,jinghua:4,expPerFu:2.459016},
    {name:"值月功曹",quality:"蓝绿",weight:15,jinghua:4,expPerFu:2.459016},
    {name:"值年功曹",quality:"紫",weight:1,jinghua:60,expPerFu:0.417558},
  ]},
  {id:2, name:"日直六星", ticket:"日直请神符", gods:[
    {name:"显道神",quality:"蓝",weight:60,jinghua:4,expPerFu:3.225806},
    {name:"开路神",quality:"蓝",weight:60,jinghua:4,expPerFu:3.225806},
    {name:"增福神",quality:"蓝绿",weight:30,jinghua:8,expPerFu:1.612903},
    {name:"损福神",quality:"蓝绿",weight:30,jinghua:8,expPerFu:1.612903},
    {name:"日游神",quality:"紫",weight:3,jinghua:80,expPerFu:0.244624},
    {name:"夜游神",quality:"紫",weight:3,jinghua:80,expPerFu:0.244624},
  ]},
  {id:3, name:"九歌地神", ticket:"九歌请神符", gods:[
    {name:"河伯",quality:"蓝",weight:120,jinghua:8,expPerFu:6.593407},
    {name:"山鬼",quality:"蓝绿",weight:60,jinghua:16,expPerFu:3.296703},
    {name:"湘夫人",quality:"紫",weight:1,jinghua:240,expPerFu:0.138278},
    {name:"湘君",quality:"紫",weight:1,jinghua:240,expPerFu:0.138278},
  ]},
  {id:4, name:"云海天神", ticket:"云海请神符", gods:[
    {name:"地安神",quality:"蓝",weight:1200,jinghua:32,expPerFu:6.659267},
    {name:"天时神",quality:"蓝绿",weight:600,jinghua:64,expPerFu:3.329633},
    {name:"阴光神",quality:"紫",weight:1,jinghua:999,expPerFu:0.076978},
    {name:"阳炁神",quality:"紫",weight:1,jinghua:999,expPerFu:0.076978},
  ]},
  {id:5, name:"五德星君", ticket:"五德请神符", gods:[
    {name:"地侯星君",quality:"蓝",weight:4800,jinghua:64,expPerFu:5.648440},
    {name:"重华星君",quality:"蓝绿",weight:2400,jinghua:128,expPerFu:2.824220},
    {name:"伺辰星君",quality:"蓝绿",weight:1200,jinghua:128,expPerFu:1.412110},
    {name:"荧惑星君",quality:"紫",weight:90,jinghua:2000,expPerFu:0.230941},
    {name:"太白星君",quality:"金",weight:8,jinghua:4000,expPerFu:0.009416},
  ]},
  {id:6, name:"天元九歌", ticket:"天元请神符", gods:[
    {name:"大司命",quality:"蓝",weight:6000,jinghua:640,expPerFu:6.600660},
    {name:"云中君",quality:"蓝绿",weight:3000,jinghua:1280,expPerFu:3.300330},
    {name:"东君",quality:"紫",weight:45,jinghua:20000,expPerFu:0.099505},
    {name:"少司命",quality:"紫",weight:45,jinghua:20000,expPerFu:0.099505},
  ]},
];

export function getGroups() { return GROUPS; }
export function getGroup(name:string) { return GROUPS.find(g=>g.name===name); }
export function getGroupNames() { return GROUPS.map(g=>g.name); }

/**
 * 最常见星级分布（快速模式用）
 * 按各守护神期望残念速率占比加权分配总星级
 */
export function typicalDistribution(avgStar:number, group:Group): number[] {
  const n = group.gods.length;
  // 边界：0星全0，5星全5
  if (avgStar <= 0) return new Array(n).fill(0);
  if (avgStar >= 5) return new Array(n).fill(5);

  const totalStar = Math.round(avgStar * n);
  if (totalStar <= 0) return new Array(n).fill(0);
  if (totalStar >= n * 5) return new Array(n).fill(5);

  const totalExp = group.gods.reduce((s,g)=>s+g.expPerFu, 0);

  const raw = group.gods.map(g => totalStar * g.expPerFu / totalExp);
  const stars = raw.map(v => Math.min(5, Math.max(0, Math.round(v))));

  // 修正总和偏差
  let diff = totalStar - stars.reduce((s,v)=>s+v, 0);
  const residuals = raw.map((v,i) => ({r: v - Math.round(v), i}));
  residuals.sort((a,b) => diff > 0 ? b.r - a.r : a.r - b.r);
  for (const {i} of residuals) {
    if (diff === 0) break;
    if (diff > 0 && stars[i] < 5) { stars[i]++; diff--; }
    else if (diff < 0 && stars[i] > 0) { stars[i]--; diff++; }
  }
  return stars;
}

/**
 * 核心算法：含精华流转的逐张步进计算
 */
function calcFuNeeded(group:Group, curStars:number[], tgtStars:number[]): number {
  const n = group.gods.length;

  // 计算各神残念缺口
  const gaps = group.gods.map((_,i) => Math.max(0, STAR_CUM[tgtStars[i]] - STAR_CUM[curStars[i]]));

  // 检查是否已全部达标
  if (gaps.every(g => g <= 0)) return 0;

  // 逐张步进
  const acc = new Array(n).fill(0);  // 各神已积累残念
  const done = gaps.map(g => g <= 0);
  let jhPool = 0; // 精华池
  let fu = 0;

  while (!done.every(Boolean)) {
    fu++;
    if (fu > 100000) break; // 安全上限

    // 各神积累期望残念
    for (let i = 0; i < n; i++) {
      const g = group.gods[i];
      if (!done[i]) {
        acc[i] += g.expPerFu;
        if (acc[i] >= gaps[i]) {
          jhPool += (acc[i] - gaps[i]) * g.jinghua;
          acc[i] = gaps[i];
          done[i] = true;
        }
      } else {
        jhPool += g.expPerFu * g.jinghua;
      }
    }

    // 精华立即补贴（优先单价最高的未完成神）
    const undone = group.gods.map((_,i) => i).filter(i => !done[i]).sort((a,b) => group.gods[b].jinghua - group.gods[a].jinghua);
    for (const i of undone) {
      if (jhPool <= 0) break;
      const g = group.gods[i];
      const canBuy = Math.min(jhPool / g.jinghua, gaps[i] - acc[i]);
      if (canBuy > 0) {
        acc[i] += canBuy;
        jhPool -= canBuy * g.jinghua;
        if (acc[i] >= gaps[i]) {
          jhPool += (acc[i] - gaps[i]) * g.jinghua;
          acc[i] = gaps[i];
          done[i] = true;
        }
      }
    }
  }
  return fu;
}

/**
 * 快速计算：平均星级 → 请神符数量
 */
export function calcSimple(groupName:string, curAvg:number, tgtAvg:number) {
  const group = getGroup(groupName);
  if (!group) return {error:`未找到组: ${groupName}`};
  if (curAvg < 0 || curAvg > 5 || tgtAvg < 0 || tgtAvg > 5) return {error:"星级范围 0.0~5.0"};
  if (tgtAvg <= curAvg) return {error:"目标不能低于当前"};

  const curDist = typicalDistribution(curAvg, group);
  const tgtDistRaw = typicalDistribution(tgtAvg, group);
  // 强制目标 >= 当前
  const tgtDist = tgtDistRaw.map((v,i) => Math.max(v, curDist[i]));

  const n = group.gods.length;
  const curActualAvg = Math.round(curDist.reduce((s,v)=>s+v,0) / n * 100) / 100;
  const tgtActualAvg = Math.round(tgtDist.reduce((s,v)=>s+v,0) / n * 100) / 100;

  const fu = calcFuNeeded(group, curDist, tgtDist);

  const details = group.gods.map((g,i) => ({
    name: g.name, quality: g.quality,
    curStar: curDist[i], tgtStar: tgtDist[i],
    need: STAR_CUM[tgtDist[i]] - STAR_CUM[curDist[i]],
    expPerFu: Math.round(g.expPerFu * 10000) / 10000,
    jinghua: g.jinghua,
  }));

  return {
    error: null, groupName, ticket: group.ticket, fu,
    curDist, tgtDist, curActualAvg, tgtActualAvg,
    inputCurAvg: curAvg, inputTgtAvg: tgtAvg,
    details,
  };
}

/**
 * 精细计算：逐神星级 → 请神符数量
 */
export function calcPrecise(groupName:string, curStars:number[], tgtStars:number[]) {
  const group = getGroup(groupName);
  if (!group) return {error:`未找到组: ${groupName}`};
  if (curStars.length !== group.gods.length || tgtStars.length !== group.gods.length) return {error:"星级数组长度不匹配"};

  for (let i = 0; i < group.gods.length; i++) {
    if (tgtStars[i] < curStars[i]) return {error:`${group.gods[i].name}目标不能低于当前`};
  }

  const fu = calcFuNeeded(group, curStars, tgtStars);

  const details = group.gods.map((g,i) => ({
    name: g.name, quality: g.quality,
    curStar: curStars[i], tgtStar: tgtStars[i],
    need: STAR_CUM[tgtStars[i]] - STAR_CUM[curStars[i]],
    expPerFu: Math.round(g.expPerFu * 10000) / 10000,
    jinghua: g.jinghua,
  }));

  return { error: null, groupName, ticket: group.ticket, fu, details };
}
