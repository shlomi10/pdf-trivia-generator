const LOADING_STEPS = [
  "Reading your document...",
  "Analyzing the content...",
  "Creating trivia questions with AI...",
  "Almost ready...",
];

let loadingInterval = null;

function showLoadingOverlay() {
  const overlay = document.getElementById("loading-overlay");
  const step = document.getElementById("loading-step");
  const timer = document.getElementById("loading-timer");
  if (!overlay) return;

  const start = Date.now();
  let stepIndex = 0;

  overlay.hidden = false;
  step.textContent = LOADING_STEPS[0];
  timer.textContent = "0s";

  if (loadingInterval) clearInterval(loadingInterval);
  loadingInterval = setInterval(() => {
    const elapsed = Math.floor((Date.now() - start) / 1000);
    timer.textContent = elapsed + "s";
    const nextStep = Math.min(Math.floor(elapsed / 4), LOADING_STEPS.length - 1);
    if (nextStep !== stepIndex) {
      stepIndex = nextStep;
      step.textContent = LOADING_STEPS[stepIndex];
    }
  }, 1000);
}

function hideLoadingOverlay() {
  const overlay = document.getElementById("loading-overlay");
  if (overlay) overlay.hidden = true;
  if (loadingInterval) {
    clearInterval(loadingInterval);
    loadingInterval = null;
  }
}

function submitForm(form, endpoint) {
  const formData = new FormData(form);
  const card = form.closest(".upload-option-card");
  const allButtons = card.querySelectorAll("button");

  allButtons.forEach((btn) => { btn.disabled = true; });
  showLoadingOverlay();

  const xhr = new XMLHttpRequest();
  xhr.onload = () => {
    setTimeout(() => {
      hideLoadingOverlay();
      if (xhr.status === 200 && xhr.getResponseHeader("content-type").includes("text/html")) {
        document.open();
        document.write(xhr.responseText);
        document.close();
      } else {
        try {
          const error = JSON.parse(xhr.responseText);
          alert(error.detail || "Request failed.");
        } catch {
          alert("Request failed.");
        }
        allButtons.forEach((btn) => { btn.disabled = false; });
      }
    }, 300);
  };

  xhr.onerror = () => {
    hideLoadingOverlay();
    alert("Something went wrong.");
    allButtons.forEach((btn) => { btn.disabled = false; });
  };

  xhr.open("POST", endpoint, true);
  xhr.withCredentials = true;
  xhr.send(formData);
}

document.addEventListener("DOMContentLoaded", () => {
  const uploadForm = document.getElementById("upload-form");
  if (uploadForm) {
    uploadForm.addEventListener("submit", (e) => {
      e.preventDefault();
      submitForm(e.target, "/upload-pdf");
    });
  }

  const guestUploadForm = document.getElementById("guest-upload-form");
  if (guestUploadForm) {
    guestUploadForm.addEventListener("submit", (e) => {
      e.preventDefault();
      submitForm(e.target, "/upload-pdf-guest");
    });
  }

  document.querySelectorAll(".default-pdf-form").forEach((form) => {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      submitForm(form, form.dataset.endpoint);
    });
  });
});
