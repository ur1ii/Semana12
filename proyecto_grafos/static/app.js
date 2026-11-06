// Cliente: consume los endpoints Flask con fetch y actualiza la interfaz.
const $ = (id) => document.getElementById(id);

const chip = (texto, color) =>
  `<span class="inline-block ${color} text-white rounded px-2 py-1 mr-1 mb-1">${texto}</span>`;

const escapar = (t) => t.replace(/[&<>"']/g, (c) =>
  ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

function mostrarMensaje(el, texto, ok) {
  el.textContent = texto;
  el.className = "text-sm mt-3 " + (ok ? "text-emerald-700" : "text-red-600");
}

// GET /api/grafo -> lista de adyacencia + selects
async function cargarGrafo() {
  const r = await fetch("/api/grafo");
  const { adyacencia } = await r.json();
  const nodos = Object.keys(adyacencia);

  $("lista").innerHTML = nodos.map((n) =>
    `<li><b>${escapar(n)}</b> → [${adyacencia[n].map(escapar).join(", ")}]</li>`).join("");

  const opciones = nodos.map((n) => `<option value="${escapar(n)}">${escapar(n)}</option>`).join("");
  for (const id of ["ruta-origen", "ruta-destino", "dfs-inicio"]) {
    const valor = $(id).value;
    $(id).innerHTML = opciones;
    if (nodos.includes(valor)) $(id).value = valor;
  }
}

// POST /api/conexiones
async function agregarConexion() {
  const origen = $("con-origen").value, destino = $("con-destino").value;
  const r = await fetch("/api/conexiones", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ origen, destino }),
  });
  const datos = await r.json();
  mostrarMensaje($("msg-conexion"), datos.mensaje || datos.error, r.ok);
  if (r.ok) {
    $("con-origen").value = $("con-destino").value = "";
    cargarGrafo();
  }
}

// GET /api/ruta?origen=A&destino=B
async function calcularRuta() {
  const q = new URLSearchParams({ origen: $("ruta-origen").value, destino: $("ruta-destino").value });
  const r = await fetch("/api/ruta?" + q);
  const d = await r.json();
  if (!r.ok) return ($("res-ruta").innerHTML = `<p class="text-red-600">${escapar(d.error)}</p>`);
  if (!d.existe) return ($("res-ruta").innerHTML = `<p class="text-red-600 font-semibold">${escapar(d.mensaje)}</p>`);
  $("res-ruta").innerHTML =
    `<p class="mb-2">Ruta con ${d.pasos} paso(s):</p>` +
    d.ruta.map((n, i) => chip(escapar(n), "bg-emerald-600") + (i < d.ruta.length - 1 ? "→ " : "")).join("");
}

// GET /api/recorrido?inicio=A
async function recorrerDFS() {
  const q = new URLSearchParams({ inicio: $("dfs-inicio").value });
  const r = await fetch("/api/recorrido?" + q);
  const d = await r.json();
  if (!r.ok) return ($("res-dfs").innerHTML = `<p class="text-red-600">${escapar(d.error)}</p>`);
  $("res-dfs").innerHTML = d.recorrido.map((n, i) => chip(`${i + 1}. ${escapar(n)}`, "bg-amber-600")).join("");
}

$("btn-conexion").addEventListener("click", agregarConexion);
$("btn-ruta").addEventListener("click", calcularRuta);
$("btn-dfs").addEventListener("click", recorrerDFS);
cargarGrafo();