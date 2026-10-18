import React, { useState } from "react";
import { Check, X, RotateCcw, AlertTriangle, ShieldCheck } from "lucide-react";

export interface ActionItem {
  id: string;
  type: string;
  target: string;
  status: "PENDING_APPROVAL" | "COMPLETED" | "APPROVED" | "REJECTED" | "REVERSED" | "AUTO_EXECUTED";
  reason?: string;
  approver?: string;
  tier?: string;
  timestamp?: string;
}

interface ActionApprovalPanelProps {
  actions: ActionItem[];
  onApprove: (actionId: string, approver: string) => void;
  onReject: (actionId: string, approver: string) => void;
  onReverse: (actionId: string) => void;
}

export const ActionApprovalPanel: React.FC<ActionApprovalPanelProps> = ({
  actions,
  onApprove,
  onReject,
  onReverse,
}) => {
  const [approver, setApprover] = useState("lead_analyst_sarah");

  const pendingActions = actions.filter((a) => a.status === "PENDING_APPROVAL");
  const resolvedActions = actions.filter((a) => a.status !== "PENDING_APPROVAL");

  return (
    <div className="bg-obsidian-900 border border-maroon-900/40 rounded-xl p-4 flex flex-col h-full shadow-xl">
      <div className="flex items-center justify-between pb-3 border-b border-maroon-900/40 mb-3">
        <div className="flex items-center space-x-2">
          <ShieldCheck className="w-5 h-5 text-rose-400" />
          <h2 className="text-sm font-bold tracking-wide text-slate-100 uppercase">Action Approval Console</h2>
        </div>
        <div className="flex items-center space-x-2">
          <label className="text-xs text-slate-400">Officer:</label>
          <input
            type="text"
            value={approver}
            onChange={(e) => setApprover(e.target.value)}
            className="bg-obsidian-950 border border-maroon-800/80 text-xs text-rose-200 px-2.5 py-1 rounded-md w-36 focus:outline-none focus:border-rose-500 font-mono shadow-inner"
          />
        </div>
      </div>

      {/* Pending Actions */}
      <div className="mb-4">
        <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2 flex items-center justify-between">
          <span>Pending Remediation Queue</span>
          <span className="text-[11px] bg-maroon-950 text-rose-300 border border-maroon-700/80 px-2.5 py-0.5 rounded-full font-mono font-semibold shadow-maroon-subtle">
            {pendingActions.length} Waiting
          </span>
        </h3>
        {pendingActions.length === 0 ? (
          <p className="text-xs text-slate-500 py-3 text-center bg-obsidian-950/40 rounded-lg border border-maroon-950">
            No actions awaiting approval.
          </p>
        ) : (
          <div className="space-y-2">
            {pendingActions.map((action) => (
              <div
                key={action.id}
                className="bg-obsidian-950/80 border border-maroon-900/40 rounded-lg p-3 flex items-center justify-between hover:border-maroon-700/60 transition shadow-sm"
              >
                <div>
                  <div className="flex items-center space-x-2 mb-1">
                    <span className="text-[11px] font-bold text-rose-300 font-mono bg-maroon-950 px-2 py-0.5 rounded border border-maroon-800/80">
                      {action.type}
                    </span>
                    <span className="text-xs font-mono text-slate-200 bg-obsidian-850 px-2 py-0.5 rounded border border-slate-800">
                      {action.target}
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-400">{action.reason}</p>
                </div>
                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => onApprove(action.id, approver)}
                    className="inline-flex items-center space-x-1 text-xs px-2.5 py-1 rounded bg-emerald-900 hover:bg-emerald-800 text-emerald-100 border border-emerald-700 font-medium transition"
                  >
                    <Check className="w-3.5 h-3.5" />
                    <span>Approve</span>
                  </button>
                  <button
                    onClick={() => onReject(action.id, approver)}
                    className="inline-flex items-center space-x-1 text-xs px-2.5 py-1 rounded bg-maroon-900 hover:bg-maroon-800 text-rose-200 border border-maroon-700 font-medium transition"
                  >
                    <X className="w-3.5 h-3.5" />
                    <span>Reject</span>
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Action Audit History */}
      <div className="flex-1 overflow-y-auto">
        <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2">
          Immutable Action Trail
        </h3>
        <div className="space-y-1.5">
          {resolvedActions.map((action) => (
            <div
              key={action.id}
              className="text-xs bg-obsidian-950/60 border border-maroon-950 rounded-lg p-2.5 flex items-center justify-between"
            >
              <div>
                <span className="font-mono text-slate-300 font-bold mr-2">{action.target}</span>
                <span className="text-slate-400 font-mono text-[11px]">{action.type}</span>
                <span className="text-[10px] text-slate-500 ml-2">by {action.approver || "SYSTEM"}</span>
              </div>
              <div className="flex items-center space-x-2">
                <span
                  className={`px-2 py-0.5 rounded text-[10px] font-bold font-mono ${
                    action.status === "COMPLETED" || action.status === "APPROVED" || action.status === "AUTO_EXECUTED"
                      ? "bg-emerald-950 text-emerald-400 border border-emerald-800/60"
                      : action.status === "REVERSED"
                      ? "bg-purple-950 text-purple-300 border border-purple-800/60"
                      : "bg-maroon-950 text-rose-400 border border-maroon-800/60"
                  }`}
                >
                  {action.status}
                </span>
                {(action.status === "COMPLETED" || action.status === "APPROVED") && (
                  <button
                    onClick={() => onReverse(action.id)}
                    title="Reverse action"
                    className="p-1 hover:bg-maroon-950 rounded text-slate-400 hover:text-rose-300 transition"
                  >
                    <RotateCcw className="w-3 h-3" />
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
