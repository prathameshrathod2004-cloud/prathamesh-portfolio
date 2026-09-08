// =========================================================
// PRATHAMESH RATHOD PORTFOLIO — INTERACTIONS & ANIMATIONS
// =========================================================

document.addEventListener("DOMContentLoaded", () => {

  // ---- Init scroll animations ----
  if (window.AOS) {
    AOS.init({ once: true, duration: 800, easing: "ease-out-cubic" });
  }

  // ---- Preloader ----
  const preloader = document.getElementById("preloader");
  window.addEventListener("load", () => {
    setTimeout(() => preloader && preloader.classList.add("hide"), 300);
  });
  // Fallback in case 'load' already fired
  setTimeout(() => preloader && preloader.classList.add("hide"), 1500);

  // ---- Set footer year ----
  const yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // ---- Mobile hamburger menu ----
  const hamburger = document.getElementById("hamburger");
  const navLinks = document.getElementById("navLinks");
  if (hamburger && navLinks) {
    hamburger.addEventListener("click", () => {
      navLinks.classList.toggle("open");
      hamburger.classList.toggle("active");
    });
    navLinks.querySelectorAll("a").forEach(link => {
      link.addEventListener("click", () => navLinks.classList.remove("open"));
    });
  }

  // ---- Navbar shrink on scroll ----
  const navbar = document.getElementById("navbar");
  if (navbar) {
    window.addEventListener("scroll", () => {
      if (window.scrollY > 40) {
        navbar.style.background = "rgba(6,6,8,0.9)";
        navbar.style.padding = "10px 0";
      } else {
        navbar.style.background = "rgba(6,6,8,0.55)";
        navbar.style.padding = "18px 0";
      }
    });
  }

  // ---- Typed text effect (hero subtitle) ----
  const typedEl = document.getElementById("typed-text");
  if (typedEl) {
    const phrases = [
      "Instagram Reel Editor",
      "Political Video Editor",
      "Cinematic Wedding Videographer",
      "Pre-Wedding & Couple Shoots",
      "Birthday Event Videographer"
    ];
    let phraseIndex = 0;
    let charIndex = 0;
    let deleting = false;

    function type() {
      const current = phrases[phraseIndex];
      if (!deleting) {
        typedEl.textContent = current.substring(0, charIndex + 1);
        charIndex++;
        if (charIndex === current.length) {
          deleting = true;
          setTimeout(type, 1400);
          return;
        }
      } else {
        typedEl.textContent = current.substring(0, charIndex - 1);
        charIndex--;
        if (charIndex === 0) {
          deleting = false;
          phraseIndex = (phraseIndex + 1) % phrases.length;
        }
      }
      setTimeout(type, deleting ? 40 : 80);
    }
    type();
  }

  // ---- Animated counters (About stats) ----
  const counters = document.querySelectorAll(".counter");
  if (counters.length) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });

    counters.forEach(counter => observer.observe(counter));
  }

  function animateCounter(el) {
    const target = parseInt(el.getAttribute("data-target"), 10);
    let current = 0;
    const step = Math.max(1, Math.ceil(target / 60));
    const timer = setInterval(() => {
      current += step;
      if (current >= target) {
        current = target;
        clearInterval(timer);
      }
      el.textContent = current;
    }, 25);
  }

});
