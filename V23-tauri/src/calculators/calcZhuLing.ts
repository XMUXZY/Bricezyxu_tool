/**
 * 注灵养成计算引擎 - 基于 注灵养成数据_经典区v2.xlsx
 * 8套注灵，每套10级，11个装备部位
 *
 * 每级消耗 = 开启材料(全部位) + 重刷主材料(全部位×期望次数) + 重刷保底材料(全部位×期望次数)
 * Excel 中 openTotal/refreshTotal/guardTotal 已是全11部位的总量
 */

export const SET_ORDER = ["神农","女娲","伏羲","轩辕","鸿钧","混元","夸父","蚩尤"];

interface LevelData {
  lv: number;
  openMat: string;   openTotal: number;
  refreshMat: string; refreshTotal: number;
  guardMat: string;   guardTotal: number;
}

interface SetInfo {
  name: string;
  unlockLv: number;
  guardMat: string;
  levels: LevelData[];
}

const SETS: Record<string, SetInfo> = {};

// [套装,解锁等级,等级,开启材料名,开启全位,刷新材料名,刷新全位总消耗,保底材料名,保底全位总消耗]
const RAW: [string,number,number,string,number,string,number,string,number][] = [
  ["神农",109,1,"普通神农草",22,"普通神农草",66,"新月之石",66],["神农",109,2,"普通神农草",44,"普通神农草",132,"新月之石",66],["神农",109,3,"普通神农草",66,"普通神农草",198,"新月之石",66],["神农",109,4,"普通神农草",88,"普通神农草",264,"新月之石",66],["神农",109,5,"普通神农草",110,"普通神农草",330,"新月之石",66],
  ["神农",109,6,"温润神农草",44,"温润神农草",132,"新月之石",66],["神农",109,7,"温润神农草",66,"温润神农草",198,"新月之石",66],["神农",109,8,"温润神农草",88,"温润神农草",264,"新月之石",66],["神农",109,9,"温润神农草",110,"温润神农草",330,"新月之石",66],["神农",109,10,"温润神农草",132,"温润神农草",396,"新月之石",66],
  ["女娲",117,1,"普通女娲石",44,"普通女娲石",132,"新月之石",132],["女娲",117,2,"普通女娲石",66,"普通女娲石",198,"新月之石",132],["女娲",117,3,"普通女娲石",88,"普通女娲石",264,"新月之石",132],["女娲",117,4,"普通女娲石",110,"普通女娲石",330,"新月之石",132],["女娲",117,5,"普通女娲石",132,"普通女娲石",396,"新月之石",132],
  ["女娲",117,6,"玲珑女娲石",44,"玲珑女娲石",132,"新月之石",132],["女娲",117,7,"玲珑女娲石",66,"玲珑女娲石",198,"新月之石",132],["女娲",117,8,"玲珑女娲石",88,"玲珑女娲石",264,"新月之石",132],["女娲",117,9,"玲珑女娲石",110,"玲珑女娲石",330,"新月之石",132],["女娲",117,10,"玲珑女娲石",132,"玲珑女娲石",396,"新月之石",132],
  ["伏羲",121,1,"普通伏羲卦",44,"普通伏羲卦",132,"新月之石",264],["伏羲",121,2,"普通伏羲卦",66,"普通伏羲卦",198,"新月之石",264],["伏羲",121,3,"普通伏羲卦",88,"普通伏羲卦",264,"新月之石",264],["伏羲",121,4,"普通伏羲卦",110,"普通伏羲卦",330,"新月之石",264],["伏羲",121,5,"普通伏羲卦",132,"普通伏羲卦",396,"新月之石",264],
  ["伏羲",121,6,"开光伏羲卦",44,"开光伏羲卦",132,"新月之石",264],["伏羲",121,7,"开光伏羲卦",66,"开光伏羲卦",198,"新月之石",264],["伏羲",121,8,"开光伏羲卦",88,"开光伏羲卦",264,"新月之石",264],["伏羲",121,9,"开光伏羲卦",110,"开光伏羲卦",330,"新月之石",264],["伏羲",121,10,"开光伏羲卦",132,"开光伏羲卦",396,"新月之石",264],
  ["轩辕",131,1,"普通轩辕令",44,"普通轩辕令",132,"新月之石",396],["轩辕",131,2,"普通轩辕令",66,"普通轩辕令",198,"新月之石",396],["轩辕",131,3,"普通轩辕令",88,"普通轩辕令",264,"新月之石",396],["轩辕",131,4,"普通轩辕令",110,"普通轩辕令",330,"新月之石",396],["轩辕",131,5,"普通轩辕令",132,"普通轩辕令",396,"新月之石",396],
  ["轩辕",131,6,"天赐轩辕令",44,"天赐轩辕令",132,"新月之石",396],["轩辕",131,7,"天赐轩辕令",66,"天赐轩辕令",198,"新月之石",396],["轩辕",131,8,"天赐轩辕令",88,"天赐轩辕令",264,"新月之石",396],["轩辕",131,9,"天赐轩辕令",110,"天赐轩辕令",330,"新月之石",396],["轩辕",131,10,"天赐轩辕令",132,"天赐轩辕令",396,"新月之石",396],
  ["鸿钧",141,1,"鸿钧石",44,"鸿钧石",132,"紫霄石",132],["鸿钧",141,2,"鸿钧石",66,"鸿钧石",132,"紫霄石",132],["鸿钧",141,3,"鸿钧石",88,"鸿钧石",132,"紫霄石",132],["鸿钧",141,4,"鸿钧石",121,"鸿钧石",264,"紫霄石",264],["鸿钧",141,5,"鸿钧石",143,"鸿钧石",264,"紫霄石",264],
  ["鸿钧",141,6,"鸿钧石",165,"鸿钧石",264,"紫霄石",264],["鸿钧",141,7,"鸿钧石",187,"鸿钧石",264,"紫霄石",528],["鸿钧",141,8,"鸿钧石",220,"鸿钧石",396,"紫霄石",528],["鸿钧",141,9,"鸿钧石",242,"鸿钧石",396,"紫霄石",528],["鸿钧",141,10,"鸿钧石",264,"鸿钧石",396,"紫霄石",528],
  ["混元",209,1,"混元珠",44,"混元珠",132,"太一石",132],["混元",209,2,"混元珠",66,"混元珠",132,"太一石",132],["混元",209,3,"混元珠",88,"混元珠",132,"太一石",132],["混元",209,4,"混元珠",121,"混元珠",264,"太一石",264],["混元",209,5,"混元珠",143,"混元珠",264,"太一石",264],
  ["混元",209,6,"混元珠",165,"混元珠",264,"太一石",264],["混元",209,7,"混元珠",187,"混元珠",264,"太一石",528],["混元",209,8,"混元珠",220,"混元珠",396,"太一石",528],["混元",209,9,"混元珠",242,"混元珠",396,"太一石",528],["混元",209,10,"混元珠",264,"混元珠",396,"太一石",528],
  ["夸父",300,1,"桃木令",11,"桃木令",132,"渭水晶",132],["夸父",300,2,"桃木令",22,"桃木令",132,"渭水晶",132],["夸父",300,3,"桃木令",44,"桃木令",132,"渭水晶",132],["夸父",300,4,"桃木令",66,"桃木令",264,"渭水晶",264],["夸父",300,5,"桃木令",88,"桃木令",264,"渭水晶",264],
  ["夸父",300,6,"桃木令",88,"桃木令",264,"渭水晶",264],["夸父",300,7,"桃木令",110,"桃木令",264,"渭水晶",528],["夸父",300,8,"桃木令",110,"桃木令",396,"渭水晶",528],["夸父",300,9,"桃木令",132,"桃木令",396,"渭水晶",528],["夸父",300,10,"桃木令",165,"桃木令",396,"渭水晶",528],
  ["蚩尤",330,1,"盐泽泉",44,"盐泽泉",132,"黎炎石",132],["蚩尤",330,2,"盐泽泉",44,"盐泽泉",132,"黎炎石",132],["蚩尤",330,3,"盐泽泉",88,"盐泽泉",396,"黎炎石",396],["蚩尤",330,4,"盐泽泉",66,"盐泽泉",264,"黎炎石",264],["蚩尤",330,5,"盐泽泉",66,"盐泽泉",264,"黎炎石",264],
  ["蚩尤",330,6,"盐泽泉",77,"盐泽泉",330,"黎炎石",330],["蚩尤",330,7,"盐泽泉",77,"盐泽泉",330,"黎炎石",330],["蚩尤",330,8,"盐泽泉",154,"盐泽泉",792,"黎炎石",792],["蚩尤",330,9,"盐泽泉",110,"盐泽泉",396,"黎炎石",396],["蚩尤",330,10,"盐泽泉",110,"盐泽泉",396,"黎炎石",396],
];

