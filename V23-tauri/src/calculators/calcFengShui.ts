/**
 * 风水录养成计算引擎 - 基于 风水录养成计算器参考数据_v2.xlsx
 * 4张宝图(北郡/琅琊盆地/昆仑/轩辕)，每张6个风水点，各点0→5星
 *
 * 使用逐星级消耗明细直接查表（Excel精确值），不做公式推算
 * 北郡有1星卡点额外消耗 = totalMain - sum(starMain)
 */

export const MAP_ORDER = ["北郡", "琅琊盆地", "昆仑", "轩辕"];

export interface FengShuiPoint {
  pid: number;
  map: string;
  name: string;
  mainMat: string;
  subMat: string | null;
  // starMain[0]=0→1星消耗, starMain[1]=1→2星, ..., starMain[4]=4→5星
  starMain: number[];
  starSub: number[];
  cardMain: number; // 卡点额外主材
  cardStar: number; // 卡点在哪个星级（0表示无卡点）
  totalMain: number;
  totalSub: number;
}

export const POINTS: FengShuiPoint[] = [
  // 北郡 - 有1星卡点(cardMain = totalMain - sum(starMain))
  {pid:1,map:"北郡",name:"平原村",mainMat:"神兽石",subMat:null,starMain:[50,76,100,126,170],starSub:[0,0,0,0,0],cardMain:6,cardStar:1,totalMain:528,totalSub:0},
  {pid:2,map:"北郡",name:"寂幻坛",mainMat:"神兽石",subMat:null,starMain:[50,76,100,126,170],starSub:[0,0,0,0,0],cardMain:6,cardStar:1,totalMain:528,totalSub:0},
  {pid:3,map:"北郡",name:"东夷祭坛",mainMat:"神兽石",subMat:null,starMain:[50,76,100,126,170],starSub:[0,0,0,0,0],cardMain:6,cardStar:1,totalMain:528,totalSub:0},
  {pid:4,map:"北郡",name:"天羽村",mainMat:"神兽石",subMat:null,starMain:[25,38,50,63,85],starSub:[0,0,0,0,0],cardMain:4,cardStar:1,totalMain:265,totalSub:0},
  {pid:5,map:"北郡",name:"遗逐村",mainMat:"神兽石",subMat:null,starMain:[25,38,50,63,85],starSub:[0,0,0,0,0],cardMain:4,cardStar:1,totalMain:265,totalSub:0},
  {pid:6,map:"北郡",name:"百果祀",mainMat:"神兽石",subMat:null,starMain:[25,38,50,63,85],starSub:[0,0,0,0,0],cardMain:4,cardStar:1,totalMain:265,totalSub:0},
  // 琅琊盆地 - 无卡点
  {pid:7,map:"琅琊盆地",name:"神祀",mainMat:"缠山图",subMat:"神兽石·星",starMain:[76,152,190,228,268],starSub:[76,152,190,228,268],cardMain:0,cardStar:0,totalMain:914,totalSub:914},
  {pid:8,map:"琅琊盆地",name:"七迷洞",mainMat:"缠山图",subMat:"神兽石·星",starMain:[76,152,190,228,268],starSub:[76,152,190,228,268],cardMain:0,cardStar:0,totalMain:914,totalSub:914},
  {pid:9,map:"琅琊盆地",name:"琅琊山",mainMat:"缠山图",subMat:"神兽石·星",starMain:[76,152,190,228,268],starSub:[76,152,190,228,268],cardMain:0,cardStar:0,totalMain:914,totalSub:914},
  {pid:10,map:"琅琊盆地",name:"长股村落",mainMat:"缠山图",subMat:"神兽石·星",starMain:[38,76,95,114,134],starSub:[76,152,190,228,268],cardMain:0,cardStar:0,totalMain:457,totalSub:914},
  {pid:11,map:"琅琊盆地",name:"长右村落",mainMat:"缠山图",subMat:"神兽石·星",starMain:[38,76,95,114,134],starSub:[76,152,190,228,268],cardMain:0,cardStar:0,totalMain:457,totalSub:914},
  {pid:12,map:"琅琊盆地",name:"东海崖",mainMat:"缠山图",subMat:"神兽石·星",starMain:[38,76,95,114,134],starSub:[76,152,190,228,268],cardMain:0,cardStar:0,totalMain:457,totalSub:914},
  // 昆仑 - 无卡点
  {pid:13,map:"昆仑",name:"翔舞部落",mainMat:"神兽石·月",subMat:"寻龍图",starMain:[108,218,272,326,380],starSub:[108,218,272,326,380],cardMain:0,cardStar:0,totalMain:1304,totalSub:1304},
  {pid:14,map:"昆仑",name:"延维聚落",mainMat:"神兽石·月",subMat:null,starMain:[108,218,272,326,380],starSub:[0,0,0,0,0],cardMain:0,cardStar:0,totalMain:1304,totalSub:0},
  {pid:15,map:"昆仑",name:"昆仑山",mainMat:"神兽石·月",subMat:"寻龍图",starMain:[54,109,136,163,190],starSub:[108,218,272,326,380],cardMain:0,cardStar:0,totalMain:652,totalSub:1304},
  {pid:16,map:"昆仑",name:"不冻泉",mainMat:"神兽石·月",subMat:null,starMain:[108,218,272,326,380],starSub:[0,0,0,0,0],cardMain:0,cardStar:0,totalMain:1304,totalSub:0},
  {pid:17,map:"昆仑",name:"蜃楼",mainMat:"神兽石·月",subMat:"寻龍图",starMain:[54,109,136,163,190],starSub:[108,218,272,326,380],cardMain:0,cardStar:0,totalMain:652,totalSub:1304},
  {pid:18,map:"昆仑",name:"玉珠峰",mainMat:"神兽石·月",subMat:"寻龍图",starMain:[108,218,272,326,380],starSub:[108,218,272,326,380],cardMain:0,cardStar:0,totalMain:1304,totalSub:1304},
  // 轩辕 - 无卡点
  {pid:19,map:"轩辕",name:"银明山",mainMat:"神兽石·日",subMat:"镇龍锁",starMain:[214,432,538,644,752],starSub:[214,432,538,644,752],cardMain:0,cardStar:0,totalMain:2580,totalSub:2580},
  {pid:20,map:"轩辕",name:"蛮牛野",mainMat:"神兽石·日",subMat:null,starMain:[214,432,538,644,752],starSub:[0,0,0,0,0],cardMain:0,cardStar:0,totalMain:2580,totalSub:0},
  {pid:21,map:"轩辕",name:"城西山",mainMat:"神兽石·日",subMat:null,starMain:[214,432,538,644,752],starSub:[0,0,0,0,0],cardMain:0,cardStar:0,totalMain:2580,totalSub:0},
  {pid:22,map:"轩辕",name:"城西村",mainMat:"神兽石·日",subMat:null,starMain:[214,432,538,644,752],starSub:[0,0,0,0,0],cardMain:0,cardStar:0,totalMain:2580,totalSub:0},
  {pid:23,map:"轩辕",name:"轩辕台",mainMat:"神兽石·日",subMat:"镇龍锁",starMain:[214,432,538,644,752],starSub:[214,432,538,644,752],cardMain:0,cardStar:0,totalMain:2580,totalSub:2580},
  {pid:24,map:"轩辕",name:"银明台",mainMat:"神兽石·日",subMat:"镇龍锁",starMain:[214,432,538,644,752],starSub:[214,432,538,644,752],cardMain:0,cardStar:0,totalMain:2580,totalSub:2580},
];

