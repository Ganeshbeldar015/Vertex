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
            "background-color": "#181822",
            label: "data(label)",
            color: "#f3f4f6",
            "font-size": "11px",
            "text-valign": "bottom",
            "text-margin-y": 6,
            width: 36,
            height: 36,
            "border-width": 2,
            "border-color": "#3b000d",
          },
        },
        {
          selector: 'node[type = "Account"]',
          style: {
            "background-color": "#1c1c28",
            "border-color": "#800020",
            "border-width": 2.5,
            shape: "ellipse",
          },
        },
        {
          selector: 'node[type = "Device"]',
          style: {
            "background-color": "#3b000d",
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
            "border-color": "#ff4d6d",
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
            "line-color": "#2a2a3a",
            "target-arrow-color": "#2a2a3a",
            "target-arrow-shape": "triangle",
            "curve-style": "bezier",
            label: "data(label)",
            "font-size": "9px",
            color: "#9ca3af",
            "text-rotation": "autorotate",
            "text-margin-y": -6,
          },
        },
        {
          selector: "edge[?is_ring]",
          style: {
            width: 3,
            "line-color": "#e11d48",
            "target-arrow-color": "#e11d48",
            color: "#ff758f",
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
    <div className="relative w-full h-full bg-obsidian-950 border border-maroon-900/40 rounded-xl overflow-hidden flex flex-col shadow-xl">
      <div className="absolute top-3 left-3 z-10 flex items-center space-x-2 bg-obsidian-900/90 backdrop-blur-md px-3.5 py-1.5 rounded-lg border border-maroon-800/40 shadow-maroon-subtle">
        <Shield className="w-4 h-4 text-rose-400" />
        <span className="text-xs font-semibold text-slate-200">Fraud Topology Graph</span>
        <span className="text-[11px] text-slate-400 font-mono">({elements.nodes.length} nodes, {elements.edges.length} edges)</span>
      </div>

      <div className="absolute top-3 right-3 z-10 flex space-x-1.5 bg-obsidian-900/90 backdrop-blur-md p-1 rounded-lg border border-maroon-800/40">
        <button
          onClick={handleZoomIn}
          title="Zoom In"
          className="p-1.5 hover:bg-maroon-950 text-slate-300 hover:text-rose-200 rounded transition"
        >
          <ZoomIn className="w-4 h-4" />
        </button>
        <button
          onClick={handleZoomOut}
          title="Zoom Out"
          className="p-1.5 hover:bg-maroon-950 text-slate-300 hover:text-rose-200 rounded transition"
        >
          <ZoomOut className="w-4 h-4" />
        </button>
        <button
          onClick={handleFit}
          title="Fit Canvas"
          className="p-1.5 hover:bg-maroon-950 text-slate-300 hover:text-rose-200 rounded transition"
        >
          <Maximize2 className="w-4 h-4" />
        </button>
      </div>

      <div ref={containerRef} className="w-full h-full min-h-[480px]" />

      {selectedElement && (
        <div className="absolute bottom-3 left-3 right-3 z-10 bg-obsidian-900/95 backdrop-blur-md p-3.5 rounded-lg border border-maroon-600/70 shadow-maroon-glow max-w-md">
          <div className="flex items-center justify-between mb-1.5">
            <span className="text-xs font-bold text-rose-300 font-mono">{selectedElement.id}</span>
            <span className="text-[11px] px-2 py-0.5 rounded bg-obsidian-950 text-slate-300 border border-maroon-900/50">
              {selectedElement.type}
            </span>
          </div>
          <div className="text-xs text-slate-300 space-y-1">
            <div>
              Risk Score:{" "}
              <span className="font-bold font-mono text-rose-400">
                {selectedElement.risk_score !== undefined ? `${(selectedElement.risk_score * 100).toFixed(0)}%` : "N/A"}
              </span>
            </div>
            {selectedElement.is_ring && (
              <div className="text-rose-400 font-semibold flex items-center space-x-1">
                <span className="w-2 h-2 rounded-full bg-rose-500 animate-pulse inline-block mr-1" />
                <span>Confirmed Laundering Ring Member</span>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