for (const r of RAW) {
  const [setName,unlockLv,lv,openMat,openTotal,refreshMat,refreshTotal,guardMat,guardTotal] = r;
  if (!SETS[setName]) SETS[setName] = { name:setName, unlockLv, guardMat, levels:[] };
  SETS[setName].levels.push({ lv, openMat, openTotal, refreshMat, refreshTotal, guardMat, guardTotal });
}

export function getSetInfo(setName:string): SetInfo|null { return SETS[setName] ?? null; }
export function getSetNames(): string[] { return SET_ORDER; }

export function getMatNames(setName:string): {openMats:string[]; refreshMats:string[]; guardMat:string} {
  const info = SETS[setName];
  if (!info) return {openMats:[],refreshMats:[],guardMat:""};
  const openSet = new Set<string>(); const refSet = new Set<string>();
  for (const l of info.levels) { openSet.add(l.openMat); refSet.add(l.refreshMat); }
  return { openMats:[...openSet], refreshMats:[...refSet], guardMat:info.guardMat };
}

/** 功能一：根据材料计算可达等级 */
export function calcByMaterials(setName:string, startLv:number, holdings:Record<string,number>) {
  const info = SETS[setName];
  if (!info) return {error:"未找到套装数据"};
  if (startLv >= 10) return {error:"已满级(10级)"};

  const current = {...holdings};
  let reachLv = startLv;
  const tableData: {lv:number;openMat:string;openNeed:number;refreshMat:string;refreshNeed:number;guardMat:string;guardNeed:number;status:string}[] = [];

  for (let i = startLv; i < info.levels.length; i++) {
    const d = info.levels[i];
    const openAvail = current[d.openMat] ?? 0;
    const refreshAvail = current[d.refreshMat] ?? 0;
    const guardAvail = current[d.guardMat] ?? 0;

    const canOpen = openAvail >= d.openTotal;
    const canRefresh = refreshAvail >= d.refreshTotal;
    const canGuard = guardAvail >= d.guardTotal;

    if (!canOpen || !canRefresh || !canGuard) {
      const lacks: string[] = [];
      if (!canOpen) lacks.push(`${d.openMat}不足(差${d.openTotal-openAvail})`);
      if (!canRefresh) lacks.push(`${d.refreshMat}不足(差${d.refreshTotal-refreshAvail})`);
      if (!canGuard) lacks.push(`${d.guardMat}不足(差${d.guardTotal-guardAvail})`);
      tableData.push({lv:d.lv,openMat:d.openMat,openNeed:d.openTotal,refreshMat:d.refreshMat,refreshNeed:d.refreshTotal,guardMat:d.guardMat,guardNeed:d.guardTotal,status:`❌ ${lacks.join("、")}`});
      break;
    }

    current[d.openMat] = openAvail - d.openTotal;
    current[d.refreshMat] = refreshAvail - d.refreshTotal;
    current[d.guardMat] = guardAvail - d.guardTotal;
    reachLv = d.lv;
    tableData.push({lv:d.lv,openMat:d.openMat,openNeed:d.openTotal,refreshMat:d.refreshMat,refreshNeed:d.refreshTotal,guardMat:d.guardMat,guardNeed:d.guardTotal,status:"✅"});
  }

  return {error:null, reachLv, tableData};
}

