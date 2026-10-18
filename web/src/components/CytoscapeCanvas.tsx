import React, { useEffect, useRef, useState } from "react";
import cytoscape, { Core } from "cytoscape";
import { ZoomIn, ZoomOut, Maximize2, Shield } from "lucide-react";

export interface CytoscapeElement {
  data: {
    id: string;
    label?: string;
    source?: string;
    target?: string;
    type?: string;
    risk_score?: number;
    flagged?: boolean;
    is_ring?: boolean;
    amount?: number;
    properties?: Record<string, any>;
  };
}

interface CytoscapeCanvasProps {
  elements: {
    nodes: CytoscapeElement[];
    edges: CytoscapeElement[];
  };
  onSelectNode?: (nodeData: any) => void;
}

export const CytoscapeCanvas: React.FC<CytoscapeCanvasProps> = ({ elements, onSelectNode }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const cyRef = useRef<Core | null>(null);
  const [selectedElement, setSelectedElement] = useState<any | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    const cyElements: any[] = [
      ...elements.nodes.map((n) => ({ ...n, group: "nodes" })),
      ...elements.edges.map((e) => ({ ...e, group: "edges" })),
    ];

    const cy = cytoscape({
      container: containerRef.current,
      elements: cyElements,
      style: [
        {
          selector: "node",
          style: {
            "background-color": "#334155",
            label: "data(label)",
            color: "#f8fafc",
            "font-size": "11px",
            "text-valign": "bottom",
            "text-margin-y": 6,
            width: 36,
            height: 36,
            "border-width": 2,
            "border-color": "#475569",
          },
        },
        {
          selector: 'node[type = "Account"]',
          style: {
            "background-color": "#2563eb",
            shape: "ellipse",
          },
        },
        {
          selector: 'node[type = "Device"]',
          style: {
            "background-color": "#9333ea",
            shape: "diamond",
            width: 32,
            height: 32,
          },
        },
        {
          selector: "node[?is_ring]",
          style: {
            "background-color": "#dc2626",
            "border-color": "#f87171",
            "border-width": 4,
            width: 44,
            height: 44,
          },
        },
        {
          selector: "edge",
          style: {
            width: 2,
            "line-color": "#475569",
            "target-arrow-color": "#475569",
            "target-arrow-shape": "triangle",
            "curve-style": "bezier",
            label: "data(label)",
            "font-size": "9px",
            color: "#94a3b8",
            "text-rotation": "autorotate",
            "text-margin-y": -6,
          },
        },
        {
          selector: "edge[?is_ring]",
          style: {
            width: 3,
            "line-color": "#ef4444",
            "target-arrow-color": "#ef4444",
          },
        },
      ],
      layout: {
        name: "cose",
        animate: true,
        animationDuration: 800,
        padding: 40,
        nodeRepulsion: () => 8000,
        idealEdgeLength: () => 90,
      },
    });

    cy.on("tap", "node", (evt) => {
      const nodeData = evt.target.data();
      setSelectedElement(nodeData);
      if (onSelectNode) onSelectNode(nodeData);
    });

    cy.on("tap", (evt) => {
      if (evt.target === cy) {
        setSelectedElement(null);
      }
    });

    cyRef.current = cy;

    return () => {
      cy.destroy();
    };
  }, [elements, onSelectNode]);

  const handleZoomIn = () => cyRef.current?.zoom(cyRef.current.zoom() * 1.25);
  const handleZoomOut = () => cyRef.current?.zoom(cyRef.current.zoom() * 0.8);
  const handleFit = () => cyRef.current?.fit();

  return (
    <div className="relative w-full h-full bg-slate-950 border border-slate-800 rounded-lg overflow-hidden flex flex-col shadow-lg">
      <div className="absolute top-3 left-3 z-10 flex items-center space-x-2 bg-slate-900/90 backdrop-blur px-3 py-1.5 rounded-md border border-slate-700/80">
        <Shield className="w-4 h-4 text-cyan-400" />
        <span className="text-xs font-semibold text-slate-200">Evidence Subgraph Canvas</span>
        <span className="text-[11px] text-slate-400">({elements.nodes.length} nodes, {elements.edges.length} edges)</span>
      </div>

      <div className="absolute top-3 right-3 z-10 flex space-x-1.5 bg-slate-900/90 backdrop-blur p-1 rounded-md border border-slate-700/80">
        <button
          onClick={handleZoomIn}
          title="Zoom In"
          className="p-1.5 hover:bg-slate-800 text-slate-300 rounded transition"
        >
          <ZoomIn className="w-4 h-4" />
        </button>
        <button
          onClick={handleZoomOut}
          title="Zoom Out"
          className="p-1.5 hover:bg-slate-800 text-slate-300 rounded transition"
        >
          <ZoomOut className="w-4 h-4" />
        </button>
        <button
          onClick={handleFit}
          title="Fit Canvas"
          className="p-1.5 hover:bg-slate-800 text-slate-300 rounded transition"
        >
          <Maximize2 className="w-4 h-4" />
        </button>
      </div>

      <div ref={containerRef} className="w-full h-full min-h-[480px]" />

      {selectedElement && (
        <div className="absolute bottom-3 left-3 right-3 z-10 bg-slate-900/95 backdrop-blur p-3 rounded-md border border-cyan-500/50 shadow-xl max-w-md">
          <div className="flex items-center justify-between mb-1">
            <span className="text-xs font-bold text-cyan-400 font-mono">{selectedElement.id}</span>
            <span className="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-300">{selectedElement.type}</span>
          </div>
          <div className="text-xs text-slate-300 space-y-0.5">
            <div>Risk Score: <span className="font-bold text-red-400">{selectedElement.risk_score || "N/A"}</span></div>
            {selectedElement.is_ring && <div className="text-red-400 font-semibold">Flagged Fraud Ring Member</div>}
          </div>
        </div>
      )}
    </div>
  );
};