export const MAP_POINTS: Record<string, number[]> = {
  "北郡": [1,2,3,4,5,6], "琅琊盆地": [7,8,9,10,11,12],
  "昆仑": [13,14,15,16,17,18], "轩辕": [19,20,21,22,23,24],
};

function getPoint(pid: number): FengShuiPoint | undefined {
  return POINTS.find(p => p.pid === pid);
}

/** 计算单点从 startStar → targetStar 的消耗（逐星级累加） */
export function calcPointCost(pid: number, startStar: number, targetStar: number) {
  const pt = getPoint(pid);
  if (!pt) return { mainMat: "", mainCost: 0, subMat: null as string | null, subCost: 0 };
  let mainCost = 0, subCost = 0;
  for (let s = startStar; s < targetStar && s < 5; s++) {
    mainCost += pt.starMain[s];
    subCost += pt.starSub[s];
    // 卡点额外消耗：跨过卡点星级时加上
    if (pt.cardStar > 0 && s === pt.cardStar - 1) {
      mainCost += pt.cardMain;
    }
  }
  return { mainMat: pt.mainMat, mainCost, subMat: pt.subMat, subCost: pt.subMat ? subCost : 0 };
}

/** 功能一：目标规划 — 指定宝图+起止星级，计算全部6点消耗 */
export function calcMapTarget(mapName: string, startStar: number, targetStar: number) {
  const pids = MAP_POINTS[mapName] ?? [];
  const matSummary: Record<string, number> = {};
  const details: { name: string; mainMat: string; mainCost: number; subMat: string | null; subCost: number }[] = [];

  for (const pid of pids) {
    const pt = getPoint(pid)!;
    const cost = calcPointCost(pid, startStar, targetStar);
    matSummary[cost.mainMat] = (matSummary[cost.mainMat] || 0) + cost.mainCost;
    if (cost.subMat && cost.subCost > 0) {
      matSummary[cost.subMat] = (matSummary[cost.subMat] || 0) + cost.subCost;
    }
    details.push({ name: pt.name, mainMat: cost.mainMat, mainCost: cost.mainCost, subMat: cost.subMat, subCost: cost.subCost });
  }
  return { matSummary, details };
}

/** 功能二：资源评估 — 输入材料量，逐点推进，计算每点可达星级 */
export function calcMapByMaterials(mapName: string, curStar: number, materials: Record<string, number>) {
  const pids = MAP_POINTS[mapName] ?? [];
  const remaining = { ...materials };
  const results: { name: string; reachStar: number; used: Record<string, number> }[] = [];

  for (const pid of pids) {
    const pt = getPoint(pid)!;
    let star = curStar;
    const used: Record<string, number> = {};
    while (star < 5) {
      const cost = calcPointCost(pid, star, star + 1);
      if ((remaining[cost.mainMat] ?? 0) < cost.mainCost) break;
      if (cost.subMat && cost.subCost > 0 && (remaining[cost.subMat] ?? 0) < cost.subCost) break;
      remaining[cost.mainMat] -= cost.mainCost;
      used[cost.mainMat] = (used[cost.mainMat] ?? 0) + cost.mainCost;
      if (cost.subMat && cost.subCost > 0) {
        remaining[cost.subMat] -= cost.subCost;
        used[cost.subMat] = (used[cost.subMat] ?? 0) + cost.subCost;
      }
      star++;
    }
    results.push({ name: pt.name, reachStar: star, used });
  }
  return { results, remaining };
}

/** 获取某宝图使用的所有材料名 */
export function getMapMaterials(mapName: string): string[] {
  const pids = MAP_POINTS[mapName] ?? [];
  const s = new Set<string>();
  for (const pid of pids) {
    const pt = getPoint(pid)!;
    s.add(pt.mainMat);
    if (pt.subMat) s.add(pt.subMat);
  }
  return [...s].sort();
}
