// Premium UI logic for QueryPilot.

// Fix Enter key + rotating hint text.
document.addEventListener("DOMContentLoaded", () => {
  const box = document.getElementById("q");
  box.addEventListener("keydown", (e) => {
    if (e.key === "Enter") ask();
  });
  // Rotate placeholder for creative touch.
  const hints = [
    "Ask question...",
    "Try: last 30 days city-wise orders?...",
    "Try: where are my orders?...",
    "Try: show paid orders?...",
  ];
  let i = 0;
  setInterval(() => {
    if (!box.value) box.placeholder = hints[i++ % hints.length];
  }, 3000);
});

// Fill input on example click.
// Saved login token. Empty means logged out.
let TOKEN = "";

// Login with name and password.
async function doLogin() {
  const name = document.getElementById("name").value.trim();
  const pw = document.getElementById("pw").value;
  const d = await fetch("/login?name=" + encodeURIComponent(name) + "&password=" + encodeURIComponent(pw)).then((r) => r.json());
  const who = document.getElementById("who");
  if (d.ok) {
    TOKEN = d.token;
    who.innerText = "Logged in: " + name + " (ask now)";
  } else {
    TOKEN = "";
    who.innerText = "Login failed: " + d.message;
  }
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
  // 0. Destructive request is blocked, no SQL runs.
  if (c.status === "blocked") {
    const box = document.getElementById("help");
    box.classList.remove("hide");
    box.innerHTML = "<b>⛔ " + c.message + "</b>";
    showOut("Q: " + q + "\n\nBlocked: no SQL run.");
    return;
  }
  if (c.status === "need_clarification" || c.status === "need_approval") {
    showHelp(c.message, c.options, q);
    showOut("Pick one choice above ⬆");
    return;
  }
  // 2. Clear question goes to query.
  runQuery(q);
}

// Run final SQL query. Shows only clean SQL, hides ok flag.
// Run final SQL query. Shows only clean SQL, hides ok flag.
async function runQuery(q) {
  if (!TOKEN) {
    showOut("Q: " + q + "\n\nPlease login first.");
    return;
  }
  setBadge("");
  showOut("Q: " + q + "\n\n● ● ● thinking...");
  const d = await fetch("/query?q=" + encodeURIComponent(q) + "&token=" + TOKEN).then((r) => r.json());
  if (d.ok === false) {
    showOut("Q: " + q + "\n\n" + (d.message || "login first"));
    return;
  }
  if (d.cached) setBadge("⚡ cached");
  else setBadge("✓ fresh");
  const sql = pickSql(d);
  showOut("Q: " + q + "\n\n" + sql);
}

// Pick only SQL part. Hides question and ok flag.
// Pick only SQL part. Hides question and ok flag.
function pickSql(d) {
  let t = "";
  if (d.sql) t = d.sql;
  else if (d.result) {
    const m = d.result.match(/SELECT[\s\S]*?;/);
    t = m ? m[0] : d.result;
  }
  // Cached text has \n as letters, make them real lines.
  return t.replace(/\\n/g, "\n").replace(/\\"/g, '"').replace(/\\'/g, "'");
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

// Copy SQL to clipboard with tick.
function copySql() {
  const t = document.getElementById("out").innerText;
  navigator.clipboard.writeText(t);
  const b = document.querySelector(".copy");
  b.innerText = "Copied ✓";
  setTimeout(() => (b.innerText = "Copy"), 1500);
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
