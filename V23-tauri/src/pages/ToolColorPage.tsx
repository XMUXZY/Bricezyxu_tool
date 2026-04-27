import { useState, useRef, useEffect } from "react";

const PRESET_COLORS = [
  "#f2e37c","#a6872c","#ffcf2f","#c0aa85","#f2e2c7","#524c42","#463823","#bdf3fe",
  "#c6febd","#ffe4d8","#c67b79","#8bb6c4","#d17702","#05c30e","#007fff","#c30505",
  "#05b8c3","#c305aa","#7e05c3","#d0c9d2","#831717",
];

const EXAMPLES: Record<string,string> = {
  "游戏道具": "<color=#d17702>传说级装备</color>、<color=#7e05c3>史诗级材料</color>、<color=#007fff>稀有级消耗品</color>",
  "系统公告": "系统公告：<color=#c30505>紧急维护通知</color>，服务器将于<color=#ffcf2f>今晚22:00-24:00</color>进行维护。",
  "多彩文本": "<color=#c30505>红色</color>、<color=#05c30e>绿色</color>、<color=#007fff>蓝色</color>、<color=#7e05c3>紫色</color>",
};

function validateColor(raw: string): string | null {
  const s = raw.trim().toLowerCase();
  if (/^#[0-9a-f]{6}$/.test(s) && PRESET_COLORS.includes(s)) return s;
  const m3 = s.match(/^#([0-9a-f])([0-9a-f])([0-9a-f])$/);
  if (m3) {
    const full = `#${m3[1]+m3[1]}${m3[2]+m3[2]}${m3[3]+m3[3]}`;
    if (PRESET_COLORS.includes(full)) return full;
  }
  return null;
}

type Segment = { text: string; color: string | null };

function parseColorTags(text: string): { segments: Segment[]; colors: string[]; tagCount: number } {
  const pattern = /<color=(#[0-9a-fA-F]{3,6}|[a-zA-Z]+)>(.*?)<\/color>/gs;
  const segments: Segment[] = [];
  const colorSet = new Set<string>();
  let tagCount = 0;
  let lastEnd = 0;
  let match;
  while ((match = pattern.exec(text)) !== null) {
    if (match.index > lastEnd) segments.push({ text: text.slice(lastEnd, match.index), color: null });
    const validated = validateColor(match[1]);
    tagCount++;
    if (validated) { colorSet.add(validated); segments.push({ text: match[2], color: validated }); }
    else segments.push({ text: match[2], color: "#ff0000" });
    lastEnd = match.index + match[0].length;
  }
  if (lastEnd < text.length) segments.push({ text: text.slice(lastEnd), color: null });
  return { segments, colors: [...colorSet], tagCount };
}

export default function ToolColorPage() {
  const [input, setInput] = useState("");
  const [currentColor, setCurrentColor] = useState("#c30505");
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const parsed = parseColorTags(input);

  const insertColorTag = () => {
    const ta = textareaRef.current;
    if (!ta) return;
    const start = ta.selectionStart;
    const end = ta.selectionEnd;
    const selected = input.slice(start, end);
    const tag = `<color=${currentColor}>${selected || "文字"}</color>`;
    const newVal = input.slice(0, start) + tag + input.slice(end);
    setInput(newVal);
    setTimeout(() => {
      ta.focus();
      const cursorPos = start + `<color=${currentColor}>`.length;
      const cursorEnd = cursorPos + (selected || "文字").length;
      ta.setSelectionRange(cursorPos, cursorEnd);
    }, 0);
  };

  return (
    <div className="page-container">
      <div style={{ display: "flex", alignItems: "center", gap: 15, marginBottom: 10 }}>
        <h1 className="page-title">🎨 文字颜色解析工具</h1>
        <span style={{ fontSize: 12, color: "#888" }}>输入含颜色代码的文本，实时预览</span>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
        {/* 左侧输入 */}
        <div className="card">
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
            <span style={{ fontWeight: "bold", color: "#fff" }}>📝 输入文本</span>
            <span style={{ fontSize: 12, color: "#888" }}>字数: {input.length}</span>
          </div>
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            style={{ width: "100%", height: 200, background: "#0f0f1a", color: "#e0e0e0", border: "1px solid #2a2a4a", borderRadius: 8, padding: 10, fontSize: 13, resize: "vertical", fontFamily: "inherit" }}
            placeholder="输入含 <color=#ff0000>颜色标签</color> 的文本..."
          />
          <div style={{ display: "flex", gap: 6, marginTop: 8, flexWrap: "wrap", alignItems: "center" }}>
            <span style={{ fontSize: 12, color: "#888", lineHeight: "28px" }}>选色：</span>
            {PRESET_COLORS.map((c) => (
              <div key={c} onClick={() => setCurrentColor(c)} style={{ width: 20, height: 20, borderRadius: 4, background: c, cursor: "pointer", border: c === currentColor ? "2px solid #fff" : "1px solid #555" }} />
            ))}
          </div>
          <div style={{ display: "flex", gap: 8, marginTop: 8, alignItems: "center" }}>
            <div onClick={insertColorTag} style={{ display: "inline-flex", alignItems: "center", gap: 6, padding: "6px 14px", borderRadius: 6, background: currentColor, color: "#fff", cursor: "pointer", fontWeight: "bold", fontSize: 13, textShadow: "0 1px 2px rgba(0,0,0,0.5)" }} title="选中文字后点击，或直接点击插入">
              🎨 插入颜色标签
            </div>
            <span style={{ fontSize: 11, color: "#666" }}>先选中文字再点击，或直接插入占位文字</span>
          </div>
          <div style={{ display: "flex", gap: 6, marginTop: 8 }}>
            <span style={{ fontSize: 12, color: "#888", lineHeight: "26px" }}>示例：</span>
            {Object.keys(EXAMPLES).map((name) => (
              <button key={name} className="btn-secondary" onClick={() => setInput(EXAMPLES[name])}>{name}</button>
            ))}
          </div>
        </div>

        {/* 右侧预览 */}
        <div className="card">
          <div style={{ fontWeight: "bold", color: "#fff", marginBottom: 8 }}>👁️ 游戏邮件预览</div>
          <div style={{ background: "#2e2218", border: "2px solid #5a4530", borderRadius: 10, padding: 12, minHeight: 200 }}>
            <div style={{ background: "#3c2d1e", textAlign: "center", padding: 10, fontWeight: "bold", color: "#e8c84a", fontSize: 16, borderRadius: "8px 8px 0 0", marginBottom: 8 }}>
              邮件预览
            </div>
            <div style={{ fontFamily: "Microsoft YaHei UI", fontSize: 12, lineHeight: 1.8, color: "#d4d0c8", userSelect: "text" }}>
              {parsed.segments.length > 0 ? parsed.segments.map((seg, i) => (
                <span key={i} style={seg.color ? { color: seg.color } : undefined}>{seg.text}</span>
              )) : <span style={{ color: "#666" }}>输入文本后此处将显示带颜色的预览…</span>}
            </div>
          </div>

          <div style={{ display: "flex", gap: 16, marginTop: 12 }}>
            <div style={{ background: "#0f3460", borderRadius: 8, padding: "8px 16px", textAlign: "center", flex: 1 }}>
              <div style={{ fontSize: 20, fontWeight: "bold", color: "#fff" }}>{parsed.colors.length}</div>
              <div style={{ fontSize: 10, color: "#aaa" }}>颜色数量</div>
            </div>
            <div style={{ background: "#1a5c3a", borderRadius: 8, padding: "8px 16px", textAlign: "center", flex: 1 }}>
              <div style={{ fontSize: 20, fontWeight: "bold", color: "#fff" }}>{parsed.tagCount}</div>
              <div style={{ fontSize: 10, color: "#aaa" }}>标签数量</div>
            </div>
            <div style={{ background: "#4a2060", borderRadius: 8, padding: "8px 16px", textAlign: "center", flex: 1 }}>
              <div style={{ fontSize: 20, fontWeight: "bold", color: "#fff" }}>{input.length}</div>
              <div style={{ fontSize: 10, color: "#aaa" }}>字符数</div>
            </div>
          </div>

          {parsed.colors.length > 0 && (
            <div style={{ marginTop: 10, display: "flex", gap: 8, flexWrap: "wrap" }}>
              <span style={{ fontSize: 12, fontWeight: "bold", color: "#fff" }}>🎨 已解析颜色：</span>
              {parsed.colors.map((c) => (
                <span key={c} style={{ display: "inline-flex", alignItems: "center", gap: 4 }}>
                  <span style={{ width: 14, height: 14, borderRadius: 7, background: c, display: "inline-block", border: "1px solid #555" }} />
                  <span style={{ fontFamily: "Consolas", fontSize: 11, color: "#888" }}>{c}</span>
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
