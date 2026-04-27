interface ResultBoxProps {
  content: string;
}

export default function ResultBox({ content }: ResultBoxProps) {
  return <div className="result-box">{content || "等待计算…"}</div>;
}
