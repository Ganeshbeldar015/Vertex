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
        return <span className="px-2 py-0.5 text-xs font-semibold rounded bg-red-950 text-red-400 border border-red-800">CRITICAL</span>;
      case "HIGH":
        return <span className="px-2 py-0.5 text-xs font-semibold rounded bg-orange-950 text-orange-400 border border-orange-800">HIGH</span>;
      case "MEDIUM":
        return <span className="px-2 py-0.5 text-xs font-semibold rounded bg-yellow-950 text-yellow-400 border border-yellow-800">MEDIUM</span>;
      default:
        return <span className="px-2 py-0.5 text-xs font-semibold rounded bg-slate-800 text-slate-300">LOW</span>;
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-lg p-4 flex flex-col h-full shadow-lg">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-3">
        <div className="flex items-center space-x-2">
          <ShieldAlert className="w-5 h-5 text-red-400" />
          <h2 className="text-base font-semibold text-slate-100">Prioritized Alert Queue</h2>
        </div>
        <span className="text-xs bg-slate-800 text-slate-400 px-2 py-1 rounded">
          {alerts.length} Active
        </span>
      </div>

      <div className="overflow-y-auto space-y-2 flex-1 pr-1">
        {alerts.map((alert) => {
          const isSelected = selectedAlertId === alert.id;
          return (
            <div
              key={alert.id}
              onClick={() => onSelectAlert(alert)}
              className={`p-3 rounded-md border transition-all cursor-pointer ${
                isSelected
                  ? "bg-slate-800/80 border-cyan-500/50 shadow-md"
                  : "bg-slate-950/60 border-slate-800 hover:border-slate-700"
              }`}
            >
              <div className="flex items-center justify-between mb-1">
                <span className="text-sm font-bold text-slate-200">{alert.account_id}</span>
                {getSeverityBadge(alert.severity)}
              </div>
              <p className="text-xs text-slate-400 line-clamp-1 mb-2 font-mono">
                {alert.rule}
              </p>
              <div className="flex items-center justify-between pt-1 border-t border-slate-800/60">
                <span className="text-[11px] text-slate-500">{alert.created_at}</span>
                <button
                  disabled={isLoading}
                  onClick={(e) => {
                    e.stopPropagation();
                    onInvestigate(alert.account_id, alert.id);
                  }}
                  className="inline-flex items-center space-x-1 text-xs px-2.5 py-1 rounded bg-cyan-600 hover:bg-cyan-500 text-white font-medium transition-colors disabled:opacity-50"
                >
                  <Play className="w-3 h-3" />
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
