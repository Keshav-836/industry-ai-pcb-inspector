// app ki shared state aur step switching - baaki saari files App use karti hain
const App = {
  board: null,
  current: 1,

  setBoard(board) {
    this.board = board;
    this.refreshStepper();
  },

  // kaunsa step khul sakta hai - galat order me kaam na ho
  canOpen(step) {
    if (step === 1) return true;
    if (step === 2) return Boolean(this.board);
    if (step === 3) return Boolean(this.board) && this.board.parts.length > 0;
    return false;
  },

  goToStep(step) {
    if (!this.canOpen(step)) return;
    this.current = step;

    // sirf current step ka card dikhao
    [1, 2, 3].forEach((n) => {
      document.getElementById(`step-${n}`).classList.toggle("hidden", n !== step);
    });
    this.refreshStepper();

    // jo step khula uski file ko batao, taaki woh apna data load kar le
    document.dispatchEvent(new CustomEvent("step:enter", { detail: step }));
  },

  refreshStepper() {
    document.querySelectorAll(".step").forEach((el) => {
      const n = Number(el.dataset.step);
      el.classList.toggle("active", n === this.current);
      el.classList.toggle("locked", !this.canOpen(n));
      el.classList.toggle("done", n < this.current);
    });
  },

  // neeche se ek chhota message popup - 4 second me apne aap gayab
  toast(message, type = "error") {
    const box = document.getElementById("toast");
    box.textContent = message;
    box.className = `toast toast-${type}`;
    clearTimeout(this.toastTimer);
    this.toastTimer = setTimeout(() => box.classList.add("hidden"), 4000);
  },
};

// stepper pe click karke bhi step badal sakte hain (agar unlocked hai)
document.querySelectorAll(".step").forEach((el) => {
  el.addEventListener("click", () => App.goToStep(Number(el.dataset.step)));
});