// Step 2: reference photo pe mouse se box bana ke parts ka naam dena
(function () {
  const img = document.getElementById("editor-img");
  const canvas = document.getElementById("editor-canvas");
  const ctx = canvas.getContext("2d");
  const list = document.getElementById("parts-list");
  const countEl = document.getElementById("parts-count");
  const saveBtn = document.getElementById("parts-save");
  const clearBtn = document.getElementById("parts-clear");

  // parts hamesha ASLI photo ke pixels me store hote hain, screen ke nahi
  let parts = [];
  let drawing = null; // abhi jo box ban raha hai (screen pixels me)
  let hovered = -1; // list me jis part pe mouse hai

  // asli photo screen pe kitni chhoti/badi dikh rahi hai
  // jaise photo 1448px ki hai aur screen pe 800px dikh rahi to scale = 1.81
  function scale() {
    return img.naturalWidth / img.clientWidth;
  }

  // mouse ke start aur end point se seedha box banao (ulta drag bhi chale)
  function rectFrom(d) {
    return {
      x: Math.min(d.x1, d.x2),
      y: Math.min(d.y1, d.y2),
      w: Math.abs(d.x2 - d.x1),
      h: Math.abs(d.y2 - d.y1),
    };
  }

  // canvas ka size bilkul photo jitna rakho
  function resizeCanvas() {
    canvas.width = img.clientWidth;
    canvas.height = img.clientHeight;
    draw();
  }

  function drawLabel(text, x, y, color) {
    ctx.font = "600 12px Segoe UI, sans-serif";
    const width = ctx.measureText(text).width + 10;
    const top = Math.max(0, y - 18);
    ctx.fillStyle = color;
    ctx.fillRect(x, top, width, 18);
    ctx.fillStyle = "#fff";
    ctx.fillText(text, x + 5, top + 13);
  }

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const s = scale();

    parts.forEach((p, i) => {
      // asli pixels ko screen pixels me badlo
      const x = p.x / s;
      const y = p.y / s;
      const w = p.w / s;
      const h = p.h / s;
      const active = i === hovered;
      const color = active ? "#f59e0b" : "#1f6feb";

      ctx.lineWidth = active ? 3 : 2;
      ctx.strokeStyle = color;
      ctx.fillStyle = active ? "rgba(245, 158, 11, 0.18)" : "rgba(31, 111, 235, 0.10)";
      ctx.fillRect(x, y, w, h);
      ctx.strokeRect(x, y, w, h);
      drawLabel(p.name || "(no name)", x, y, color);
    });

    // jo box abhi drag ho raha hai usko dotted line se dikhao
    if (drawing) {
      const r = rectFrom(drawing);
      ctx.setLineDash([6, 4]);
      ctx.strokeStyle = "#1f6feb";
      ctx.lineWidth = 2;
      ctx.strokeRect(r.x, r.y, r.w, r.h);
      ctx.setLineDash([]);
    }
  }

  // mouse ki position canvas ke hisaab se, aur canvas ke bahar na jaye
  function pointer(e) {
    const rect = canvas.getBoundingClientRect();
    return {
      x: Math.max(0, Math.min(e.clientX - rect.left, canvas.width)),
      y: Math.max(0, Math.min(e.clientY - rect.top, canvas.height)),
    };
  }

  // "Part 1", "Part 2"... aisa naam jo pehle se use na hua ho
  function nextName() {
    const used = new Set(parts.map((p) => p.name.toLowerCase()));
    let n = parts.length + 1;
    while (used.has(`part ${n}`)) n += 1;
    return `Part ${n}`;
  }

  canvas.addEventListener("mousedown", (e) => {
    const p = pointer(e);
    drawing = { x1: p.x, y1: p.y, x2: p.x, y2: p.y };
  });

  // window pe sunte hain taaki mouse canvas se bahar jaye tab bhi chale
  window.addEventListener("mousemove", (e) => {
    if (!drawing) return;
    const p = pointer(e);
    drawing.x2 = p.x;
    drawing.y2 = p.y;
    draw();
  });

  window.addEventListener("mouseup", () => {
    if (!drawing) return;
    const r = rectFrom(drawing);
    drawing = null;
    const s = scale();

    // bahut chhota box matlab galti se click - ignore karo
    if (r.w * s < 8 || r.h * s < 8) {
      draw();
      return;
    }

    parts.push({
      name: nextName(),
      x: Math.round(r.x * s),
      y: Math.round(r.y * s),
      w: Math.round(r.w * s),
      h: Math.round(r.h * s),
    });
    renderList();
    draw();

    // naye part ke naam wale box me cursor daal do - seedha type karo
    const inputs = list.querySelectorAll("input");
    const last = inputs[inputs.length - 1];
    last.focus();
    last.select();
  });

  function renderList() {
    list.innerHTML = "";
    countEl.textContent = parts.length;

    if (!parts.length) {
      list.innerHTML = '<p class="empty">No parts yet. Drag on the photo to draw the first box.</p>';
      return;
    }

    parts.forEach((part, i) => {
      const row = document.createElement("div");
      row.className = "part-row";

      const num = document.createElement("span");
      num.className = "part-num";
      num.textContent = i + 1;

      const input = document.createElement("input");
      input.className = "input input-sm";
      input.value = part.name;
      input.placeholder = "Part name";
      input.addEventListener("input", () => {
        part.name = input.value;
        draw();
      });
      // Enter dabane pe typing khatam
      input.addEventListener("keydown", (e) => {
        if (e.key === "Enter") input.blur();
      });

      const remove = document.createElement("button");
      remove.type = "button";
      remove.className = "btn-link";
      remove.textContent = "Remove";
      remove.addEventListener("click", () => {
        parts.splice(i, 1);
        hovered = -1;
        renderList();
        draw();
      });

      // list ki row pe mouse = photo pe wahi box orange
      row.addEventListener("mouseenter", () => {
        hovered = i;
        draw();
      });
      row.addEventListener("mouseleave", () => {
        hovered = -1;
        draw();
      });

      row.append(num, input, remove);
      list.appendChild(row);
    });
  }

  clearBtn.addEventListener("click", () => {
    if (!parts.length) return;
    if (!confirm("Remove all boxes?")) return;
    parts = [];
    renderList();
    draw();
  });

  saveBtn.addEventListener("click", async () => {
    if (!parts.length) {
      App.toast("Draw at least one part first");
      return;
    }
    saveBtn.disabled = true;
    saveBtn.textContent = "Saving...";
    try {
      const board = await Api.saveParts(App.board.id, parts);
      App.setBoard(board);
      App.toast(`${board.parts.length} parts saved`, "success");
      App.goToStep(3);
    } catch (err) {
      // jaise do parts ka same naam - server ka message dikhao
      App.toast(err.message);
    } finally {
      saveBtn.disabled = false;
      saveBtn.textContent = "Save and continue";
    }
  });

  // jab Step 2 khule: board ki photo aur pehle se bane parts load karo
  document.addEventListener("step:enter", (e) => {
    if (e.detail !== 2) return;

    // copy banate hain taaki Save se pehle asli board na badle
    parts = App.board.parts.map((p) => ({ ...p }));
    renderList();

    const url = Api.referenceUrl(App.board.id);
    if (img.getAttribute("src") === url && img.complete) {
      resizeCanvas();
    } else {
      img.onload = resizeCanvas;
      img.src = url;
    }
  });

  // window ka size badle to boxes sahi jagah pe rahein
  window.addEventListener("resize", () => {
    if (img.complete && img.naturalWidth) resizeCanvas();
  });
})();