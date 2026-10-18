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
    <div className="bg-slate-900 border border-slate-800 rounded-lg p-4 flex flex-col h-full shadow-lg">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-3">
        <div className="flex items-center space-x-2">
          <ShieldCheck className="w-5 h-5 text-emerald-400" />
          <h2 className="text-base font-semibold text-slate-100">Gated Action Approval Panel</h2>
        </div>
        <div className="flex items-center space-x-2">
          <label className="text-xs text-slate-400">Approver:</label>
          <input
            type="text"
            value={approver}
            onChange={(e) => setApprover(e.target.value)}
            className="bg-slate-950 border border-slate-700 text-xs text-slate-200 px-2 py-1 rounded w-36 focus:outline-none focus:border-cyan-500"
          />
        </div>
      </div>

      {/* Pending Actions */}
      <div className="mb-4">
        <h3 className="text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2 flex items-center justify-between">
          <span>Pending Remediation Requests</span>
          <span className="text-[11px] bg-amber-950 text-amber-400 border border-amber-800 px-2 py-0.5 rounded">
            {pendingActions.length} Waiting
          </span>
        </h3>
        {pendingActions.length === 0 ? (
          <p className="text-xs text-slate-500 py-3 text-center bg-slate-950/40 rounded border border-slate-800/60">
            No actions awaiting approval.
          </p>
        ) : (
          <div className="space-y-2">
            {pendingActions.map((action) => (
              <div
                key={action.id}
                className="bg-slate-950/80 border border-slate-800 rounded-md p-3 flex items-center justify-between"
              >
                <div>
                  <div className="flex items-center space-x-2 mb-1">
                    <span className="text-xs font-bold text-red-400 font-mono">{action.type}</span>
                    <span className="text-xs font-mono text-slate-200 bg-slate-800 px-1.5 py-0.5 rounded">
                      {action.target}
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-400">{action.reason}</p>
                </div>
                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => onApprove(action.id, approver)}
                    className="inline-flex items-center space-x-1 text-xs px-2.5 py-1 rounded bg-emerald-600 hover:bg-emerald-500 text-white font-medium transition"
                  >
                    <Check className="w-3.5 h-3.5" />
                    <span>Approve</span>
                  </button>
                  <button
                    onClick={() => onReject(action.id, approver)}
                    className="inline-flex items-center space-x-1 text-xs px-2.5 py-1 rounded bg-red-800 hover:bg-red-700 text-white font-medium transition"
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
        <h3 className="text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
          Action Audit Trail
        </h3>
        <div className="space-y-1.5">
          {resolvedActions.map((action) => (
            <div
              key={action.id}
              className="text-xs bg-slate-950/50 border border-slate-800/70 rounded p-2 flex items-center justify-between"
            >
              <div>
                <span className="font-mono text-slate-300 font-bold mr-2">{action.target}</span>
                <span className="text-slate-400">{action.type}</span>
                <span className="text-[11px] text-slate-500 ml-2">by {action.approver || "SYSTEM"}</span>
              </div>
              <div className="flex items-center space-x-2">
                <span
                  className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${
                    action.status === "COMPLETED" || action.status === "APPROVED" || action.status === "AUTO_EXECUTED"
                      ? "bg-emerald-950 text-emerald-400"
                      : action.status === "REVERSED"
                      ? "bg-purple-950 text-purple-400"
                      : "bg-red-950 text-red-400"
                  }`}
                >
                  {action.status}
                </span>
                {(action.status === "COMPLETED" || action.status === "APPROVED") && (
                  <button
                    onClick={() => onReverse(action.id)}
                    title="Reverse action"
                    className="p-1 hover:bg-slate-800 rounded text-slate-400 hover:text-purple-300"
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
