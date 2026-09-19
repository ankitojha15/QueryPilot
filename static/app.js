// Simple UI logic for QueryPilot.

// Fill input on example click.
function fill(text) {
  document.getElementById("q").value = text;
  ask();
}

// Ask question to API.
async function ask(extra) {
  let q = document.getElementById("q").value.trim();
  if (!q) return;
  if (extra) q = q + " " + extra;
  showOut("Loading...");
  // 1. Check if question needs help.
  const c = await fetch("/clarify?q=" + encodeURIComponent(q)).then((r) => r.json());
  if (c.status === "need_clarification" || c.status === "need_approval") {
    showHelp(c.message, c.options, q);
    showOut("Need your choice above.");
    return;
  }
  // 2. Clear question goes to query.
  runQuery(q);
}

// Run final SQL query.
async function runQuery(q) {
  showOut("Loading...");
  const d = await fetch("/query?q=" + encodeURIComponent(q)).then((r) => r.json());
  const sql = d.sql || d.result || JSON.stringify(d);
  showOut(sql);
}

// Show help buttons.
function showHelp(msg, opts, q) {
  const box = document.getElementById("help");
  box.classList.remove("hide");
  box.innerHTML = "<b>" + msg + "</b><br>";
  opts.forEach((o) => {
    const b = document.createElement("button");
    b.className = "ex opt";
    b.innerText = o;
    b.onclick = () => askChoice(q, o);
    box.appendChild(b);
  });
}

// Ask again with user choice.
function askChoice(q, choice) {
  document.getElementById("help").classList.add("hide");
  runQuery(q + " " + choice);
}

// Show output text.
function showOut(text) {
  const out = document.getElementById("out");
  out.classList.remove("hide");
  out.innerText = text;
}
