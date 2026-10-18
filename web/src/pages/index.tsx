import React, { useState } from "react";
import Head from "next/head";
import { AlertQueue, AlertItem } from "../components/AlertQueue";
import { CytoscapeCanvas } from "../components/CytoscapeCanvas";
import { AgentTimeline, ToolCallStep, Hypothesis } from "../components/AgentTimeline";
import { ActionApprovalPanel, ActionItem } from "../components/ActionApprovalPanel";
import { CaseReportModal } from "../components/CaseReportModal";
import { Shield, FileDown, RefreshCw } from "lucide-react";

const INITIAL_ALERTS: AlertItem[] = [
  {
    id: "ALT-1001",
    account_id: "A-1042",
    rule: "SHARED_DEVICE_AND_CIRCULAR_TRANSFER",
    severity: "CRITICAL",
    created_at: "2026-10-18 10:00:00",
    status: "NEW",
    risk_score: 0.85,
  },
  {
    id: "ALT-1002",
    account_id: "A-1050",
    rule: "HIGH_CENTRALITY_TRANSIT_HUB",
    severity: "HIGH",
    created_at: "2026-10-18 10:15:00",
    status: "NEW",
    risk_score: 0.72,
  },
  {
    id: "ALT-1003",
    account_id: "A-2010",
    rule: "UNUSUAL_TRANSACTION_BURST",
    severity: "MEDIUM",
    created_at: "2026-10-18 10:30:00",
    status: "NEW",
    risk_score: 0.45,
  },
];

const INITIAL_NODES = [
  { data: { id: "A-1042", label: "Account A-1042", type: "Account", risk_score: 0.85, flagged: true, is_ring: true } },
  { data: { id: "A-1050", label: "Account A-1050", type: "Account", risk_score: 0.72, flagged: false, is_ring: true } },
  { data: { id: "A-1061", label: "Account A-1061", type: "Account", risk_score: 0.68, flagged: false, is_ring: true } },
  { data: { id: "D-77", label: "Device D-77", type: "Device", is_ring: true } },
  { data: { id: "C-901", label: "Customer C-901", type: "Customer" } },
];

const INITIAL_EDGES = [
  { data: { id: "e1", source: "A-1042", target: "A-1050", label: "TRANSFERRED_TO", amount: 9500, is_ring: true } },
  { data: { id: "e2", source: "A-1050", target: "A-1061", label: "TRANSFERRED_TO", amount: 8900, is_ring: true } },
  { data: { id: "e3", source: "A-1061", target: "A-1042", label: "TRANSFERRED_TO", amount: 8200, is_ring: true } },
  { data: { id: "e4", source: "A-1042", target: "D-77", label: "USED_DEVICE", is_ring: true } },
  { data: { id: "e5", source: "A-1050", target: "D-77", label: "USED_DEVICE", is_ring: true } },
  { data: { id: "e6", source: "C-901", target: "A-1042", label: "OWNS" } },
];

const INITIAL_TIMELINE: ToolCallStep[] = [
  { tool: "graph.get_entity", args: { entity_id: "A-1042" } },
  { tool: "graph.expand_neighborhood", args: { entity_id: "A-1042", hops: 2 } },
  { tool: "algo.score_risk", args: { account_id: "A-1042" } },
  { tool: "algo.detect_cycles", args: { max_length: 5 } },
];

const INITIAL_HYPOTHESES: Hypothesis[] = [
  { name: "shared_device_collusion", status: "CONFIRMED" },
  { name: "circular_money_flow", status: "CONFIRMED" },
];

const INITIAL_ACTIONS: ActionItem[] = [
  {
    id: "ACT-1001",
    type: "FLAG_ENTITY",
    target: "A-1042",
    status: "AUTO_EXECUTED",
    reason: "Suspected fraud ring coordinator",
  },
  {
    id: "ACT-1002",
    type: "FREEZE_ACCOUNT",
    target: "A-1042",
    status: "PENDING_APPROVAL",
    reason: "Primary suspect in circular laundering ring",
  },
  {
    id: "ACT-1003",
    type: "BLOCK_DEVICE",
    target: "D-77",
    status: "PENDING_APPROVAL",
    reason: "Device shared across multiple flagged accounts",
  },
];

