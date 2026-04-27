/**
 * 青龙星图养成计算引擎 - 基于 青龙星图材料消耗表.xlsx
 * 7个星官，每个10重×6级，概率增量公式精确计算
 *
 * 材料说明：
 * - 碧木星砂(1-4重) / 云隐星砂(5-7重) / 龙威星砂(8-10重)：锤炼主材料
 * - 青龙之灵：保级材料，每次锤炼消耗（含1级）
 * - 青龙碎晶：升重材料，升至X重需 X×10 颗/星官
 */

export const OFFICIALS = ["角木蛟","亢金龙","氐土貉","房日兔","心月狐","尾火虎","箕水豹"];
export const MAX_WEIGHT = 10;
export const MAX_LEVEL = 6;

export const MAT_NAMES = {
  low: "碧木星砂",
  mid: "云隐星砂",
  high: "龙威星砂",
  guard: "青龙之灵",
  crystal: "青龙碎晶",
};

/** 升重碎晶消耗：升至X重需 X×10 颗/星官 */
export const UPGRADE_CRYSTAL: Record<number,number> = {
  2:20, 3:30, 4:40, 5:50, 6:60, 7:70, 8:80, 9:90, 10:100
};

function getMatTier(w:number): "low"|"mid"|"high" {
  return w <= 4 ? "low" : w <= 7 ? "mid" : "high";
}

interface ForgeEntry { expMat:number; expGuard:number; }
const FORGE: Record<string, ForgeEntry> = {};

// RAW: [重数, 星级, 单次消耗, 期望次数, 期望主材料, 保级/次, 期望保级]
const RAW: [number,number,number,number,number,number,number][] = [
  [1,1,15,1.345,20.175,2,2.69],[1,2,15,1.345,20.175,2,2.69],[1,3,20,1.51,30.2,2,3.02],[1,4,20,1.51,30.2,3,4.53],[1,5,25,1.7117,42.7937,3,5.1352],[1,6,25,1.7117,42.7937,3,5.1352],
  [2,1,30,1.4235,42.705,4,5.694],[2,2,30,1.4235,42.705,4,5.694],[2,3,35,1.6053,56.1838,4,6.421],[2,4,35,1.7117,59.9112,5,8.5587],[2,5,40,1.8305,73.22,5,9.1525],[2,6,40,1.9632,78.526,5,9.8158],
  [3,1,45,1.51,67.95,6,9.06],[3,2,45,1.51,67.95,6,9.06],[3,3,50,1.7117,85.5875,6,10.2705],[3,4,50,1.8305,91.525,8,14.644],[3,5,55,1.9632,107.9733,8,15.7052],[3,6,55,2.1126,116.1951,8,16.9011],
  [4,1,60,1.7117,102.705,10,17.1175],[4,2,60,1.8305,109.83,10,18.305],[4,3,65,1.9632,127.6048,10,19.6315],[4,4,65,2.1126,137.3214,12,25.3517],[4,5,75,2.2813,171.1012,12,27.3762],[4,6,75,2.2813,171.1012,12,27.3762],
  [5,1,30,1.7117,51.3525,15,25.6762],[5,2,32,1.8305,58.576,15,27.4575],[5,3,34,1.9632,66.7471,15,29.4473],[5,4,36,2.1126,76.055,15,31.6896],[5,5,38,2.2813,86.6913,15,34.2202],[5,6,40,2.2813,91.254,15,34.2202],
  [6,1,42,1.9632,82.4523,15,29.4473],[6,2,44,1.9632,86.3786,15,29.4473],[6,3,46,2.2813,104.9421,15,34.2202],[6,4,48,2.2813,109.5048,15,34.2202],[6,5,50,2.6901,134.5055,15,40.3517],[6,6,54,2.6901,145.2659,15,40.3517],
  [7,1,60,1.9632,117.789,15,29.4473],[7,2,66,1.9632,129.5679,15,29.4473],[7,3,72,2.2813,164.2572,15,34.2202],[7,4,78,2.2813,177.9453,15,34.2202],[7,5,84,2.6901,225.9692,15,40.3517],[7,6,90,2.6901,242.1099,15,40.3517],
  [8,1,20,2.4724,49.4472,25,61.8091],[8,2,20,2.4724,49.4472,25,61.8091],[8,3,24,2.6901,64.5626,25,67.2528],[8,4,24,2.6901,64.5626,25,67.2528],[8,5,28,2.9391,82.2961,25,73.4787],[8,6,28,2.9391,82.2961,25,73.4787],
  [9,1,32,2.9391,94.0527,25,73.4787],[9,2,32,2.9391,94.0527,25,73.4787],[9,3,36,3.2251,116.1045,25,80.6282],[9,4,36,3.2251,116.1045,25,80.6282],[9,5,40,3.5556,142.2242,25,88.8901],[9,6,40,3.5556,142.2242,25,88.8901],
  [10,1,44,3.2251,141.9056,25,80.6282],[10,2,44,3.2251,141.9056,25,80.6282],[10,3,48,3.2251,154.8061,25,80.6282],[10,4,48,3.5556,170.669,25,88.8901],[10,5,52,3.5556,184.8914,25,88.8901],[10,6,52,3.5556,184.8914,25,88.8901],
];
for (const r of RAW) {
  FORGE[`${r[0]}_${r[1]}`] = { expMat: r[4], expGuard: r[6] };
}

