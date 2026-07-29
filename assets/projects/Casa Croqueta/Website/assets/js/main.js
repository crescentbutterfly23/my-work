/* Casa Croqueta — light interactions (no dependencies) */
(function () {
  "use strict";

  // Sticky nav background on scroll
  var nav = document.querySelector("[data-nav]");
  if (nav) {
    var onScroll = function () {
      if (window.scrollY > 24) nav.classList.add("scrolled");
      else nav.classList.remove("scrolled");
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  // Mobile nav toggle
  var toggle = document.querySelector("[data-nav-toggle]");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      nav.classList.toggle("open");
      var open = nav.classList.contains("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    nav.querySelectorAll(".nav-links a").forEach(function (a) {
      a.addEventListener("click", function () { nav.classList.remove("open"); });
    });
  }

  // Scroll-reveal is handled entirely in CSS (scroll-driven animations),
  // so content is always visible even if this script never runs.

  // Current year
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  // ------------------------------------------------------------------
  // Cart: menu -> add to cart -> drawer -> order review -> Google Form
  // ------------------------------------------------------------------
  var CART_KEY = "cc_cart_v1";

  function loadCart() {
    try {
      var raw = window.localStorage.getItem(CART_KEY);
      var parsed = raw ? JSON.parse(raw) : [];
      return Array.isArray(parsed) ? parsed : [];
    } catch (err) {
      return [];
    }
  }
  function saveCart(cart) {
    try { window.localStorage.setItem(CART_KEY, JSON.stringify(cart)); } catch (err) { /* storage unavailable, cart stays in memory only */ }
  }

  var cart = loadCart();

  function money(n) {
    return "$" + n.toFixed(2).replace(/\.00$/, "");
  }
  function cartTotal() {
    return cart.reduce(function (sum, line) { return sum + line.price * line.qty; }, 0);
  }
  function findLine(id) {
    for (var i = 0; i < cart.length; i++) if (cart[i].id === id) return cart[i];
    return null;
  }

  function addToCart(id, name, price, qty) {
    var line = findLine(id);
    if (line) line.qty += qty;
    else cart.push({ id: id, name: name, price: price, qty: qty });
    saveCart(cart);
    renderCart();
  }
  function removeFromCart(id) {
    cart = cart.filter(function (line) { return line.id !== id; });
    saveCart(cart);
    renderCart();
  }
  function setQty(id, qty) {
    var line = findLine(id);
    if (!line) return;
    if (qty <= 0) return removeFromCart(id);
    line.qty = qty;
    saveCart(cart);
    renderCart();
  }

  // -- Rendering: nav badge, drawer, order-review summary --
  var cartCountEl = document.querySelector("[data-cart-count]");
  var drawerList = document.querySelector("[data-drawer-list]");
  var drawerEmpty = document.querySelector("[data-drawer-empty]");
  var drawerFoot = document.querySelector("[data-drawer-foot]");
  var drawerTotalAmount = document.querySelector("[data-drawer-total-amount]");
  var reviewEmpty = document.querySelector("[data-cart-empty]");
  var reviewList = document.querySelector("[data-cart-list]");
  var reviewTotal = document.querySelector("[data-cart-total]");
  var reviewTotalAmount = document.querySelector("[data-cart-total-amount]");
  var messageField = document.getElementById("of-message");

  function renderCart() {
    var itemCount = cart.reduce(function (n, l) { return n + l.qty; }, 0);
    if (cartCountEl) {
      cartCountEl.textContent = String(itemCount);
      cartCountEl.hidden = itemCount === 0;
    }

    // Drawer
    if (drawerList) {
      drawerList.innerHTML = "";
      cart.forEach(function (line) {
        var li = document.createElement("li");
        li.className = "cart-line";
        li.innerHTML =
          '<div><div class="cart-line-name">' + escapeHtml(line.name) + '</div>' +
          '<div class="cart-line-meta">' + money(line.price) + " each</div></div>" +
          '<div class="cart-line-price">' + money(line.price * line.qty) + "</div>" +
          '<div class="cart-line-controls">' +
          '<div class="qty-stepper" data-line-stepper>' +
          '<button type="button" data-line-minus aria-label="Decrease quantity">&minus;</button>' +
          '<input type="number" value="' + line.qty + '" min="1" max="20" data-line-qty aria-label="Quantity">' +
          '<button type="button" data-line-plus aria-label="Increase quantity">+</button>' +
          "</div>" +
          '<button type="button" class="cart-line-remove" data-line-remove>Remove</button>' +
          "</div>";
        li.querySelector("[data-line-minus]").addEventListener("click", function () { setQty(line.id, line.qty - 1); });
        li.querySelector("[data-line-plus]").addEventListener("click", function () { setQty(line.id, line.qty + 1); });
        li.querySelector("[data-line-qty]").addEventListener("change", function (e) {
          setQty(line.id, Math.max(1, parseInt(e.target.value, 10) || 1));
        });
        li.querySelector("[data-line-remove]").addEventListener("click", function () { removeFromCart(line.id); });
        drawerList.appendChild(li);
      });
    }
    if (drawerEmpty) drawerEmpty.hidden = cart.length > 0;
    if (drawerFoot) drawerFoot.hidden = cart.length === 0;
    if (drawerTotalAmount) drawerTotalAmount.textContent = money(cartTotal());

    // Order review (above the send-order form)
    if (reviewList) {
      reviewList.innerHTML = "";
      cart.forEach(function (line) {
        var li = document.createElement("li");
        li.innerHTML =
          "<span><b>" + line.qty + "&times;</b> " + escapeHtml(line.name) + "</span>" +
          "<span>" + money(line.price * line.qty) + "</span>";
        reviewList.appendChild(li);
      });
    }
    if (reviewEmpty) reviewEmpty.hidden = cart.length > 0;
    if (reviewList) reviewList.hidden = cart.length === 0;
    if (reviewTotal) reviewTotal.hidden = cart.length === 0;
    if (reviewTotalAmount) reviewTotalAmount.textContent = money(cartTotal());
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function cartSummaryText() {
    if (!cart.length) return "";
    var lines = cart.map(function (l) {
      return l.qty + "x " + l.name + " (" + money(l.price * l.qty) + ")";
    });
    return "Order:\n" + lines.join("\n") + "\nEstimated total: " + money(cartTotal());
  }

  // -- Menu: quantity steppers + add to cart --
  document.querySelectorAll(".menu-item").forEach(function (item) {
    var id = item.getAttribute("data-id");
    var name = item.getAttribute("data-name");
    var price = parseFloat(item.getAttribute("data-price"));
    var qtyInput = item.querySelector("[data-qty-input]");
    var minusBtn = item.querySelector("[data-qty-minus]");
    var plusBtn = item.querySelector("[data-qty-plus]");
    var addBtn = item.querySelector("[data-add-to-cart]");

    minusBtn.addEventListener("click", function () {
      qtyInput.value = Math.max(1, (parseInt(qtyInput.value, 10) || 1) - 1);
    });
    plusBtn.addEventListener("click", function () {
      qtyInput.value = Math.min(20, (parseInt(qtyInput.value, 10) || 1) + 1);
    });
    addBtn.addEventListener("click", function () {
      var qty = Math.max(1, parseInt(qtyInput.value, 10) || 1);
      addToCart(id, name, price, qty);
      qtyInput.value = 1;
      var original = addBtn.textContent;
      addBtn.textContent = "Added";
      addBtn.classList.add("added");
      setTimeout(function () {
        addBtn.textContent = original;
        addBtn.classList.remove("added");
      }, 1200);
    });
  });

  // -- Cart drawer open/close --
  var drawer = document.querySelector("[data-cart-drawer]");
  var cartToggle = document.querySelector("[data-cart-toggle]");
  if (drawer && cartToggle) {
    var openDrawer = function () {
      drawer.classList.add("open");
      drawer.setAttribute("aria-hidden", "false");
      cartToggle.setAttribute("aria-expanded", "true");
    };
    var closeDrawer = function () {
      drawer.classList.remove("open");
      drawer.setAttribute("aria-hidden", "true");
      cartToggle.setAttribute("aria-expanded", "false");
    };
    cartToggle.addEventListener("click", openDrawer);
    drawer.querySelectorAll("[data-cart-close]").forEach(function (el) {
      el.addEventListener("click", closeDrawer);
    });
    document.querySelectorAll("[data-cart-checkout]").forEach(function (el) {
      el.addEventListener("click", closeDrawer);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeDrawer();
    });
  }

  renderCart();

  // -- Order form -> Google Form (hidden-iframe submit) --
  // Progressive enhancement: the <form action target="hidden-form-target">
  // already works with zero JS, submitting into the hidden iframe below so
  // the visitor never leaves the site. JS only adds the inline thank-you
  // message, the cart-summary merge into the message field, and a basic
  // honeypot check.
  var form = document.getElementById("order-form");
  var hiddenFrame = document.querySelector("[data-hidden-form-target]");
  if (form) {
    var statusEl = form.querySelector(".form-status");
    var submitBtn = form.querySelector('button[type="submit"]');
    var honeypot = form.querySelector('[name="company"]');
    var submittedOnce = false;

    if (hiddenFrame) {
      hiddenFrame.addEventListener("load", function () {
        // The very first load is the blank iframe itself; ignore it.
        if (!submittedOnce) return;
        statusEl.textContent = "Thank you. We received your order inquiry and will be in touch soon.";
        statusEl.className = "form-status is-success";
        submitBtn.disabled = false;
        submitBtn.textContent = "Send Order Inquiry";
        form.reset();
        cart = [];
        saveCart(cart);
        renderCart();
      });
    }

    form.addEventListener("submit", function (e) {
      if (honeypot && honeypot.value) { e.preventDefault(); return; } // bot caught
      if (form.action.indexOf("YOUR_GOOGLE_FORM_ID") !== -1) {
        e.preventDefault();
        statusEl.textContent = "This form is not connected yet. Please DM or email us directly for now.";
        statusEl.className = "form-status is-error";
        return;
      }

      // Merge the cart summary into the message before it gets sent.
      var summary = cartSummaryText();
      if (summary && messageField) {
        messageField.value = summary + (messageField.value ? "\n\n" + messageField.value : "");
      }

      submittedOnce = true;
      statusEl.textContent = "";
      statusEl.className = "form-status";
      submitBtn.disabled = true;
      submitBtn.textContent = "Sending...";
      // Let the native submission proceed into the hidden iframe.
    });
  }
})();
