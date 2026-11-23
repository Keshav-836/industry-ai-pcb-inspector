// Step 3: test photos upload karna aur har photo ka result dikhana
(function () {
  const MAX_FILES = 10;

  const input = document.getElementById("test-input");
  const drop = document.getElementById("test-drop");
  const filesBox = document.getElementById("test-files");
  const runBtn = document.getElementById("test-run");
  const clearBtn = document.getElementById("test-clear");
  const summary = document.getElementById("results-summary");
  const results = document.getElementById("results");
  const boardName = document.getElementById("inspect-board-name");
  const partCount = document.getElementById("inspect-part-count");

  let files = [];
  let lastBoardId = null;

  // ---------- photos chunna ----------

  function addFiles(list) {
    const images = Array.from(list).filter((f) => f.type.startsWith("image/"));
    if (files.length + images.length > MAX_FILES) {
      App.toast(`You can check up to ${MAX_FILES} photos at once`);
    }
    files = files.concat(images).slice(0, MAX_FILES);
    renderFiles();
  }

  function renderFiles() {
    filesBox.innerHTML = "";
    files.forEach((file, i) => {
      const chip = document.createElement("div");
      chip.className = "file-chip";

      const thumb = document.createElement("img");
      thumb.src = URL.createObjectURL(file);
      thumb.alt = file.name;

      const name = document.createElement("span");
      name.textContent = file.name;

      const remove = document.createElement("button");
      remove.type = "button";
      remove.className = "btn-link";
      remove.textContent = "Remove";
      remove.addEventListener("click", () => {
        files.splice(i, 1);
        renderFiles();
      });

      chip.append(thumb, name, remove);
      filesBox.appendChild(chip);
    });

    runBtn.disabled = files.length === 0;
    runBtn.textContent = files.length > 1 ? `Check ${files.length} photos` : "Check photo";
  }

  input.addEventListener("change", () => {
    addFiles(input.files);
    // value khaali karo taaki wahi photo dobara bhi chun sakein
    input.value = "";
  });

  App.setupDropzone(drop, addFiles);

  clearBtn.addEventListener("click", () => {
    files = [];
    renderFiles();
    results.innerHTML = "";
    summary.classList.add("hidden");
  });

  // ---------- result dikhana ----------

  function el(tag, className, text) {
    // chhota helper: element banao, class aur text ek line me
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function scoresTable(parts) {
    // "Part scores" - interview me samjhane ke liye ki app ne kyu decide kiya
    const details = el("details", "scores");
    details.appendChild(el("summary", "", "Part scores"));

    const table = el("table");
    const head = el("tr");
    ["Part", "Result", "Score"].forEach((h) => head.appendChild(el("th", "", h)));
    table.appendChild(head);

    parts.forEach((p) => {
      const row = el("tr");
      row.appendChild(el("td", "", p.name));
      row.appendChild(el("td", p.missing ? "text-bad" : "text-ok", p.missing ? "Missing" : "Present"));
      row.appendChild(el("td", "", p.score.toFixed(2)));
      table.appendChild(row);
    });

    details.appendChild(table);
    details.appendChild(el("p", "scores-note", "Score above 0.35 means the part is missing."));
    return details;
  }

  function resultCard(r) {
    const isOk = r.status === "OK";
    const card = el("div", `result-card ${r.error ? "is-error" : isOk ? "is-ok" : "is-bad"}`);

    // upar: file ka naam + OK/MISSING badge
    const head = el("div", "result-head");
    head.appendChild(el("strong", "", r.filename));
    if (!r.error) {
      head.appendChild(el("span", `badge ${isOk ? "badge-ok" : "badge-bad"}`, isOk ? "OK" : "MISSING"));
    }
    card.appendChild(head);

    // photo kharab thi to sirf error dikhao
    if (r.error) {
      card.appendChild(el("p", "result-error", r.error));
      return card;
    }

    const body = el("div", "result-body");

    const img = el("img", "result-img");
    img.src = r.image;
    img.alt = `Result for ${r.filename}`;
    body.appendChild(img);

    const side = el("div", "result-side");
    if (isOk) {
      side.appendChild(el("div", "big-status big-ok", "OK"));
      side.appendChild(el("p", "muted", `All ${r.parts.length} parts present`));
    } else {
      const count = r.missing_parts.length;
      side.appendChild(el("div", "big-status big-bad", "MISSING"));
      side.appendChild(el("p", "muted", `${count} ${count === 1 ? "part" : "parts"} missing`));
      const chips = el("div", "missing-chips");
      r.missing_parts.forEach((name) => chips.appendChild(el("span", "chip-bad", name)));
      side.appendChild(chips);
    }

    // alignment fail hua to user ko saaf bata do
    if (r.warning) {
      side.appendChild(el("p", "warning", r.warning));
    }

    side.appendChild(scoresTable(r.parts));
    body.appendChild(side);
    card.appendChild(body);
    return card;
  }

  function renderResults(list) {
    results.innerHTML = "";
    const ok = list.filter((r) => r.status === "OK").length;
    const bad = list.filter((r) => r.status === "MISSING").length;
    const failed = list.filter((r) => r.error).length;

    let text = `${list.length} ${list.length === 1 ? "photo" : "photos"} checked: ${ok} OK, ${bad} with missing parts`;
    if (failed) text += `, ${failed} could not be read`;
    summary.textContent = text;
    summary.classList.remove("hidden");

    list.forEach((r) => results.appendChild(resultCard(r)));
    summary.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  runBtn.addEventListener("click", async () => {
    if (!files.length) return;
    const label = runBtn.textContent;
    runBtn.disabled = true;
    runBtn.textContent = "Checking...";
    try {
      const data = await Api.inspect(App.board.id, files);
      renderResults(data.results);
    } catch (err) {
      App.toast(err.message);
    } finally {
      runBtn.disabled = false;
      runBtn.textContent = label;
    }
  });

  // jab Step 3 khule: board ka naam dikhao, board badla ho to purane result hatao
  document.addEventListener("step:enter", (e) => {
    if (e.detail !== 3) return;
    boardName.textContent = App.board.name;
    partCount.textContent = App.board.parts.length;

    if (lastBoardId !== App.board.id) {
      lastBoardId = App.board.id;
      results.innerHTML = "";
      summary.classList.add("hidden");
    }
  });
})();