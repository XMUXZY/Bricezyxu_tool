const cache: Record<string, any> = {};

export async function loadGameData<T = any>(filename: string): Promise<T> {
  if (cache[filename]) return cache[filename] as T;
  const resp = await fetch(`/game_data/${filename}`);
  if (!resp.ok) throw new Error(`Failed to load ${filename}: ${resp.status}`);
  const data = await resp.json();
  cache[filename] = data;
  return data as T;
}

export function formatNumber(num: number): string {
  if (num === 0) return "0";
  if (num >= 1000000) return num.toLocaleString("en-US", { maximumFractionDigits: 0 });
  if (num >= 10000) return num.toLocaleString("en-US", { maximumFractionDigits: 1 });
  if (num >= 100) return num.toLocaleString("en-US", { maximumFractionDigits: 2 });
  if (num >= 10) return num.toLocaleString("en-US", { maximumFractionDigits: 3 });
  return num.toLocaleString("en-US", { maximumFractionDigits: 4 });
}

export function parseIntSafe(val: string, defaultVal: number): number {
  const v = parseInt((val || "").trim() || String(defaultVal), 10);
  return isNaN(v) ? defaultVal : v;
}

export function parseFloatOrInf(val: string): number {
  const v = (val || "").trim();
  if (!v) return Infinity;
  const n = parseFloat(v);
  return isNaN(n) ? Infinity : n;
}
