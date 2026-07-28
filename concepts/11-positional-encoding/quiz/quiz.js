async function hmacHex(keyStr, msgStr) {
  const enc = new TextEncoder();
  const key = await crypto.subtle.importKey(
    "raw", enc.encode(keyStr), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]
  );
  const sig = await crypto.subtle.sign("HMAC", key, enc.encode(msgStr));
  return [...new Uint8Array(sig)].map(b => b.toString(16).padStart(2, "0")).join("");
}

function canonical(answers) {
  // answers: { q01: "b", q02: "a", ... } -> "q01=b;q02=a" sorted by id
  return Object.keys(answers).sort()
    .map(id => `${id}=${answers[id].toLowerCase()}`).join(";");
}

let DATA = null;

async function init() {
  DATA = await (await fetch("questions.json")).json();
  document.getElementById("title").textContent = DATA.title;
  document.getElementById("path").textContent = `progress/${DATA.module_id}.key`;
  const form = document.getElementById("quiz");
  for (const q of DATA.questions) {
    const fs = document.createElement("fieldset");
    fs.innerHTML = `<legend>${q.text}</legend>`;
    for (const [letter, label] of Object.entries(q.options)) {
      const id = `${q.id}_${letter}`;
      fs.insertAdjacentHTML("beforeend",
        `<label><input type="radio" name="${q.id}" value="${letter}" id="${id}"> ${label}</label>`);
    }
    form.appendChild(fs);
  }
  document.getElementById("submit").addEventListener("click", onSubmit);
  document.getElementById("copy").addEventListener("click", () => {
    navigator.clipboard.writeText(document.getElementById("shard").textContent);
  });
}

async function onSubmit() {
  const handle = document.getElementById("handle").value.trim().toLowerCase();
  if (!/^[a-z0-9_-]+$/.test(handle)) { alert("Invalid handle. Use a-z, 0-9, _ or -."); return; }
  const answers = {};
  for (const q of DATA.questions) {
    const sel = document.querySelector(`input[name="${q.id}"]:checked`);
    if (!sel) { alert("Answer every question first."); return; }
    answers[q.id] = sel.value;
  }
  const canon = canonical(answers);
  const msg = `${handle}|${DATA.module_id}|${canon}`;
  const hex = (await hmacHex(DATA.salt, msg)).slice(0, 12).toUpperCase();
  const line = `${handle}:${DATA.course_prefix || "DLX"}-${DATA.module_id}-${hex}`;
  document.getElementById("shard").textContent = line;
  document.getElementById("result").hidden = false;
}

init();
