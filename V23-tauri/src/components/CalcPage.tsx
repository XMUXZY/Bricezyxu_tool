import { useState, ReactNode } from "react";

interface CalcPageProps {
  title: string;
  subtitle: string;
  tab1Label: string;
  tab2Label: string;
  tab1Content: ReactNode;
  tab2Content: ReactNode;
  infoTitle: string;
  infoItems: string[];
}

export default function CalcPage({
  title, subtitle, tab1Label, tab2Label,
  tab1Content, tab2Content, infoTitle, infoItems,
}: CalcPageProps) {
  const [tab, setTab] = useState(0);

  return (
    <div className="page-container">
      <h1 className="page-title">{title}</h1>
      <p className="page-subtitle">{subtitle}</p>

      <div className="tab-switcher">
        <button className={`tab-btn${tab === 0 ? " active" : ""}`} onClick={() => setTab(0)}>
          {tab1Label}
        </button>
        <button className={`tab-btn${tab === 1 ? " active" : ""}`} onClick={() => setTab(1)}>
          {tab2Label}
        </button>
      </div>

      {tab === 0 ? tab1Content : tab2Content}

      <div className="info-card">
        <h3>📖 {infoTitle}</h3>
        {infoItems.map((item, i) => (
          <p key={i}>{item}</p>
        ))}
      </div>
    </div>
  );
}
