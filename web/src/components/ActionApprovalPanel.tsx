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
    <div className="bg-white border border-slate-200 rounded-xl p-4 flex flex-col h-full shadow-sm">
      <div className="flex items-center justify-between pb-3 border-b border-slate-200 mb-3">
        <div className="flex items-center space-x-2">
          <ShieldCheck className="w-5 h-5 text-emerald-600" />
          <h2 className="text-sm font-bold tracking-wide text-slate-900 uppercase">Action Approval Console</h2>
        </div>
        <div className="flex items-center space-x-2">
          <label className="text-xs text-slate-500 font-medium">Officer:</label>
          <input
            type="text"
            value={approver}
            onChange={(e) => setApprover(e.target.value)}
            className="bg-slate-50 border border-slate-300 text-xs text-slate-800 px-2.5 py-1 rounded-md w-36 focus:outline-none focus:border-maroon-600 font-mono shadow-inner"
          />
        </div>
      </div>

      {/* Pending Actions */}
      <div className="mb-4">
        <h3 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-2 flex items-center justify-between">
          <span>Pending Remediation Queue</span>
          <span className="text-[11px] bg-maroon-50 text-maroon-800 border border-maroon-200 px-2.5 py-0.5 rounded-full font-mono font-semibold">
            {pendingActions.length} Waiting
          </span>
        </h3>
        {pendingActions.length === 0 ? (
          <p className="text-xs text-slate-500 py-3 text-center bg-slate-50 rounded-lg border border-slate-200">
            No actions awaiting approval.
          </p>
        ) : (
          <div className="space-y-2">
            {pendingActions.map((action) => (
              <div
                key={action.id}
                className="bg-slate-50/80 border border-slate-200 rounded-lg p-3 flex items-center justify-between hover:border-maroon-200 transition shadow-sm"
              >
                <div>
                  <div className="flex items-center space-x-2 mb-1">
                    <span className="text-[11px] font-bold text-maroon-900 font-mono bg-maroon-100 px-2 py-0.5 rounded border border-maroon-200">
                      {action.type}
                    </span>
                    <span className="text-xs font-mono text-slate-800 bg-white px-2 py-0.5 rounded border border-slate-200">
                      {action.target}
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-600">{action.reason}</p>
                </div>
                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => onApprove(action.id, approver)}
                    className="inline-flex items-center space-x-1 text-xs px-2.5 py-1 rounded bg-emerald-600 hover:bg-emerald-700 text-white font-medium transition shadow-sm"
                  >
                    <Check className="w-3.5 h-3.5" />
                    <span>Approve</span>
                  </button>
                  <button
                    onClick={() => onReject(action.id, approver)}
                    className="inline-flex items-center space-x-1 text-xs px-2.5 py-1 rounded bg-maroon-800 hover:bg-maroon-900 text-white font-medium transition shadow-sm"
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
        <h3 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
          Immutable Action Trail
        </h3>
        <div className="space-y-1.5">
          {resolvedActions.map((action) => (
            <div
              key={action.id}
              className="text-xs bg-slate-50 border border-slate-200 rounded-lg p-2.5 flex items-center justify-between"
            >
              <div>
                <span className="font-mono text-slate-900 font-bold mr-2">{action.target}</span>
                <span className="text-slate-600 font-mono text-[11px]">{action.type}</span>
                <span className="text-[10px] text-slate-400 ml-2">by {action.approver || "SYSTEM"}</span>
              </div>
              <div className="flex items-center space-x-2">
                <span
                  className={`px-2 py-0.5 rounded text-[10px] font-bold font-mono ${
                    action.status === "COMPLETED" || action.status === "APPROVED" || action.status === "AUTO_EXECUTED"
                      ? "bg-emerald-50 text-emerald-700 border border-emerald-200"
                      : action.status === "REVERSED"
                      ? "bg-purple-50 text-purple-700 border border-purple-200"
                      : "bg-red-50 text-red-700 border border-red-200"
                  }`}
                >
                  {action.status}
                </span>
                {(action.status === "COMPLETED" || action.status === "APPROVED") && (
                  <button
                    onClick={() => onReverse(action.id)}
                    title="Reverse action"
                    className="p-1 hover:bg-slate-200 rounded text-slate-400 hover:text-purple-700 transition"
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
