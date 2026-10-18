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
            "background-color": "#f1f5f9",
            label: "data(label)",
            color: "#1e293b",
            "font-size": "11px",
            "text-valign": "bottom",
            "text-margin-y": 6,
            width: 36,
            height: 36,
            "border-width": 2,
            "border-color": "#94a3b8",
          },
        },
        {
          selector: 'node[type = "Account"]',
          style: {
            "background-color": "#ffffff",
            "border-color": "#800020",
            "border-width": 2.5,
            shape: "ellipse",
          },
        },
        {
          selector: 'node[type = "Device"]',
          style: {
            "background-color": "#fdf2f4",
            "border-color": "#9c1737",
            "border-width": 2,
            shape: "diamond",
            width: 34,
            height: 34,
          },
        },
        {
          selector: "node[?is_ring]",
          style: {
            "background-color": "#800020",
            "border-color": "#e11d48",
            "border-width": 4,
            color: "#ffffff",
            "font-weight": "bold",
            width: 44,
            height: 44,
          },
        },
        {
          selector: "edge",
          style: {
            width: 2,
            "line-color": "#cbd5e1",
            "target-arrow-color": "#94a3b8",
            "target-arrow-shape": "triangle",
            "curve-style": "bezier",
            label: "data(label)",
            "font-size": "9px",
            color: "#64748b",
            "text-rotation": "autorotate",
            "text-margin-y": -6,
          },
        },
        {
          selector: "edge[?is_ring]",
          style: {
            width: 3,
            "line-color": "#dc2626",
            "target-arrow-color": "#dc2626",
            color: "#991b1b",
          },
        },
      ],
      layout: {
        name: "cose",
        animate: false,
        padding: 40,
        nodeRepulsion: () => 8000,
        idealEdgeLength: () => 90,
      },
    });

    cy.on("tap", "node", (evt) => {
      if (cy.destroyed()) return;
      const nodeData = evt.target.data();
      setSelectedElement(nodeData);
      if (onSelectNode) onSelectNode(nodeData);
    });

    cy.on("tap", (evt) => {
      if (cy.destroyed()) return;
      if (evt.target === cy) {
        setSelectedElement(null);
      }
    });

    cyRef.current = cy;

    return () => {
      try {
        cy.stop();
        cy.destroy();
      } catch {
        // Suppress any late frame renderer notifications during fast-refresh
      }
      cyRef.current = null;
    };
  }, [elements, onSelectNode]);

  const handleZoomIn = () => {
    if (cyRef.current && !cyRef.current.destroyed()) {
      cyRef.current.zoom(cyRef.current.zoom() * 1.25);
    }
  };
  const handleZoomOut = () => {
    if (cyRef.current && !cyRef.current.destroyed()) {
      cyRef.current.zoom(cyRef.current.zoom() * 0.8);
    }
  };
  const handleFit = () => {
    if (cyRef.current && !cyRef.current.destroyed()) {
      cyRef.current.fit();
    }
  };

  return (
    <div className="relative w-full h-full bg-white border border-slate-200 rounded-xl overflow-hidden flex flex-col shadow-sm">
      <div className="absolute top-3 left-3 z-10 flex items-center space-x-2 bg-white/95 backdrop-blur-md px-3.5 py-1.5 rounded-lg border border-slate-200 shadow-sm">
        <Shield className="w-4 h-4 text-maroon-700" />
        <span className="text-xs font-semibold text-slate-800">Fraud Topology Graph</span>
        <span className="text-[11px] text-slate-500 font-mono">({elements.nodes.length} nodes, {elements.edges.length} edges)</span>
      </div>

      <div className="absolute top-3 right-3 z-10 flex space-x-1.5 bg-white/95 backdrop-blur-md p-1 rounded-lg border border-slate-200 shadow-sm">
        <button
          onClick={handleZoomIn}
          title="Zoom In"
          className="p-1.5 hover:bg-slate-100 text-slate-600 hover:text-maroon-800 rounded transition"
        >
          <ZoomIn className="w-4 h-4" />
        </button>
        <button
          onClick={handleZoomOut}
          title="Zoom Out"
          className="p-1.5 hover:bg-slate-100 text-slate-600 hover:text-maroon-800 rounded transition"
        >
          <ZoomOut className="w-4 h-4" />
        </button>
        <button
          onClick={handleFit}
          title="Fit Canvas"
          className="p-1.5 hover:bg-slate-100 text-slate-600 hover:text-maroon-800 rounded transition"
        >
          <Maximize2 className="w-4 h-4" />
        </button>
      </div>

      <div ref={containerRef} className="w-full h-full min-h-[480px]" />

      {selectedElement && (
        <div className="absolute bottom-3 left-3 right-3 z-10 bg-white/95 backdrop-blur-md p-3.5 rounded-lg border border-maroon-200 shadow-xl max-w-md">
          <div className="flex items-center justify-between mb-1.5">
            <span className="text-xs font-bold text-maroon-900 font-mono">{selectedElement.id}</span>
            <span className="text-[11px] px-2 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-200">
              {selectedElement.type}
            </span>
          </div>
          <div className="text-xs text-slate-700 space-y-1">
            <div>
              Risk Score:{" "}
              <span className="font-bold font-mono text-red-600">
                {selectedElement.risk_score !== undefined ? `${(selectedElement.risk_score * 100).toFixed(0)}%` : "N/A"}
              </span>
            </div>
            {selectedElement.is_ring && (
              <div className="text-red-700 font-semibold flex items-center space-x-1">
                <span className="w-2 h-2 rounded-full bg-red-600 animate-pulse inline-block mr-1" />
                <span>Confirmed Laundering Ring Member</span>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
