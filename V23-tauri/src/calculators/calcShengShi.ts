/**
 * 圣石养成计算引擎 - 基于 圣石养成数据_经典区v3.xlsx
 *
 * 三类石头（均有10%暴击3倍，期望×1.2）：
 * - 圣石(栏位1)：最高120级，只消耗积分，满级≈206,904积分
 * - 玄石(栏位2)：最高360级，消耗积分+同系最低阶圣石，满级≈185,533积分+62,595圣石
 * - 罡石(栏位3)：最高150级，消耗积分+同类罡石道具，满级≈6,320积分+15,123道具
 *
 * 数据为期望值（含暴击修正），从 JSON 加载累计值查表
 * 区间消耗 = cumJf[target] - cumJf[start]
 */

export const SLOTS = [
  { key: "圣石", label: "圣石(栏位1)", maxLv: 120, hasItem: false, itemName: "", desc: "只消耗积分" },
  { key: "玄石", label: "玄石(栏位2)", maxLv: 360, hasItem: true, itemName: "同系最低阶圣石", desc: "积分+圣石" },
  { key: "罡石", label: "罡石(栏位3)", maxLv: 150, hasItem: true, itemName: "同类罡石道具", desc: "积分+罡石道具" },
];

interface CumEntry { lv: number; jf: number; item: number; cumJf: number; cumItem: number; }

const CUM: Record<string, Record<number, CumEntry>> = {
  "圣石": { 0:{lv:0,jf:0,item:0,cumJf:0,cumItem:0}, 1:{lv:1,jf:0,item:0,cumJf:0,cumItem:0} },
  "玄石": { 0:{lv:0,jf:0,item:0,cumJf:0,cumItem:0} },
  "罡石": { 0:{lv:0,jf:0,item:0,cumJf:0,cumItem:0} },
};
let _loaded = false;
let _loadPromise: Promise<void> | null = null;

export async function ensureData(): Promise<void> {
  if (_loaded) return;
  if (_loadPromise) { await _loadPromise; return; }
  _loadPromise = (async () => {
    const resp = await fetch('/game_data/shengshi_data.json');
    const json = await resp.json();
    for (const [lv, jf, cumJf] of json.stone as number[][]) {
      CUM["圣石"][lv] = { lv, jf, item: 0, cumJf, cumItem: 0 };
    }
    for (const [lv, jf, item, cumJf, cumItem] of json.xuan as number[][]) {
      CUM["玄石"][lv] = { lv, jf, item, cumJf, cumItem };
    }
    for (const [lv, jf, item, cumJf, cumItem] of json.gang as number[][]) {
      CUM["罡石"][lv] = { lv, jf, item, cumJf, cumItem };
    }
    _loaded = true;
  })();
  await _loadPromise;
}

function getSlot(label: string) {
  return SLOTS.find(s => label.includes(s.key)) ?? SLOTS[0];
}

/** 功能一：根据材料计算可达等级 */
export async function calcByMaterials(slot: string, curLv: number, jf: number, itemVal: number) {
  await ensureData();
  const s = getSlot(slot);
  const cum = CUM[s.key];
  let lv = curLv, totalJf = 0, totalItem = 0, steps = 0;
  let remJf = jf, remItem = itemVal;

  while (lv < s.maxLv) {
    const nextLv = lv + 1;
    const curE = cum[lv], nextE = cum[nextLv];
    if (!curE || !nextE) break;
    const needJf = nextE.cumJf - curE.cumJf;
    const needItem = s.hasItem ? (nextE.cumItem - curE.cumItem) : 0;
    if (needJf <= 0 && needItem <= 0) { lv = nextLv; steps++; continue; }
    if (remJf !== Infinity && remJf < needJf) break;
    if (s.hasItem && remItem !== Infinity && remItem < needItem) break;
    if (remJf !== Infinity) { remJf -= needJf; totalJf += needJf; }
    if (s.hasItem && remItem !== Infinity) { remItem -= needItem; totalItem += needItem; }
    lv = nextLv; steps++;
  }
  return { level: lv, totalJf: Math.round(totalJf), totalItem: Math.round(totalItem), steps, remainingJf: Math.round(remJf * 100) / 100, remainingItem: Math.round(remItem * 100) / 100 };
}

/** 功能二：根据目标计算所需材料 */
export async function calcForTarget(slot: string, startLv: number, targetLv: number) {
  await ensureData();
  const s = getSlot(slot);
  const cum = CUM[s.key];
  const startE = cum[startLv], targetE = cum[targetLv];
  if (!startE || !targetE) return { totalJf: 0, totalItem: 0 };
  return {
    totalJf: Math.round(targetE.cumJf - startE.cumJf),
    totalItem: s.hasItem ? Math.round(targetE.cumItem - startE.cumItem) : 0,
  };
}