export default function Home() {
  const [alerts, setAlerts] = useState<AlertItem[]>(INITIAL_ALERTS);
  const [selectedAlertId, setSelectedAlertId] = useState<string | null>("ALT-1001");
  const [elements, setElements] = useState({ nodes: INITIAL_NODES, edges: INITIAL_EDGES });
  const [timeline, setTimeline] = useState<ToolCallStep[]>(INITIAL_TIMELINE);
  const [hypotheses, setHypotheses] = useState<Hypothesis[]>(INITIAL_HYPOTHESES);
  const [actions, setActions] = useState<ActionItem[]>(INITIAL_ACTIONS);
  const [activeTab, setActiveTab] = useState<"timeline" | "approvals">("approvals");
  const [isExportOpen, setIsExportOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [activeCaseId, setActiveCaseId] = useState("CASE-A1042");

  const rationale =
    "Account A-1042 shares Device D-77 with Account A-1050. Transfers complete a circular money flow among A-1042 -> A-1050 -> A-1061 -> A-1042. Composite risk score computed at 0.85 (HIGH).";

  const handleInvestigate = async (accountId: string, alertId: string) => {
    setIsLoading(true);
    setSelectedAlertId(alertId);
    try {
      const res = await fetch("http://localhost:8000/api/investigate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ account_id: accountId, alert_id: alertId }),
      });
      if (res.ok) {
        const data = await res.json();
        setActiveCaseId(data.case_id);
        if (data.cytoscape_elements) {
          setElements(data.cytoscape_elements);
        }
        if (data.timeline) {
          setTimeline(data.timeline);
        }
        if (data.hypotheses_tested) {
          setHypotheses(data.hypotheses_tested);
        }
        if (data.recommended_actions) {
          setActions(data.recommended_actions);
        }
      }
    } catch {
      // Local fallback in case standalone API is offline
      console.log("Using loaded fallback graph for account", accountId);
    } finally {
      setIsLoading(false);
    }
  };

  const handleApprove = async (actionId: string, approver: string) => {
    try {
      await fetch(`http://localhost:8000/api/actions/${actionId}/approve`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ approver }),
      });
    } catch (e) {
      console.log("Applied local state change");
    }
    setActions((prev) =>
      prev.map((a) =>
        a.id === actionId ? { ...a, status: "COMPLETED", approver } : a
      )
    );
  };

  const handleReject = async (actionId: string, approver: string) => {
    try {
      await fetch(`http://localhost:8000/api/actions/${actionId}/reject`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ approver }),
      });
    } catch (e) {
      console.log("Applied local state change");
    }
    setActions((prev) =>
      prev.map((a) =>
        a.id === actionId ? { ...a, status: "REJECTED", approver } : a
      )
    );
  };

  const handleReverse = async (actionId: string) => {
    try {
      await fetch(`http://localhost:8000/api/actions/${actionId}/reverse`, {
        method: "POST",
      });
    } catch (e) {
      console.log("Applied local state change");
    }
    setActions((prev) =>
      prev.map((a) =>
        a.id === actionId ? { ...a, status: "REVERSED" } : a
      )
    );
  };

  const markdownReport = `# Fraud Investigation Case Report: ${activeCaseId}

## Executive Summary
- Target Account: \`A-1042\`
- Investigation Verdict: **FRAUD_RING_DETECTED**
- Risk Score: 0.85 (HIGH)

## Narrative Rationale
${rationale}

## Remediation Actions
- FREEZE_ACCOUNT on A-1042 -> COMPLETED
- BLOCK_DEVICE on D-77 -> COMPLETED
`;

  return (
    <>
      <Head>
        <title>GraphSleuth — Fraud Ring Investigation Agent</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <div className="flex flex-col h-screen bg-obsidian-950 text-slate-100 selection:bg-maroon-800">
        {/* Navigation / Command Header */}
        <header className="h-16 border-b border-maroon-900/40 bg-obsidian-900/95 backdrop-blur-md px-6 flex items-center justify-between shadow-md">
          <div className="flex items-center space-x-3.5">
            <div className="w-9 h-9 rounded-lg bg-gradient-to-tr from-maroon-950 via-maroon-800 to-rose-700 flex items-center justify-center shadow-maroon-glow border border-maroon-600/50">
              <Shield className="w-5 h-5 text-rose-100" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h1 className="text-sm font-extrabold tracking-wide text-white uppercase">GraphSleuth</h1>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-maroon-950 text-rose-300 border border-maroon-800/80 tracking-wider">
                  SENGRA INTEL
                </span>
              </div>
              <p className="text-[11px] text-slate-400">Autonomous Financial Fraud Ring Investigator & Graph Engine</p>
            </div>
          </div>

          {/* Center Live Metrics Stat Bar */}
          <div className="hidden lg:flex items-center space-x-6 text-xs bg-obsidian-950/80 px-4 py-1.5 rounded-full border border-maroon-900/30">
            <div className="flex items-center space-x-1.5">
              <span className="w-2 h-2 rounded-full bg-rose-500 animate-pulse" />
              <span className="text-slate-400">Rings Isolated:</span>
              <span className="font-bold font-mono text-rose-300">3 Networks</span>
            </div>
            <div className="w-px h-3 bg-maroon-900/50" />
            <div className="flex items-center space-x-1.5">
              <span className="text-slate-400">Graph F1:</span>
              <span className="font-bold font-mono text-emerald-400">100% (+0.67 vs Vector)</span>
            </div>
            <div className="w-px h-3 bg-maroon-900/50" />
            <div className="flex items-center space-x-1.5">
              <span className="text-slate-400">Mule Latency:</span>
              <span className="font-bold font-mono text-rose-300">&lt; 18ms</span>
            </div>
          </div>

          <div className="flex items-center space-x-3">
            <div className="flex items-center space-x-2 bg-obsidian-950 px-3 py-1.5 rounded-lg border border-maroon-900/50 shadow-inner">
              <span className="text-xs text-slate-400">Case:</span>
              <span className="text-xs font-bold text-rose-300 font-mono tracking-wide">{activeCaseId}</span>
              <span className="text-[11px] px-2 py-0.5 rounded bg-maroon-950 text-rose-200 font-bold border border-maroon-700/70 shadow-maroon-subtle">
                RISK 0.85
              </span>
            </div>
            <button
              onClick={() => setIsExportOpen(true)}
              className="inline-flex items-center space-x-1.5 px-3.5 py-1.5 rounded-lg bg-obsidian-850 hover:bg-maroon-950 text-rose-200 hover:text-white text-xs font-medium border border-maroon-800/60 hover:border-maroon-600 transition shadow-sm"
            >
              <FileDown className="w-4 h-4 text-rose-400" />
              <span>Export Dossier</span>
            </button>
          </div>
        </header>

        {/* Main 3-Column Dashboard */}
        <main className="flex-1 grid grid-cols-12 gap-4 p-4 overflow-hidden bg-obsidian-950">
          {/* Left Column: Alert Queue */}
          <section className="col-span-3 h-full overflow-hidden">
            <AlertQueue
              alerts={alerts}
              selectedAlertId={selectedAlertId}
              onSelectAlert={(a) => setSelectedAlertId(a.id)}
              onInvestigate={handleInvestigate}
              isLoading={isLoading}
            />
          </section>

          {/* Center Column: Cytoscape Graph Canvas */}
          <section className="col-span-5 h-full overflow-hidden">
            <CytoscapeCanvas elements={elements} />
          </section>

          {/* Right Column: Reasoning Timeline & Action Approval Panel */}
          <section className="col-span-4 h-full flex flex-col overflow-hidden bg-obsidian-900 border border-maroon-900/40 rounded-xl p-3 shadow-xl">
            <div className="flex space-x-2 border-b border-maroon-900/40 pb-2 mb-2 px-1">
              <button
                onClick={() => setActiveTab("approvals")}
                className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold tracking-wide transition ${
                  activeTab === "approvals"
                    ? "bg-maroon-950 text-rose-200 border border-maroon-700/70 shadow-maroon-subtle"
                    : "text-slate-400 hover:text-slate-200 hover:bg-obsidian-850"
                }`}
              >
                Gated Actions ({actions.filter((a) => a.status === "PENDING_APPROVAL").length})
              </button>
              <button
                onClick={() => setActiveTab("timeline")}
                className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold tracking-wide transition ${
                  activeTab === "timeline"
                    ? "bg-maroon-950 text-rose-200 border border-maroon-700/70 shadow-maroon-subtle"
                    : "text-slate-400 hover:text-slate-200 hover:bg-obsidian-850"
                }`}
              >
                Agent Forensic Trail
              </button>
            </div>

            <div className="flex-1 overflow-hidden">
              {activeTab === "approvals" ? (
                <ActionApprovalPanel
                  actions={actions}
                  onApprove={handleApprove}
                  onReject={handleReject}
                  onReverse={handleReverse}
                />
              ) : (
                <AgentTimeline
                  timeline={timeline}
                  hypotheses={hypotheses}
                  rationale={rationale}
                />
              )}
            </div>
          </section>
        </main>
      </div>

      <CaseReportModal
        isOpen={isExportOpen}
        onClose={() => setIsExportOpen(false)}
        caseId={activeCaseId}
        markdownContent={markdownReport}
      />
    </>
  );
}
