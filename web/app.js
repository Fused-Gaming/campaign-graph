let cy;
const statusStyles = { DOCUMENTED: { lineStyle: "solid", opacity: 1 }, INFERRED: { lineStyle: "dashed", opacity: 0.75 }, UNRESOLVED: { lineStyle: "dotted", opacity: 0.6 }, CONTRADICTED: { lineStyle: "dashed", opacity: 0.45 } };
async function loadMetrics() {
  const metrics = await fetch("/api/metrics").then(r => r.json());
  document.querySelector("#metrics").innerHTML = Object.entries(metrics).map(([k,v]) => `<div class="metric"><b>${v}</b><span>${k.replaceAll("_"," ")}</span></div>`).join("");
}
async function loadGraph() {
  const view = document.querySelector("#view").value;
  const selectedStatus = document.querySelector("#status").value;
  const payload = await fetch(`/api/graph?view=${view}`).then(r => r.json());
  let elements = payload.elements;
  if (selectedStatus) {
    const edges = elements.edges.filter(e => e.data.verification_status === selectedStatus);
    const ids = new Set(edges.flatMap(e => [e.data.source, e.data.target]));
    elements = { nodes: elements.nodes.filter(n => ids.has(n.data.id)), edges };
  }
  if (cy) cy.destroy();
  cy = cytoscape({ container: document.getElementById("cy"), elements, style: [
    { selector: "node", style: { "label": "data(label)", "font-size": 10, "text-wrap": "wrap", "text-max-width": 100, "background-color": "#65718a", "color": "#f3f5f7", "text-outline-color": "#090b10", "text-outline-width": 2, "width": 32, "height": 32 } },
    { selector: "edge", style: { "curve-style": "bezier", "target-arrow-shape": "triangle", "arrow-scale": 0.8, "width": 2, "label": "data(type)", "font-size": 8, "text-rotation": "autorotate", "text-margin-y": -7, "line-color": "#697386", "target-arrow-color": "#697386", "color": "#c7ced9" } }
  ], layout: { name: "cose", animate: false, nodeRepulsion: 8000 } });
  cy.edges().forEach(edge => { const s = statusStyles[edge.data("verification_status")] || statusStyles.UNRESOLVED; edge.style("line-style", s.lineStyle); edge.style("opacity", s.opacity); });
  cy.on("tap", "edge", evt => renderEdge(evt.target.data()));
}
function renderEdge(d) {
  const ev = (d.evidence || [])[0] || {};
  document.querySelector("#details").innerHTML = `<h2>${d.type}</h2><p><strong>Status:</strong> ${d.verification_status || ""}</p><p><strong>Confidence:</strong> ${d.confidence || ""}</p><p><strong>Date:</strong> ${d.date || "—"}</p><p><strong>Amount:</strong> ${d.amount == null ? "—" : `${d.currency || ""} ${d.amount}`}</p><p><strong>Description:</strong><br>${escapeHtml(d.description || "")}</p><p><strong>Source:</strong><br>${ev.source_title ? escapeHtml(ev.source_title) : "—"}</p>${d.source_url ? `<p><a href="${encodeURI(d.source_url)}" target="_blank" rel="noreferrer">Open record ↗</a></p>` : ""}<details><summary>Raw edge record</summary><pre>${escapeHtml(JSON.stringify(d, null, 2))}</pre></details>`;
}
function escapeHtml(value) { return String(value).replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;").replaceAll('"',"&quot;"); }
document.querySelector("#view").addEventListener("change", loadGraph);
document.querySelector("#status").addEventListener("change", loadGraph);
loadMetrics(); loadGraph();
