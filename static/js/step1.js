// Step 1: reference photo upload karna ya purana board kholna
(function () {
  const input = document.getElementById("ref-input");
  const drop = document.getElementById("ref-drop");
  const preview = document.getElementById("ref-preview");
  const dropText = document.getElementById("ref-drop-text");
  const nameInput = document.getElementById("board-name");
  const saveBtn = document.getElementById("ref-save");
  const list = document.getElementById("board-list");

  let chosenFile = null;

  function showPreview(file) {
    chosenFile = file;
    preview.src = URL.createObjectURL(file);
    preview.classList.remove("hidden");
    dropText.classList.add("hidden");
    saveBtn.disabled = false;
  }

  input.addEventListener("change", () => {
    if (input.files[0]) showPreview(input.files[0]);
  });

  // drag and drop - photo ko seedha box me chhod sakte hain
  ["dragenter", "dragover"].forEach((evt) => {
    drop.addEventListener(evt, (e) => {
      e.preventDefault();
      drop.classList.add("dragging");
    });
  });
  ["dragleave", "drop"].forEach((evt) => {
    drop.addEventListener(evt, (e) => {
      e.preventDefault();
      drop.classList.remove("dragging");
    });
  });
  drop.addEventListener("drop", (e) => {
    const file = e.dataTransfer.files[0];
    if (file) showPreview(file);
  });

  saveBtn.addEventListener("click", async () => {
    saveBtn.disabled = true;
    saveBtn.textContent = "Saving...";
    try {
      const board = await Api.createBoard(chosenFile, nameInput.value);
      App.setBoard(board);
      App.goToStep(2);
      loadBoards();
    } catch (err) {
      App.toast(err.message);
    } finally {
      saveBtn.disabled = false;
      saveBtn.textContent = "Use this photo";
    }
  });

  function boardCard(board) {
    // textContent use karte hain, innerHTML nahi - naam me HTML ho to bhi safe
    const card = document.createElement("button");
    card.type = "button";
    card.className = "board-card";

    const img = document.createElement("img");
    img.src = Api.referenceUrl(board.id);
    img.alt = board.name;

    const info = document.createElement("div");
    info.className = "board-info";
    const title = document.createElement("strong");
    title.textContent = board.name;
    const meta = document.createElement("span");
    meta.textContent = `${board.parts.length} parts named`;
    info.append(title, meta);

    card.append(img, info);

    // parts pehle se named hain to seedha Step 3, warna Step 2
    card.addEventListener("click", () => {
      App.setBoard(board);
      App.goToStep(board.parts.length ? 3 : 2);
    });
    return card;
  }

  async function loadBoards() {
    try {
      const boards = await Api.listBoards();
      list.innerHTML = "";
      if (!boards.length) {
        list.innerHTML = '<p class="empty">No saved boards yet.</p>';
        return;
      }
      boards.forEach((board) => list.appendChild(boardCard(board)));
    } catch (err) {
      App.toast(err.message);
    }
  }

  loadBoards();
})();