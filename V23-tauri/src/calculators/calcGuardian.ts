/**
 * 守护神养成计算引擎 - 移植自 calc_guardian.py
 * 基于真实出货概率 + 幸运值保底 + 次数保底
 */

let _data: any = null;
let _loadPromise: Promise<void> | null = null;
let EXP_MAP: Record<string,Record<string,number>> = {};

async function ensureData() {
  if (_data) return;
  if (_loadPromise) { await _loadPromise; return; }
  _loadPromise = (async () => {
    const r = await fetch("/game_data/guardian_data.json");
    _data = await r.json();
    EXP_MAP = calcExpMap();
  })();
  await _loadPromise;
}

function calcExpMap(): Record<string,Record<string,number>> {
  const result: Record<string,Record<string,number>> = {};
  const remnantPerDraw = _data.guardian_config.remnant_per_draw;
  for (const group of _data.groups) {
    const gname = group.name;
    const totalWeight = group.guardians.reduce((s:number,g:any) => s + g.weight, 0);
    const pityTrigger = group.pity_trigger;
    const pityGuardians: string[] = group.pity_guardians ?? [];
    const pityCount = pityGuardians.length;
    const countPity = group.count_pity;
    const countPityTarget = group.count_pity_target;
    const gmap: Record<string,number> = {};

    for (const g of group.guardians) {
      let exp = (g.weight / totalWeight) * remnantPerDraw;
      if (pityGuardians.includes(g.name) && pityCount > 0) exp += (1/pityCount) * remnantPerDraw / pityTrigger;
      if (countPity && countPityTarget === g.name) exp += remnantPerDraw / countPity;
      gmap[g.name] = exp;
    }
    result[gname] = gmap;
  }
  return result;
}

const STAR_CUM: Record<number,number> = {0:0,1:20,2:60,3:140,4:300,5:300};

export async function getGroupNames(): Promise<string[]> {
  await ensureData();
  return _data.groups.map((g:any) => g.name);
}

export async function getGroupGuardians(groupName:string): Promise<any[]> {
  await ensureData();
  return _data.groups.find((g:any) => g.name === groupName)?.guardians ?? [];
}

export async function getGroupTicket(groupName:string): Promise<string> {
  await ensureData();
  return _data.groups.find((g:any) => g.name === groupName)?.ticket ?? "请神符";
}

export async function calcSimple(groupName:string, curAvg:number, tgtAvg:number, heldEssence:number = 0) {
  await ensureData();
  if (curAvg < 0 || curAvg > 5 || tgtAvg < 0 || tgtAvg > 5) return {error:"平均星级范围 0.0 ~ 5.0"};
  if (tgtAvg < curAvg) return {error:"目标不能低于当前"};

  const group = _data.groups.find((g:any) => g.name === groupName);
  if (!group) return {error:`未找到组: ${groupName}`};
  const n = group.guardians.length;
  const gmap = EXP_MAP[groupName] ?? {};
  const ticket = group.ticket;

  if (tgtAvg === curAvg) return {error:null, groupName, totalTickets:0, ticket, details:[]};

  // 最常见方案：按期望残念速率比例加权分配
  const totalExp = Object.values(gmap).reduce((s,v) => s + v, 0);
  const curTotal = Math.round(curAvg * n);
  const tgtTotal = Math.round(tgtAvg * n);

  const curDist = totalExp > 0
    ? group.guardians.map((g:any) => Math.min(5, Math.max(0, Math.round(curTotal * (gmap[g.name]??0) / totalExp))))
    : new Array(n).fill(Math.round(curAvg));
  const tgtDist = totalExp > 0
    ? group.guardians.map((g:any) => Math.min(5, Math.max(0, Math.round(tgtTotal * (gmap[g.name]??0) / totalExp))))
    : new Array(n).fill(Math.round(tgtAvg));

  // 约束
  for (let i = 0; i < n; i++) if (tgtDist[i] < curDist[i]) tgtDist[i] = curDist[i];

  let maxTickets = 0;
  const details = group.guardians.map((g:any, i:number) => {
    const need = STAR_CUM[tgtDist[i]] - STAR_CUM[curDist[i]];
    const gap = Math.max(0, need);
    const exp = gmap[g.name] ?? 0;
    const tickets = exp > 0 ? Math.ceil(gap / exp) : 0;
    if (tickets > maxTickets) maxTickets = tickets;
    return { name:g.name, quality:g.quality, curStar:curDist[i], tgtStar:tgtDist[i], need, gap, tickets, expPerTicket:Math.round(exp*10000)/10000 };
  });

  return { error:null, groupName, totalTickets:maxTickets, ticket, details, curDist, tgtDist };
}

export async function calcPrecise(groupName:string, curStars:number[], tgtStars:number[], heldEssence:number = 0) {
  await ensureData();
  const group = _data.groups.find((g:any) => g.name === groupName);
  if (!group) return {error:`未找到组: ${groupName}`};
  const gmap = EXP_MAP[groupName] ?? {};
  const ticket = group.ticket;

  let maxTickets = 0;
  const details = group.guardians.map((g:any, i:number) => {
    const need = STAR_CUM[tgtStars[i]] - STAR_CUM[curStars[i]];
    const gap = Math.max(0, need);
    const exp = gmap[g.name] ?? 0;
    const tickets = exp > 0 ? Math.ceil(gap / exp) : 0;
    if (tickets > maxTickets) maxTickets = tickets;
    return { name:g.name, quality:g.quality, curStar:curStars[i], tgtStar:tgtStars[i], need, gap, tickets, expPerTicket:Math.round(exp*10000)/10000 };
  });

  return { error:null, groupName, totalTickets:maxTickets, ticket, details };
}
