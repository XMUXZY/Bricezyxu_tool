/**
 * 装备重铸计算引擎
 * 移植自 Python calculators/calc_c.py
 */

interface ReforgeRow {
  level: number; stage: number; materialA: string;
  materialARequired: number; materialBRequired: number;
}

export const REFORGE_DATA: ReforgeRow[] = [
  {level:0,stage:0,materialA:"不灭离炎",materialARequired:2,materialBRequired:1},
  {level:1,stage:0,materialA:"不灭离炎",materialARequired:1,materialBRequired:0},{level:1,stage:1,materialA:"不灭离炎",materialARequired:1,materialBRequired:0},{level:1,stage:2,materialA:"不灭离炎",materialARequired:1,materialBRequired:0},{level:1,stage:3,materialA:"不灭离炎",materialARequired:1,materialBRequired:0},{level:1,stage:4,materialA:"不灭离炎",materialARequired:1,materialBRequired:0},{level:1,stage:5,materialA:"不灭离炎",materialARequired:1,materialBRequired:0},
  {level:2,stage:0,materialA:"不灭离炎",materialARequired:1,materialBRequired:0},{level:2,stage:1,materialA:"不灭离炎",materialARequired:1,materialBRequired:0},{level:2,stage:2,materialA:"不灭离炎",materialARequired:1,materialBRequired:0},{level:2,stage:3,materialA:"不灭离炎",materialARequired:1,materialBRequired:0},{level:2,stage:4,materialA:"不灭离炎",materialARequired:1,materialBRequired:0},{level:2,stage:5,materialA:"不灭离炎",materialARequired:1,materialBRequired:0},
  {level:3,stage:0,materialA:"不灭离炎",materialARequired:1,materialBRequired:0},{level:3,stage:1,materialA:"不灭离炎",materialARequired:1,materialBRequired:0},{level:3,stage:2,materialA:"不灭离炎",materialARequired:1,materialBRequired:0},{level:3,stage:3,materialA:"不灭离炎",materialARequired:1,materialBRequired:0},{level:3,stage:4,materialA:"不灭离炎",materialARequired:1,materialBRequired:0},{level:3,stage:5,materialA:"不灭离炎",materialARequired:1,materialBRequired:0},
  {level:4,stage:0,materialA:"不灭离炎",materialARequired:2,materialBRequired:1},{level:4,stage:1,materialA:"不灭离炎",materialARequired:2,materialBRequired:1},{level:4,stage:2,materialA:"不灭离炎",materialARequired:2,materialBRequired:1},{level:4,stage:3,materialA:"不灭离炎",materialARequired:2,materialBRequired:1},{level:4,stage:4,materialA:"不灭离炎",materialARequired:2,materialBRequired:1},{level:4,stage:5,materialA:"不灭离炎",materialARequired:2,materialBRequired:1},
  {level:5,stage:0,materialA:"不灭离炎",materialARequired:2,materialBRequired:1},{level:5,stage:1,materialA:"不灭离炎",materialARequired:2,materialBRequired:1},{level:5,stage:2,materialA:"不灭离炎",materialARequired:2,materialBRequired:1},{level:5,stage:3,materialA:"不灭离炎",materialARequired:2,materialBRequired:1},{level:5,stage:4,materialA:"不灭离炎",materialARequired:2,materialBRequired:1},{level:5,stage:5,materialA:"不灭离炎",materialARequired:2,materialBRequired:1},
  {level:6,stage:0,materialA:"青璃焰光",materialARequired:2,materialBRequired:1},{level:6,stage:1,materialA:"青璃焰光",materialARequired:2,materialBRequired:1},{level:6,stage:2,materialA:"青璃焰光",materialARequired:2,materialBRequired:1},{level:6,stage:3,materialA:"青璃焰光",materialARequired:2,materialBRequired:1},{level:6,stage:4,materialA:"青璃焰光",materialARequired:2,materialBRequired:1},{level:6,stage:5,materialA:"青璃焰光",materialARequired:2,materialBRequired:1},
  {level:7,stage:0,materialA:"青璃焰光",materialARequired:2,materialBRequired:1},{level:7,stage:1,materialA:"青璃焰光",materialARequired:2,materialBRequired:1},{level:7,stage:2,materialA:"青璃焰光",materialARequired:2,materialBRequired:1},{level:7,stage:3,materialA:"青璃焰光",materialARequired:2,materialBRequired:1},{level:7,stage:4,materialA:"青璃焰光",materialARequired:2,materialBRequired:1},{level:7,stage:5,materialA:"青璃焰光",materialARequired:2,materialBRequired:1},
  {level:8,stage:0,materialA:"青璃焰光",materialARequired:2.10526,materialBRequired:1.05263},{level:8,stage:1,materialA:"青璃焰光",materialARequired:2.10526,materialBRequired:1.05263},{level:8,stage:2,materialA:"青璃焰光",materialARequired:3.15789,materialBRequired:1.05263},{level:8,stage:3,materialA:"青璃焰光",materialARequired:3.15789,materialBRequired:1.05263},{level:8,stage:4,materialA:"青璃焰光",materialARequired:4.21053,materialBRequired:1.05263},{level:8,stage:5,materialA:"青璃焰光",materialARequired:4.21053,materialBRequired:1.05263},
  {level:9,stage:0,materialA:"青璃焰光",materialARequired:2.35294,materialBRequired:1.17647},{level:9,stage:1,materialA:"青璃焰光",materialARequired:2.35294,materialBRequired:1.17647},{level:9,stage:2,materialA:"青璃焰光",materialARequired:3.52941,materialBRequired:1.17647},{level:9,stage:3,materialA:"青璃焰光",materialARequired:3.52941,materialBRequired:1.17647},{level:9,stage:4,materialA:"青璃焰光",materialARequired:4.70588,materialBRequired:1.17647},{level:9,stage:5,materialA:"青璃焰光",materialARequired:4.70588,materialBRequired:1.17647},
  {level:10,stage:0,materialA:"青璃焰光",materialARequired:5.33333,materialBRequired:1.33333},{level:10,stage:1,materialA:"青璃焰光",materialARequired:5.33333,materialBRequired:1.33333},{level:10,stage:2,materialA:"青璃焰光",materialARequired:6.66667,materialBRequired:1.33333},{level:10,stage:3,materialA:"青璃焰光",materialARequired:6.66667,materialBRequired:1.33333},{level:10,stage:4,materialA:"青璃焰光",materialARequired:8,materialBRequired:1.33333},{level:10,stage:5,materialA:"青璃焰光",materialARequired:8,materialBRequired:1.33333},
  {level:11,stage:0,materialA:"冥雷寒铁",materialARequired:12,materialBRequired:2.66667},{level:11,stage:1,materialA:"冥雷寒铁",materialARequired:12,materialBRequired:2.66667},{level:11,stage:2,materialA:"冥雷寒铁",materialARequired:16,materialBRequired:2.66667},{level:11,stage:3,materialA:"冥雷寒铁",materialARequired:16,materialBRequired:2.66667},{level:11,stage:4,materialA:"冥雷寒铁",materialARequired:20,materialBRequired:2.66667},{level:11,stage:5,materialA:"冥雷寒铁",materialARequired:20,materialBRequired:2.66667},
  {level:12,stage:0,materialA:"冥雷寒铁",materialARequired:12.85714,materialBRequired:2.85714},{level:12,stage:1,materialA:"冥雷寒铁",materialARequired:12.85714,materialBRequired:2.85714},{level:12,stage:2,materialA:"冥雷寒铁",materialARequired:17.14286,materialBRequired:2.85714},{level:12,stage:3,materialA:"冥雷寒铁",materialARequired:17.14286,materialBRequired:2.85714},{level:12,stage:4,materialA:"冥雷寒铁",materialARequired:21.42857,materialBRequired:2.85714},{level:12,stage:5,materialA:"冥雷寒铁",materialARequired:21.42857,materialBRequired:2.85714},
  {level:13,stage:0,materialA:"冥雷寒铁",materialARequired:12.85714,materialBRequired:2.85714},{level:13,stage:1,materialA:"冥雷寒铁",materialARequired:12.85714,materialBRequired:2.85714},{level:13,stage:2,materialA:"冥雷寒铁",materialARequired:17.14286,materialBRequired:2.85714},{level:13,stage:3,materialA:"冥雷寒铁",materialARequired:17.14286,materialBRequired:2.85714},{level:13,stage:4,materialA:"冥雷寒铁",materialARequired:21.42857,materialBRequired:2.85714},{level:13,stage:5,materialA:"冥雷寒铁",materialARequired:21.42857,materialBRequired:2.85714},
  {level:14,stage:0,materialA:"冥雷寒铁",materialARequired:18.33333,materialBRequired:5},{level:14,stage:1,materialA:"冥雷寒铁",materialARequired:18.33333,materialBRequired:5},{level:14,stage:2,materialA:"冥雷寒铁",materialARequired:23.33333,materialBRequired:5},{level:14,stage:3,materialA:"冥雷寒铁",materialARequired:23.33333,materialBRequired:5},{level:14,stage:4,materialA:"冥雷寒铁",materialARequired:28.33333,materialBRequired:5},{level:14,stage:5,materialA:"冥雷寒铁",materialARequired:28.33333,materialBRequired:5},
  {level:15,stage:0,materialA:"冥雷寒铁",materialARequired:18.33333,materialBRequired:5},{level:15,stage:1,materialA:"冥雷寒铁",materialARequired:18.33333,materialBRequired:5},{level:15,stage:2,materialA:"冥雷寒铁",materialARequired:23.33333,materialBRequired:5},{level:15,stage:3,materialA:"冥雷寒铁",materialARequired:23.33333,materialBRequired:5},{level:15,stage:4,materialA:"冥雷寒铁",materialARequired:28.33333,materialBRequired:5},{level:15,stage:5,materialA:"冥雷寒铁",materialARequired:28.33333,materialBRequired:5},
  {level:16,stage:0,materialA:"辉光玄铁",materialARequired:20,materialBRequired:5.45455},{level:16,stage:1,materialA:"辉光玄铁",materialARequired:20,materialBRequired:5.45455},{level:16,stage:2,materialA:"辉光玄铁",materialARequired:25.45455,materialBRequired:5.45455},{level:16,stage:3,materialA:"辉光玄铁",materialARequired:25.45455,materialBRequired:5.45455},{level:16,stage:4,materialA:"辉光玄铁",materialARequired:30.90909,materialBRequired:5.45455},{level:16,stage:5,materialA:"辉光玄铁",materialARequired:30.90909,materialBRequired:5.45455},
  {level:17,stage:0,materialA:"辉光玄铁",materialARequired:26,materialBRequired:10},{level:17,stage:1,materialA:"辉光玄铁",materialARequired:26,materialBRequired:10},{level:17,stage:2,materialA:"辉光玄铁",materialARequired:32,materialBRequired:10},{level:17,stage:3,materialA:"辉光玄铁",materialARequired:32,materialBRequired:10},{level:17,stage:4,materialA:"辉光玄铁",materialARequired:38,materialBRequired:10},{level:17,stage:5,materialA:"辉光玄铁",materialARequired:38,materialBRequired:10},
  {level:18,stage:0,materialA:"辉光玄铁",materialARequired:26,materialBRequired:10},{level:18,stage:1,materialA:"辉光玄铁",materialARequired:26,materialBRequired:10},{level:18,stage:2,materialA:"辉光玄铁",materialARequired:32,materialBRequired:10},{level:18,stage:3,materialA:"辉光玄铁",materialARequired:32,materialBRequired:10},{level:18,stage:4,materialA:"辉光玄铁",materialARequired:38,materialBRequired:10},{level:18,stage:5,materialA:"辉光玄铁",materialARequired:38,materialBRequired:10},
  {level:19,stage:0,materialA:"辉光玄铁",materialARequired:28.88889,materialBRequired:11.11111},{level:19,stage:1,materialA:"辉光玄铁",materialARequired:28.88889,materialBRequired:11.11111},{level:19,stage:2,materialA:"辉光玄铁",materialARequired:35.55556,materialBRequired:11.11111},{level:19,stage:3,materialA:"辉光玄铁",materialARequired:35.55556,materialBRequired:11.11111},{level:19,stage:4,materialA:"辉光玄铁",materialARequired:42.22222,materialBRequired:11.11111},{level:19,stage:5,materialA:"辉光玄铁",materialARequired:42.22222,materialBRequired:11.11111},
  {level:20,stage:0,materialA:"辉光玄铁",materialARequired:35.71429,materialBRequired:19.04762},{level:20,stage:1,materialA:"辉光玄铁",materialARequired:35.71429,materialBRequired:19.04762},{level:20,stage:2,materialA:"辉光玄铁",materialARequired:42.85714,materialBRequired:19.04762},{level:20,stage:3,materialA:"辉光玄铁",materialARequired:42.85714,materialBRequired:19.04762},{level:20,stage:4,materialA:"辉光玄铁",materialARequired:50,materialBRequired:19.04762},{level:20,stage:5,materialA:"辉光玄铁",materialARequired:50,materialBRequired:19.04762},
  {level:21,stage:0,materialA:"坠影紫晶",materialARequired:37.5,materialBRequired:20},{level:21,stage:1,materialA:"坠影紫晶",materialARequired:37.5,materialBRequired:20},{level:21,stage:2,materialA:"坠影紫晶",materialARequired:45,materialBRequired:20},{level:21,stage:3,materialA:"坠影紫晶",materialARequired:45,materialBRequired:20},{level:21,stage:4,materialA:"坠影紫晶",materialARequired:52.5,materialBRequired:20},{level:21,stage:5,materialA:"坠影紫晶",materialARequired:52.5,materialBRequired:20},
  {level:22,stage:0,materialA:"坠影紫晶",materialARequired:39.47368,materialBRequired:21.05263},{level:22,stage:1,materialA:"坠影紫晶",materialARequired:39.47368,materialBRequired:21.05263},{level:22,stage:2,materialA:"坠影紫晶",materialARequired:47.36842,materialBRequired:21.05263},{level:22,stage:3,materialA:"坠影紫晶",materialARequired:47.36842,materialBRequired:21.05263},{level:22,stage:4,materialA:"坠影紫晶",materialARequired:55.26316,materialBRequired:21.05263},{level:22,stage:5,materialA:"坠影紫晶",materialARequired:55.26316,materialBRequired:21.05263},
  {level:23,stage:0,materialA:"坠影紫晶",materialARequired:44.44444,materialBRequired:27.77778},{level:23,stage:1,materialA:"坠影紫晶",materialARequired:44.44444,materialBRequired:27.77778},{level:23,stage:2,materialA:"坠影紫晶",materialARequired:55.55556,materialBRequired:27.77778},{level:23,stage:3,materialA:"坠影紫晶",materialARequired:55.55556,materialBRequired:27.77778},{level:23,stage:4,materialA:"坠影紫晶",materialARequired:66.66667,materialBRequired:27.77778},{level:23,stage:5,materialA:"坠影紫晶",materialARequired:66.66667,materialBRequired:27.77778},
  {level:24,stage:0,materialA:"坠影紫晶",materialARequired:47.05882,materialBRequired:29.41176},{level:24,stage:1,materialA:"坠影紫晶",materialARequired:47.05882,materialBRequired:29.41176},{level:24,stage:2,materialA:"坠影紫晶",materialARequired:58.82353,materialBRequired:29.41176},{level:24,stage:3,materialA:"坠影紫晶",materialARequired:58.82353,materialBRequired:29.41176},{level:24,stage:4,materialA:"坠影紫晶",materialARequired:70.58824,materialBRequired:29.41176},{level:24,stage:5,materialA:"坠影紫晶",materialARequired:70.58824,materialBRequired:29.41176},
  {level:25,stage:0,materialA:"坠影紫晶",materialARequired:48.48485,materialBRequired:30.30303},{level:25,stage:1,materialA:"坠影紫晶",materialARequired:51.6129,materialBRequired:32.25806},{level:25,stage:2,materialA:"坠影紫晶",materialARequired:68.96552,materialBRequired:34.48276},{level:25,stage:3,materialA:"坠影紫晶",materialARequired:74.07407,materialBRequired:37.03704},{level:25,stage:4,materialA:"坠影紫晶",materialARequired:92.30769,materialBRequired:38.46154},{level:25,stage:5,materialA:"坠影紫晶",materialARequired:96,materialBRequired:40},
  {level:26,stage:0,materialA:"绯云玄晶",materialARequired:72,materialBRequired:48},{level:26,stage:1,materialA:"绯云玄晶",materialARequired:72,materialBRequired:48},{level:26,stage:2,materialA:"绯云玄晶",materialARequired:88,materialBRequired:48},{level:26,stage:3,materialA:"绯云玄晶",materialARequired:88,materialBRequired:48},{level:26,stage:4,materialA:"绯云玄晶",materialARequired:104,materialBRequired:48},{level:26,stage:5,materialA:"绯云玄晶",materialARequired:104,materialBRequired:48},
  {level:27,stage:0,materialA:"绯云玄晶",materialARequired:72,materialBRequired:48},{level:27,stage:1,materialA:"绯云玄晶",materialARequired:72,materialBRequired:48},{level:27,stage:2,materialA:"绯云玄晶",materialARequired:88,materialBRequired:48},{level:27,stage:3,materialA:"绯云玄晶",materialARequired:88,materialBRequired:48},{level:27,stage:4,materialA:"绯云玄晶",materialARequired:104,materialBRequired:48},{level:27,stage:5,materialA:"绯云玄晶",materialARequired:104,materialBRequired:48},
  {level:28,stage:0,materialA:"绯云玄晶",materialARequired:72,materialBRequired:48},{level:28,stage:1,materialA:"绯云玄晶",materialARequired:72,materialBRequired:48},{level:28,stage:2,materialA:"绯云玄晶",materialARequired:88,materialBRequired:48},{level:28,stage:3,materialA:"绯云玄晶",materialARequired:88,materialBRequired:48},{level:28,stage:4,materialA:"绯云玄晶",materialARequired:104,materialBRequired:48},{level:28,stage:5,materialA:"绯云玄晶",materialARequired:104,materialBRequired:48},
  {level:29,stage:0,materialA:"绯云玄晶",materialARequired:88,materialBRequired:60},{level:29,stage:1,materialA:"绯云玄晶",materialARequired:88,materialBRequired:60},{level:29,stage:2,materialA:"绯云玄晶",materialARequired:100,materialBRequired:60},{level:29,stage:3,materialA:"绯云玄晶",materialARequired:100,materialBRequired:60},{level:29,stage:4,materialA:"绯云玄晶",materialARequired:112,materialBRequired:60},{level:29,stage:5,materialA:"绯云玄晶",materialARequired:112,materialBRequired:60},
  {level:30,stage:0,materialA:"绯云玄晶",materialARequired:88,materialBRequired:60},{level:30,stage:1,materialA:"绯云玄晶",materialARequired:88,materialBRequired:60},{level:30,stage:2,materialA:"绯云玄晶",materialARequired:100,materialBRequired:60},{level:30,stage:3,materialA:"绯云玄晶",materialARequired:100,materialBRequired:60},{level:30,stage:4,materialA:"绯云玄晶",materialARequired:112,materialBRequired:60},{level:30,stage:5,materialA:"绯云玄晶",materialARequired:112,materialBRequired:60},
];

