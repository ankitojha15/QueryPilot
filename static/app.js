// Premium UI logic for QueryPilot.

// Fix Enter key to ask.
document.addEventListener("DOMContentLoaded", () => {
  const box = document.getElementById("q");
  box.addEventListener("keydown", (e) => {
    if (e.key === "Enter") ask();
  });
});

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
  setBadge("");
  showOut("● ● ● thinking...");
  // 1. Check if question needs help.
  const c = await fetch("/clarify?q=" + encodeURIComponent(q)).then((r) => r.json());
  if (c.status === "need_clarification" || c.status === "need_approval") {
    showHelp(c.message, c.options, q);
    showOut("Pick one choice above ⬆");
    return;
  }
  // 2. Clear question goes to query.
  runQuery(q);
}

// Run final SQL query.
async function runQuery(q) {
  setBadge("");
  showOut("● ● ● thinking...");
  const d = await fetch("/query?q=" + encodeURIComponent(q)).then((r) => r.json());
  if (d.cached) setBadge("⚡ cached");
  else if (d.ok) setBadge("✓ fresh");
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
  document.getElementById("q").value = q + " " + choice;
  runQuery(q + " " + choice);
}

// Copy SQL to clipboard.
function copySql() {
  const t = document.getElementById("out").innerText;
  navigator.clipboard.writeText(t);
}

// Show output text in card.
function showOut(text) {
  document.getElementById("ans").classList.remove("hide");
  document.getElementById("out").innerText = text;
  document.getElementById("ans").scrollIntoView({ behavior: "smooth", block: "nearest" });
}

// Show small badge.
function setBadge(text) {
  const b = document.getElementById("badge");
  if (!text) {
    b.classList.add("hide");
    return;
  }
  b.classList.remove("hide");
  b.innerText = text;
}
