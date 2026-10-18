import React, { useState } from "react";
import { X, Download, Copy, Check, FileText } from "lucide-react";

interface CaseReportModalProps {
  isOpen: boolean;
  onClose: () => void;
  caseId: string;
  markdownContent: string;
}

export const CaseReportModal: React.FC<CaseReportModalProps> = ({
  isOpen,
  onClose,
  caseId,
  markdownContent,
}) => {
  const [copied, setCopied] = useState(false);

  if (!isOpen) return null;

  const handleCopy = () => {
    navigator.clipboard.writeText(markdownContent);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const blob = new Blob([markdownContent], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${caseId}-report.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/85 backdrop-blur-md p-4">
      <div className="bg-obsidian-900 border border-maroon-700/60 rounded-xl max-w-2xl w-full max-h-[85vh] flex flex-col shadow-maroon-glow">
        <div className="flex items-center justify-between p-4 border-b border-maroon-900/50">
          <div className="flex items-center space-x-2">
            <FileText className="w-5 h-5 text-rose-400" />
            <h3 className="text-sm font-bold tracking-wide text-slate-100 uppercase">
              Investigation Dossier ({caseId})
            </h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 hover:bg-maroon-950 rounded text-slate-400 hover:text-white transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-4 overflow-y-auto flex-1 font-mono text-xs text-rose-100 bg-obsidian-950 m-4 rounded-lg border border-maroon-900/40 whitespace-pre-wrap leading-relaxed shadow-inner">
          {markdownContent}
        </div>

        <div className="p-4 border-t border-maroon-900/50 flex justify-end space-x-2.5 bg-obsidian-900/50">
          <button
            onClick={handleCopy}
            className="inline-flex items-center space-x-1.5 px-3.5 py-1.5 rounded-lg bg-obsidian-850 hover:bg-maroon-950 text-rose-200 text-xs font-medium border border-maroon-800/60 transition"
          >
            {copied ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
            <span>{copied ? "Copied!" : "Copy Markdown"}</span>
          </button>
          <button
            onClick={handleDownload}
            className="inline-flex items-center space-x-1.5 px-3.5 py-1.5 rounded-lg bg-gradient-to-r from-maroon-800 to-rose-700 hover:from-maroon-700 hover:to-rose-600 text-white text-xs font-medium transition shadow-maroon-subtle"
          >
            <Download className="w-4 h-4" />
            <span>Download Report</span>
          </button>
        </div>
      </div>
    </div>
  );
};