/** 功能二：根据目标计算所需材料 */
export function calcByTarget(setName:string, startLv:number, targetLv:number) {
  const info = SETS[setName];
  if (!info) return {error:"未找到套装数据"};
  if (targetLv <= startLv) return {error:"目标等级需大于起始等级"};
  if (targetLv > 10) return {error:"最高10级"};

  const totals: Record<string,number> = {};
  const tableData: {lv:number;openMat:string;openNeed:number;refreshMat:string;refreshNeed:number;guardMat:string;guardNeed:number}[] = [];

  for (let i = startLv; i < targetLv && i < info.levels.length; i++) {
    const d = info.levels[i];
    totals[`开启:${d.openMat}`] = (totals[`开启:${d.openMat}`]??0) + d.openTotal;
    totals[`重刷:${d.refreshMat}`] = (totals[`重刷:${d.refreshMat}`]??0) + d.refreshTotal;
    totals[`保底:${d.guardMat}`] = (totals[`保底:${d.guardMat}`]??0) + d.guardTotal;
    tableData.push({lv:d.lv,openMat:d.openMat,openNeed:d.openTotal,refreshMat:d.refreshMat,refreshNeed:d.refreshTotal,guardMat:d.guardMat,guardNeed:d.guardTotal});
  }

  return {error:null, unlockLv:info.unlockLv, totals, tableData};
}
