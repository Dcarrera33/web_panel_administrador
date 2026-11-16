/* JavaScript de la web: menú móvil, entrada de los contenidos al hacer scroll y carrusel de «Saber más». */
(function () {
  "use strict";

  // ---- Entrada al hacer scroll ----
  // Cada bloque sube y aparece al entrar en pantalla, uno detrás de otro. Sin JavaScript todo se ve igual, sin animar.
  if ("IntersectionObserver" in window) {
    document.documentElement.classList.add("js");
    var groups = document.querySelectorAll(
      ".split__photo, .split__text > *, .page-head > *, .section-head > *, .course-list, .course__main > *, .aside, " +
      ".carousel-wrap, .steps, .faq-layout__head, .faq, .cta-band__inner > *, .contact > *"
    );
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("is-visible"); observer.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    groups.forEach(function (el) {
      // Las listas entran elemento a elemento
      var items = el.matches(".course-list, .steps, .faq") ? el.children : [el];
      Array.prototype.forEach.call(items, function (item) {
        var siblings = Array.prototype.indexOf.call(item.parentNode.children, item);
        item.classList.add("reveal");
        item.style.transitionDelay = Math.min(siblings, 6) * 80 + "ms";
        observer.observe(item);
      });
    });
  }

  // ---- Menú hamburguesa (móvil) ----
  var burger = document.querySelector(".burger");
  var nav = document.querySelector(".mainnav");
  if (burger && nav) {
    burger.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      burger.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  // ---- Carrusel de fotos ----
  // Cambia solo cada data-seconds segundos; flechas, puntos y deslizar con el dedo.
  // Se pausa con el ratón encima y no se mueve solo si el usuario ha pedido "reducir movimiento".
  document.querySelectorAll("[data-carousel]").forEach(function (box) {
    var slides = box.querySelectorAll(".carousel__slide");
    if (slides.length < 2) return;
    var seconds = parseInt(box.dataset.seconds, 10) || 6;
    var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var dotsBox = box.parentNode.querySelector(".carousel__dots");
    var dots = dotsBox ? dotsBox.querySelectorAll("button") : [];
    var current = 0, timer = null;

    function show(n) {
      slides[current].classList.remove("is-active");
      current = (n + slides.length) % slides.length;
      slides[current].classList.add("is-active");
      dots.forEach(function (d, i) { d.setAttribute("aria-current", i === current ? "true" : "false"); });
    }
    function stop() { if (timer) { clearInterval(timer); timer = null; } }
    function start() { stop(); if (!reduce) timer = setInterval(function () { show(current + 1); }, seconds * 1000); }
    function go(n) { show(n); start(); }

    var prev = box.querySelector(".carousel__btn--prev");
    var next = box.querySelector(".carousel__btn--next");
    if (prev) prev.addEventListener("click", function () { go(current - 1); });
    if (next) next.addEventListener("click", function () { go(current + 1); });
    dots.forEach(function (d, i) { d.addEventListener("click", function () { go(i); }); });

    box.addEventListener("mouseenter", stop);
    box.addEventListener("mouseleave", start);
    box.addEventListener("focusin", stop);
    box.addEventListener("focusout", start);

    var startX = null;
    box.addEventListener("touchstart", function (e) { startX = e.touches[0].clientX; stop(); }, { passive: true });
    box.addEventListener("touchend", function (e) {
      if (startX !== null) {
        var dx = e.changedTouches[0].clientX - startX;
        if (Math.abs(dx) > 40) show(current + (dx < 0 ? 1 : -1));
      }
      startX = null; start();
    });
    box.addEventListener("keydown", function (e) {
      if (e.key === "ArrowLeft") go(current - 1);
      if (e.key === "ArrowRight") go(current + 1);
    });

    show(0);
    start();
  });
})();
