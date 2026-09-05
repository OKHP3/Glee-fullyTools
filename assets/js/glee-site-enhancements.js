// Glee-specific behavior intentionally kept outside the shared foundation runtime.
(function () {
  const measurementId = "G-89W66VMGPB";
  const consentKey = "glee-analytics-consent";

  function readConsent() {
    try { return localStorage.getItem(consentKey); } catch (_) { return null; }
  }
  function writeConsent(value) {
    try { localStorage.setItem(consentKey, value); } catch (_) {}
  }
  function loadAnalytics() {
    window["ga-disable-" + measurementId] = false;
    if (document.querySelector("script[data-glee-analytics]")) return;
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
    window.gtag("js", new Date());
    window.gtag("config", measurementId, {
      client_storage: "none",
      allow_google_signals: false,
      allow_ad_personalization_signals: false,
    });
    const script = document.createElement("script");
    script.async = true;
    script.src = "https://www.googletagmanager.com/gtag/js?id=" + measurementId;
    script.dataset.gleeAnalytics = "true";
    document.head.appendChild(script);
  }
  function setAnalyticsConsent(value) {
    writeConsent(value);
    if (value === "granted") loadAnalytics();
    else window["ga-disable-" + measurementId] = true;
    document.querySelectorAll("[data-analytics-status]").forEach((status) => {
      status.textContent = value === "granted"
        ? "Optional analytics is on for this browser."
        : "Optional analytics is off for this browser.";
    });
  }
  window.gleeAnalytics = {
    enable: () => setAnalyticsConsent("granted"),
    disable: () => setAnalyticsConsent("denied"),
    status: readConsent,
  };
  if (readConsent() === "granted") loadAnalytics();
  document.querySelectorAll("[data-analytics-action]").forEach((button) => {
    button.addEventListener("click", () => setAnalyticsConsent(button.dataset.analyticsAction));
  });

  if ("serviceWorker" in navigator) {
    window.addEventListener("load", () => {
      navigator.serviceWorker.register("/sw.js", { scope: "/" }).catch(() => {});
    });
  }

  document.querySelectorAll("[data-external-frame]").forEach((frame) => {
    const selector = frame.getAttribute("data-fallback");
    const fallback = selector && document.querySelector(selector);
    if (!fallback) return;
    let timer;
    const show = () => { window.clearTimeout(timer); fallback.hidden = false; fallback.classList.add("visible"); };
    frame.addEventListener("load", () => { window.clearTimeout(timer); fallback.hidden = true; fallback.classList.remove("visible"); }, { once: true });
    frame.addEventListener("error", show, { once: true });
    timer = window.setTimeout(show, Number(frame.dataset.timeout || 8000));
  });

  function applySparkle(data) {
    const links = document.querySelectorAll("[data-sparkle-link]");
    if (!links.length) return;
    const text = (data.emoji ? data.emoji + " " : "") + (data.label || "") +
      (data.description ? " — " + data.description : "") + (data.suffix ? " " + data.suffix : "");
    links.forEach((link) => {
      if (data.url) link.href = data.url;
      if (text) link.textContent = text;
    });
  }
  fetch("/assets/data/sparkle.json")
    .then((response) => response.ok ? response.json() : null)
    .then((data) => { if (data) applySparkle(data); })
    .catch(() => {});
}());
