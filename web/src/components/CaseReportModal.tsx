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
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-sm p-4">
      <div className="bg-white border border-slate-200 rounded-xl max-w-2xl w-full max-h-[85vh] flex flex-col shadow-2xl">
        <div className="flex items-center justify-between p-4 border-b border-slate-200">
          <div className="flex items-center space-x-2">
            <FileText className="w-5 h-5 text-maroon-700" />
            <h3 className="text-sm font-bold tracking-wide text-slate-900 uppercase">
              Investigation Dossier ({caseId})
            </h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 hover:bg-slate-100 rounded text-slate-500 hover:text-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-4 overflow-y-auto flex-1 font-mono text-xs text-slate-800 bg-slate-50 m-4 rounded-lg border border-slate-200 whitespace-pre-wrap leading-relaxed shadow-inner">
          {markdownContent}
        </div>

        <div className="p-4 border-t border-slate-200 flex justify-end space-x-2.5 bg-slate-50/50">
          <button
            onClick={handleCopy}
            className="inline-flex items-center space-x-1.5 px-3.5 py-1.5 rounded-lg bg-white hover:bg-slate-100 text-slate-700 text-xs font-semibold border border-slate-200 transition shadow-sm"
          >
            {copied ? <Check className="w-4 h-4 text-emerald-600" /> : <Copy className="w-4 h-4 text-slate-500" />}
            <span>{copied ? "Copied!" : "Copy Markdown"}</span>
          </button>
          <button
            onClick={handleDownload}
            className="inline-flex items-center space-x-1.5 px-3.5 py-1.5 rounded-lg bg-gradient-to-r from-maroon-800 to-rose-700 hover:from-maroon-900 hover:to-rose-800 text-white text-xs font-semibold transition shadow-sm"
          >
            <Download className="w-4 h-4" />
            <span>Download Report</span>
          </button>
        </div>
      </div>
    </div>
  );
};
