// Plain UI logic for QueryPilot.

// Saved login token. Empty means logged out.
let TOKEN = "";

// Enter key submits the right box.
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

// Login with name and password.
async function doLogin() {
  const name = document.getElementById("name").value.trim();
  const pw = document.getElementById("pw").value;
  const d = await fetch("/login?name=" + encodeURIComponent(name) + "&password=" + encodeURIComponent(pw)).then((r) => r.json());
  const who = document.getElementById("who");
  if (d.ok) {
    TOKEN = d.token;
    who.innerText = "Signed in as " + name + ". You can ask now.";
  } else {
    TOKEN = "";
    who.innerText = "Sign in failed: " + d.message;
  }
}

// Ask question to API.
async function ask(extra) {
  let q = document.getElementById("q").value.trim();
  if (!q) return;
  if (extra) q = q + " " + extra;
  setBadge("");
  showLoading();
  // 1. Check if question needs help.
  const c = await fetch("/clarify?q=" + encodeURIComponent(q)).then((r) => r.json());
  // 2. Destructive request is blocked, no SQL runs.
  if (c.status === "blocked") {
    const box = document.getElementById("help");
    box.classList.remove("hide");
    box.innerHTML = "<b>Refused.</b> " + c.message;
    showOut("Q: " + q + "\n\nRefused: no SQL was run.");
    return;
  }
  if (c.status === "need_clarification" || c.status === "need_approval") {
    showHelp(c.message, c.options, q);
    showOut("Q: " + q + "\n\nPlease pick one choice above.");
    return;
  }
  // 3. Clear question goes to query.
  runQuery(q);
}

// Run final SQL query. Shows clean SQL plus rows.
async function runQuery(q, approved) {
  if (!TOKEN) {
    showOut("Q: " + q + "\n\nPlease sign in first.");
    return;
  }
  setBadge("");
  showLoading();
  let url = "/query?q=" + encodeURIComponent(q) + "&token=" + TOKEN;
  if (approved) url += "&approved=yes";
  const d = await fetch(url).then((r) => r.json());
  if (d.ok === false) {
    showOut("Q: " + q + "\n\n" + (d.message || "Please sign in first."));
    return;
  }
  if (d.cached) setBadge("cached");
  else setBadge("fresh");
  showOut("Q: " + q + "\n\n" + pickSql(d) + rowsText(d));
}

// Make rows into plain text table.
function rowsText(d) {
  if (!d.cols) return "";
  if (!d.rows.length) return "\n\nRows: none.";
  const lines = d.rows.map((r) => r.join(" | "));
  return "\n\nRows (" + d.rows.length + "):\n" + d.cols.join(" | ") + "\n" + lines.join("\n");
}

// Pick only the SQL part from the answer.
function pickSql(d) {
  let t = "";
  if (d.sql) t = d.sql;
  else if (d.result) {
    const m = d.result.match(/SELECT[\s\S]*?;/);
    t = m ? m[0] : d.result;
  }
  // Cached text keeps newlines as characters, turn them back.
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

// Ask again with user choice. Yes-run sends approval, cancel stops.
function askChoice(q, choice) {
  document.getElementById("help").classList.add("hide");
  if (choice === "cancel") {
    showOut("Q: " + q + "\n\nCancelled.");
    return;
  }
  if (choice === "yes-run") {
    runQuery(q, true);
    return;
  }
  document.getElementById("q").value = q + " " + choice;
}

// Copy SQL to clipboard.
function copySql() {
  const t = document.getElementById("out").innerText;
  navigator.clipboard.writeText(t);
  const b = document.querySelector(".copy");
  b.innerText = "Copied";
  setTimeout(() => (b.innerText = "Copy"), 1500);
}

// Show skeleton bars while waiting.
function showLoading() {
  document.getElementById("ans").classList.remove("hide");
  document.getElementById("out").innerHTML = '<span class="sk"></span><span class="sk"></span><span class="sk"></span>';
}

// Show output text.
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

// Show short site notes for Privacy and Terms.
function showLegal(which) {
  const box = document.getElementById("legal");
  box.classList.remove("hide");
  if (which === "privacy") {
    box.innerText = "Privacy: demo logins only (amit, neha, ravi). Questions are sent to the SQL API and cached for 5 minutes. No tracking, no analytics.";
  } else {
    box.innerText = "Terms: demo project for learning. Only safe SELECT queries run. Destructive requests are refused. Sample data only.";
  }
}
