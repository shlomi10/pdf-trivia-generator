(function () {
  function fmt(template, vars) {
    return template.replace(/\{(\w+)\}/g, (_, key) => (vars[key] != null ? vars[key] : ""));
  }

  function updateChrome(data) {
    document.documentElement.lang = data.lang;
    document.documentElement.dir = data.dir;
    document.querySelectorAll(".lang-btn").forEach((btn) => {
      btn.classList.toggle("active", btn.getAttribute("data-lang") === data.lang);
    });
    document.querySelectorAll("[data-i18n]").forEach((el) => {
      const key = el.getAttribute("data-i18n");
      if (data.ui[key] != null) el.textContent = data.ui[key];
    });
    const welcome = document.querySelector("[data-i18n-welcome]");
    if (welcome && data.ui["welcome.user"]) {
      const name = welcome.getAttribute("data-username") || "";
      welcome.textContent = fmt(data.ui["welcome.user"], { name: name }) + " 👋";
    }
    if (typeof window.applyLanguage === "function") {
      window.applyLanguage(data);
    }
  }

  async function switchLang(lang) {
    const res = await fetch("/set-language/" + encodeURIComponent(lang) + "?format=json", {
      credentials: "include",
      headers: { Accept: "application/json" },
    });
    if (!res.ok) throw new Error("language switch failed");
    updateChrome(await res.json());
  }

  document.addEventListener("click", (e) => {
    const btn = e.target.closest(".lang-btn");
    if (!btn || !window.__preserveLangSwitch) return;
    e.preventDefault();
    switchLang(btn.getAttribute("data-lang")).catch(() => {
      window.location.href = btn.getAttribute("href");
    });
  });
})();
