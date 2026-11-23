// saare server calls ek jagah - baaki files bas yeh functions use karti hain
// yeh sab 127.0.0.1 (apna laptop) pe jaate hain, internet pe nahi
const Api = {
  async request(url, options = {}) {
    const res = await fetch(url, options);
    const data = await res.json().catch(() => ({}));
    // server ne error bheja to wahi message aage bhejo
    if (!res.ok) {
      throw new Error(data.error || "Something went wrong");
    }
    return data;
  },

  listBoards() {
    return this.request("/api/boards");
  },

  getBoard(id) {
    return this.request(`/api/boards/${id}`);
  },

  createBoard(file, name) {
    // file bhejne ke liye FormData use hota hai
    const form = new FormData();
    form.append("image", file);
    form.append("name", name || "");
    return this.request("/api/boards", { method: "POST", body: form });
  },

  saveParts(id, parts) {
    return this.request(`/api/boards/${id}/parts`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ parts }),
    });
  },

  inspect(id, files) {
    const form = new FormData();
    files.forEach((file) => form.append("images", file));
    return this.request(`/api/boards/${id}/inspect`, { method: "POST", body: form });
  },

  referenceUrl(id) {
    return `/api/boards/${id}/reference`;
  },
};