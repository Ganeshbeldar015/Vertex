import React from "react";
import { AlertCircle, ShieldAlert, CheckCircle2, Play } from "lucide-react";

export interface AlertItem {
  id: string;
  account_id: string;
  rule: string;
  severity: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW";
  created_at: string;
  status: "NEW" | "INVESTIGATED" | "RESOLVED";
  risk_score?: number;
}

interface AlertQueueProps {
  alerts: AlertItem[];
  selectedAlertId: string | null;
  onSelectAlert: (alert: AlertItem) => void;
  onInvestigate: (accountId: string, alertId: string) => void;
  isLoading: boolean;
}

export const AlertQueue: React.FC<AlertQueueProps> = ({
  alerts,
  selectedAlertId,
  onSelectAlert,
  onInvestigate,
  isLoading,
}) => {
  const getSeverityBadge = (severity: string) => {
    switch (severity) {
      case "CRITICAL":
        return (
          <span className="px-2 py-0.5 text-[10px] font-bold tracking-wider rounded bg-maroon-950 text-rose-300 border border-maroon-700/80 shadow-maroon-subtle flex items-center space-x-1">
            <span className="w-1.5 h-1.5 rounded-full bg-rose-500 animate-pulse inline-block mr-1" />
            CRITICAL
          </span>
        );
      case "HIGH":
        return (
          <span className="px-2 py-0.5 text-[10px] font-bold tracking-wider rounded bg-[#4a0410] text-rose-200 border border-maroon-800">
            HIGH
          </span>
        );
      case "MEDIUM":
        return (
          <span className="px-2 py-0.5 text-[10px] font-bold tracking-wider rounded bg-amber-950/70 text-amber-300 border border-amber-800/60">
            MEDIUM
          </span>
        );
      default:
        return (
          <span className="px-2 py-0.5 text-[10px] font-medium rounded bg-obsidian-850 text-slate-400 border border-slate-800">
            LOW
          </span>
        );
    }
  };

  return (
    <div className="bg-obsidian-900 border border-maroon-900/40 rounded-xl p-4 flex flex-col h-full shadow-xl">
      <div className="flex items-center justify-between pb-3 border-b border-maroon-900/40 mb-3">
        <div className="flex items-center space-x-2">
          <ShieldAlert className="w-5 h-5 text-rose-400" />
          <h2 className="text-sm font-bold tracking-wide text-slate-100 uppercase">Alert Stream</h2>
        </div>
        <span className="text-xs bg-maroon-950 text-rose-300 border border-maroon-800/80 px-2.5 py-0.5 rounded-full font-mono font-semibold">
          {alerts.length} Active
        </span>
      </div>

      <div className="overflow-y-auto space-y-2.5 flex-1 pr-1">
        {alerts.map((alert) => {
          const isSelected = selectedAlertId === alert.id;
          return (
            <div
              key={alert.id}
              onClick={() => onSelectAlert(alert)}
              className={`p-3.5 rounded-lg border transition-all cursor-pointer ${
                isSelected
                  ? "bg-obsidian-850 border-maroon-600/80 shadow-maroon-subtle"
                  : "bg-obsidian-950/70 border-maroon-900/20 hover:border-maroon-800/60 hover:bg-obsidian-900/80"
              }`}
            >
              <div className="flex items-center justify-between mb-1.5">
                <div className="flex items-center space-x-2">
                  <span className="text-sm font-bold font-mono text-slate-200">{alert.account_id}</span>
                  {alert.risk_score !== undefined && (
                    <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-obsidian-950 text-rose-400 border border-maroon-900/60">
                      {(alert.risk_score * 100).toFixed(0)}%
                    </span>
                  )}
                </div>
                {getSeverityBadge(alert.severity)}
              </div>
              <p className="text-xs text-slate-400 line-clamp-1 mb-2.5 font-mono text-[11px]">
                {alert.rule}
              </p>
              <div className="flex items-center justify-between pt-1.5 border-t border-maroon-900/20">
                <span className="text-[11px] text-slate-500 font-mono">{alert.created_at}</span>
                <button
                  disabled={isLoading}
                  onClick={(e) => {
                    e.stopPropagation();
                    onInvestigate(alert.account_id, alert.id);
                  }}
                  className="inline-flex items-center space-x-1 text-xs px-3 py-1 rounded bg-gradient-to-r from-maroon-800 to-rose-700 hover:from-maroon-700 hover:to-rose-600 text-white font-medium transition-all shadow-maroon-subtle disabled:opacity-50"
                >
                  <Play className="w-3 h-3 fill-white" />
                  <span>Investigate</span>
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