export const MATERIAL_CONVERSION: Record<string,number> = {
  "不灭离炎":1,"青璃焰光":3,"冥雷寒铁":9,"辉光玄铁":27
};
export const MATERIAL_B_NAME = "忘川冥息";
export const EQUIPMENT_COUNT = 11;

const REFORGE_INDEX = new Map<string,number>();
REFORGE_DATA.forEach((d,i) => REFORGE_INDEX.set(`${d.level}_${d.stage}`, i));

function findDataIndex(level: number, stage: number): number {
  return REFORGE_INDEX.get(`${level}_${stage}`) ?? -1;
}

export function formatNum(num: number): string {
  if (num >= 10000) return num.toLocaleString("en-US",{maximumFractionDigits:1});
  if (num >= 100) return num.toLocaleString("en-US",{maximumFractionDigits:2});
  if (num >= 1) return num.toLocaleString("en-US",{maximumFractionDigits:3});
  return num.toFixed(4);
}

export function calcReforgeByMaterials(initLevel:number, initStage:number, matType:string, remainingA:number, remainingB:number) {
  const startIndex = findDataIndex(initLevel, initStage);
  if (startIndex < 0) return {error:"无效的初始等级和阶段"};

  let currentLevel = initLevel, currentStage = initStage;
  let totalUsedA = 0, totalUsedB = 0;

  for (let i = startIndex; i < REFORGE_DATA.length; i++) {
    const sd = REFORGE_DATA[i];
    let requiredA = sd.materialARequired * EQUIPMENT_COUNT;
    const requiredB = sd.materialBRequired * EQUIPMENT_COUNT;

    if (sd.materialA !== matType) {
      if (MATERIAL_CONVERSION[sd.materialA] && MATERIAL_CONVERSION[matType]) {
        requiredA = requiredA * MATERIAL_CONVERSION[sd.materialA] / MATERIAL_CONVERSION[matType];
      } else break;
    }

    if (remainingA >= requiredA && remainingB >= requiredB) {
      if (remainingA !== Infinity) remainingA -= requiredA;
      if (remainingB !== Infinity) remainingB -= requiredB;
      totalUsedA += requiredA;
      totalUsedB += requiredB;
      if (sd.stage === 5) { currentLevel = sd.level + 1; currentStage = 0; }
      else { currentLevel = sd.level; currentStage = sd.stage + 1; }
    } else break;
  }

  return { error:null, currentLevel, currentStage, totalUsedA, totalUsedB, remainingA, remainingB };
}

