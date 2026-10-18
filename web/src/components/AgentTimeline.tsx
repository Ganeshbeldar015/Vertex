import React from "react";
import { CheckCircle2, CircleDot, Activity, ChevronRight, Terminal } from "lucide-react";

export interface ToolCallStep {
  tool: string;
  args?: Record<string, any>;
  arguments?: Record<string, any>;
  result?: Record<string, any>;
}

export interface Hypothesis {
  name: string;
  status: "CONFIRMED" | "REFUTED" | "UNTESTED";
  evidence?: string[];
}

interface AgentTimelineProps {
  timeline: ToolCallStep[];
  hypotheses: Hypothesis[];
  rationale: string;
}

export const AgentTimeline: React.FC<AgentTimelineProps> = ({
  timeline,
  hypotheses,
  rationale,
}) => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-lg p-4 flex flex-col h-full shadow-lg">
      <div className="flex items-center space-x-2 pb-3 border-b border-slate-800 mb-3">
        <Activity className="w-5 h-5 text-cyan-400" />
        <h2 className="text-base font-semibold text-slate-100">Live Agent Reasoning Timeline</h2>
      </div>

      {/* Hypotheses Overview */}
      {hypotheses.length > 0 && (
        <div className="mb-4 bg-slate-950/70 border border-slate-800/80 rounded-md p-3">
          <h3 className="text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
            Tested Hypotheses
          </h3>
          <div className="space-y-1.5">
            {hypotheses.map((h, i) => (
              <div key={i} className="flex items-center justify-between text-xs">
                <span className="text-slate-300 font-mono">{h.name}</span>
                <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-950 text-emerald-400 border border-emerald-800">
                  {h.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Stepper Timeline */}
      <div className="overflow-y-auto flex-1 space-y-3 pr-1">
        {timeline.map((step, idx) => {
          const args = step.args || step.arguments || {};
          return (
            <div key={idx} className="relative pl-6 border-l-2 border-slate-700/60 pb-1">
              <div className="absolute -left-1.5 top-0 w-3 h-3 rounded-full bg-cyan-500 border-2 border-slate-900" />
              <div className="bg-slate-950/60 border border-slate-800 rounded p-2.5">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs font-bold text-cyan-400 font-mono">
                    Step {idx + 1}: {step.tool}
                  </span>
                  <Terminal className="w-3.5 h-3.5 text-slate-500" />
                </div>
                <div className="text-[11px] text-slate-400 font-mono bg-slate-900/80 p-1.5 rounded overflow-x-auto">
                  {JSON.stringify(args)}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Agent Narrative Summary */}
      {rationale && (
        <div className="mt-4 pt-3 border-t border-slate-800">
          <h4 className="text-xs font-semibold text-slate-400 mb-1">Synthesized Rationale:</h4>
          <p className="text-xs text-slate-300 leading-relaxed bg-slate-950/80 p-2.5 rounded border border-slate-800">
            {rationale}
          </p>
        </div>
      )}
    </div>
  );
};