/**
 * 功能一：指定起止(重,级) → 计算区间消耗
 */
export function calcForTarget(
  startW:number, startL:number, targetW:number, targetL:number, officialCount:number = 7
) {
  if (targetW < startW || (targetW === startW && targetL <= startL)) {
    return { error: "目标必须高于当前状态" };
  }
  if (targetW > MAX_WEIGHT || targetL > MAX_LEVEL) {
    return { error: `最高 ${MAX_WEIGHT}重${MAX_LEVEL}级` };
  }

  const used = { low:0, mid:0, high:0, guard:0, crystal:0 };

  // 升重碎晶
  const crystalFromW = startL === 6 ? startW + 1 : (startL === 0 && startW > 0 ? startW : startW);
  for (let w = 1; w <= MAX_WEIGHT; w++) {
    if (w <= startW) continue;
    if (w > targetW) break;
    used.crystal += (UPGRADE_CRYSTAL[w] ?? 0);
  }

  // 锤炼消耗
  let w = startW === 0 ? 1 : startW;
  let l = startL;
  if (startW === 0) { l = 0; }

  while (w < targetW || (w === targetW && l < targetL)) {
    const nextL = l + 1;
    if (nextL > MAX_LEVEL) { w++; l = 0; continue; }
    if (w > targetW || (w === targetW && nextL > targetL)) break;

    const entry = FORGE[`${w}_${nextL}`];
    if (!entry) break;
    const tier = getMatTier(w);
    used[tier] += entry.expMat;
    used.guard += entry.expGuard;
    l = nextL;
  }

  // 乘以星官数
  const total = {
    low: Math.round(used.low * officialCount * 10) / 10,
    mid: Math.round(used.mid * officialCount * 10) / 10,
    high: Math.round(used.high * officialCount * 10) / 10,
    guard: Math.round(used.guard * officialCount * 10) / 10,
    crystal: used.crystal * officialCount,
  };
  const single = {
    low: Math.round(used.low * 10) / 10,
    mid: Math.round(used.mid * 10) / 10,
    high: Math.round(used.high * 10) / 10,
    guard: Math.round(used.guard * 10) / 10,
    crystal: used.crystal,
  };

  return { error: null, single, total, officialCount };
}

/**
 * 功能二：指定起点 + 材料量 → 计算可达终点
 */
export function calcByMaterials(
  startW:number, startL:number,
  mats: { low:number; mid:number; high:number; guard:number },
  officialCount:number = 7
) {
  // 材料按星官平分
  const perMat = {
    low: mats.low === Infinity ? Infinity : mats.low / officialCount,
    mid: mats.mid === Infinity ? Infinity : mats.mid / officialCount,
    high: mats.high === Infinity ? Infinity : mats.high / officialCount,
    guard: mats.guard === Infinity ? Infinity : mats.guard / officialCount,
  };

  const used = { low:0, mid:0, high:0, guard:0 };
  let w = startW === 0 ? 1 : startW;
  let l = startL;
  if (startW === 0) { l = 0; }
  let reachedW = startW, reachedL = startL;

  while (w <= MAX_WEIGHT) {
    const nextL = l + 1;
    if (nextL > MAX_LEVEL) {
      // 需要升重
      if (w >= MAX_WEIGHT) break;
      w++; l = 0; continue;
    }
    const entry = FORGE[`${w}_${nextL}`];
    if (!entry) break;

    const tier = getMatTier(w);
    const remMat = perMat[tier] === Infinity ? Infinity : perMat[tier] - used[tier];
    const remGuard = perMat.guard === Infinity ? Infinity : perMat.guard - used.guard;

    if (remMat < entry.expMat || remGuard < entry.expGuard) break;

    used[tier] += entry.expMat;
    used.guard += entry.expGuard;
    l = nextL;
    reachedW = w; reachedL = l;
  }

  const totalUsed = {
    low: Math.round(used.low * officialCount * 10) / 10,
    mid: Math.round(used.mid * officialCount * 10) / 10,
    high: Math.round(used.high * officialCount * 10) / 10,
    guard: Math.round(used.guard * officialCount * 10) / 10,
  };
  const singleUsed = {
    low: Math.round(used.low * 10) / 10,
    mid: Math.round(used.mid * 10) / 10,
    high: Math.round(used.high * 10) / 10,
    guard: Math.round(used.guard * 10) / 10,
  };

  return { error: null, reachedW, reachedL, singleUsed, totalUsed, officialCount };
}