export function calcMaterialsForTarget(startLevel:number, startStage:number, targetLevel:number, targetStage:number, targetMatType:string) {
  const startIdx = findDataIndex(startLevel, startStage);
  const endIdx = findDataIndex(targetLevel, targetStage);
  if (startIdx < 0) return {error:"无效的初始等级和阶段"};
  if (endIdx < 0) return {error:"无效的目标等级和阶段"};
  if (startIdx >= endIdx) return {error:"目标等级/阶段必须大于初始等级/阶段"};

  const totalMaterials: Record<string,number> = {"不灭离炎":0,"青璃焰光":0,"冥雷寒铁":0,"辉光玄铁":0,"坠影紫晶":0,"绯云玄晶":0,[MATERIAL_B_NAME]:0};

  for (let i = startIdx; i < endIdx; i++) {
    const sd = REFORGE_DATA[i];
    totalMaterials[sd.materialA] += sd.materialARequired * EQUIPMENT_COUNT;
    totalMaterials[MATERIAL_B_NAME] += sd.materialBRequired * EQUIPMENT_COUNT;
  }

  let convertedTotal = 0;
  for (const [name, amount] of Object.entries(totalMaterials)) {
    if (name === MATERIAL_B_NAME || amount <= 0) continue;
    if (MATERIAL_CONVERSION[name] && MATERIAL_CONVERSION[targetMatType]) {
      convertedTotal += amount * MATERIAL_CONVERSION[name] / MATERIAL_CONVERSION[targetMatType];
    } else if (name === targetMatType) convertedTotal += amount;
  }

  return { error:null, totalMaterials, convertedTotal, stagesCount: endIdx - startIdx };
}
