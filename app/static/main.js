document.addEventListener("DOMContentLoaded", function () {

  // ── Take dose (AJAX) ──────────────────────────────────
  document.querySelectorAll(".take-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var id = btn.dataset.id;
      btn.disabled = true;

      fetch("/medicines/" + id + "/take", {
        method: "POST",
        headers: { "X-Requested-With": "XMLHttpRequest" },
      })
        .then(function (res) { return res.json(); })
        .then(function (data) {
          if (data.error === "out_of_stock") {
            showToast("Out of stock!", "danger");
            return;
          }
          updateCard(id, data.stock, data.status);
          showToast("Dose taken! " + data.stock + " remaining.", "success");
          if (data.stock === 0) btn.disabled = true;
          else btn.disabled = false;
        })
        .catch(function () {
          btn.disabled = false;
          showToast("Something went wrong.", "danger");
        });
    });
  });

  // ── Refill stock (AJAX) ───────────────────────────────
  document.querySelectorAll(".refill-form").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var id = form.dataset.id;
      var amount = form.querySelector("input[name=amount]").value;

      fetch("/medicines/" + id + "/stock", {
        method: "POST",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: "amount=" + encodeURIComponent(amount),
      })
        .then(function (res) { return res.json(); })
        .then(function (data) {
          updateCard(id, data.stock, data.status);
          showToast("Refilled! New stock: " + data.stock + ".", "success");
          var takeBtn = document.querySelector(".take-btn[data-id='" + id + "']");
          if (takeBtn) takeBtn.disabled = false;
        })
        .catch(function () {
          showToast("Refill failed.", "danger");
        });
    });
  });

  // ── Countdown timers ──────────────────────────────────
  function formatCountdown(seconds) {
    if (seconds <= 0) return "Now!";
    var h = Math.floor(seconds / 3600);
    var m = Math.floor((seconds % 3600) / 60);
    if (h > 0) return "in " + h + "h " + m + "m";
    return "in " + m + "m";
  }

  var countdowns = document.querySelectorAll(".countdown");
  countdowns.forEach(function (el) {
    var remaining = parseInt(el.dataset.seconds, 10);

    el.textContent = formatCountdown(remaining);

    var interval = setInterval(function () {
      remaining -= 1;
      if (remaining <= 0) {
        el.textContent = "Now!";
        clearInterval(interval);
      } else {
        el.textContent = formatCountdown(remaining);
      }
    }, 1000);
  });

  // ── Update card DOM (extended) ────────────────────────
  function updateCard(id, stock, status, days) {
    var card = document.getElementById("card-" + id);
    if (!card) return;

    var countEl = document.getElementById("stock-" + id);
    if (countEl) {
      countEl.innerHTML =
        "<strong>" + stock + "</strong> dose" + (stock !== 1 ? "s" : "") + " remaining" +
        " · <span id='days-" + id + "'><strong>" + (days !== undefined ? days : "?") +
        "</strong> days supply</span>";
    }

    var badge = card.querySelector(".badge");
    if (badge) {
      badge.className = "badge badge-" + status;
      badge.textContent =
        status === "ok" ? "In stock" : status === "low" ? "Low stock" : "Out of stock";
    }

    var bar = card.querySelector(".stock-bar");
    if (bar) {
      bar.className = "stock-bar " + status;
    }
  }

  // ── Profile dropdown ──────────────────────────────────
  var avatarBtn       = document.getElementById("avatarBtn");
  var profileDropdown = document.getElementById("profileDropdown");

  if (avatarBtn) {
    avatarBtn.addEventListener("click", function (e) {
      e.stopPropagation();
      profileDropdown.classList.toggle("open");
    });

    document.addEventListener("click", function () {
      profileDropdown.classList.remove("open");
    });
  }

  // ── Update card DOM ───────────────────────────────────
  function updateCard(id, stock, status) {
    var card = document.getElementById("card-" + id);
    if (!card) return;

    // Stock count text
    var countEl = document.getElementById("stock-" + id);
    if (countEl) {
      countEl.innerHTML =
        "<strong>" + stock + "</strong> dose" + (stock !== 1 ? "s" : "") + " remaining";
    }

    // Badge
    var badge = card.querySelector(".badge");
    if (badge) {
      badge.className = "badge badge-" + status;
      badge.textContent =
        status === "ok" ? "In stock" : status === "low" ? "Low stock" : "Out of stock";
    }

    // Progress bar
    var bar = card.querySelector(".stock-bar");
    if (bar) {
      bar.className = "stock-bar " + status;
    }
  }

  // ── Toast notifications ───────────────────────────────
  function showToast(message, type) {
    var container = document.getElementById("toast-container");
    if (!container) {
      container = document.createElement("div");
      container.id = "toast-container";
      container.style.cssText =
        "position:fixed;bottom:24px;right:24px;display:flex;flex-direction:column;gap:8px;z-index:9999;";
      document.body.appendChild(container);
    }

    var toast = document.createElement("div");
    toast.className = "alert alert-" + type;
    toast.style.cssText =
      "padding:12px 18px;border-radius:8px;font-size:14px;font-weight:500;" +
      "box-shadow:0 4px 12px rgba(0,0,0,.15);max-width:300px;";
    toast.textContent = message;
    container.appendChild(toast);

    setTimeout(function () {
      toast.style.opacity = "0";
      toast.style.transition = "opacity 0.3s";
      setTimeout(function () { toast.remove(); }, 300);
    }, 3000);
  }
});