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
    <div className="bg-obsidian-900 border border-maroon-900/40 rounded-xl p-4 flex flex-col h-full shadow-xl">
      <div className="flex items-center space-x-2 pb-3 border-b border-maroon-900/40 mb-3">
        <Activity className="w-5 h-5 text-rose-400" />
        <h2 className="text-sm font-bold tracking-wide text-slate-100 uppercase">Agent Reasoning Trail</h2>
      </div>

      {/* Hypotheses Overview */}
      {hypotheses.length > 0 && (
        <div className="mb-4 bg-obsidian-950/80 border border-maroon-900/40 rounded-lg p-3.5">
          <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2 flex items-center justify-between">
            <span>Evaluated Hypotheses</span>
            <span className="text-[10px] text-rose-300 font-mono">Multi-Hop Evidence</span>
          </h3>
          <div className="space-y-1.5">
            {hypotheses.map((h, i) => (
              <div key={i} className="flex items-center justify-between text-xs">
                <span className="text-slate-300 font-mono">{h.name}</span>
                <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-maroon-950 text-rose-300 border border-maroon-700/70 shadow-maroon-subtle">
                  {h.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Stepper Timeline */}
      <div className="overflow-y-auto flex-1 space-y-3.5 pr-1">
        {timeline.map((step, idx) => {
          const args = step.args || step.arguments || {};
          return (
            <div key={idx} className="relative pl-6 border-l-2 border-maroon-900/60 pb-1">
              <div className="absolute -left-[5px] top-0 w-2.5 h-2.5 rounded-full bg-rose-500 border-2 border-obsidian-950 shadow-maroon-subtle" />
              <div className="bg-obsidian-950/70 border border-maroon-900/30 rounded-lg p-3 hover:border-maroon-800/60 transition">
                <div className="flex items-center justify-between mb-1.5">
                  <span className="text-xs font-bold text-rose-300 font-mono">
                    Step {idx + 1}: {step.tool}
                  </span>
                  <Terminal className="w-3.5 h-3.5 text-slate-500" />
                </div>
                <div className="text-[11px] text-slate-300 font-mono bg-obsidian-900/90 p-2 rounded border border-maroon-950 overflow-x-auto">
                  {JSON.stringify(args)}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Agent Narrative Summary */}
      {rationale && (
        <div className="mt-4 pt-3 border-t border-maroon-900/40">
          <h4 className="text-xs font-bold text-slate-400 mb-1.5 uppercase tracking-wider">Synthesized Verdict:</h4>
          <p className="text-xs text-slate-300 leading-relaxed bg-obsidian-950/80 p-3 rounded-lg border border-maroon-900/40">
            {rationale}
          </p>
        </div>
      )}
    </div>
  );
};
