/**
 * script.js — Navbar interactions
 * - Hamburger open/close
 * - Mobile accordion sub-menus
 * - Close menu on outside click or Escape key
 * - Update aria-expanded for accessibility
 */

(function () {
  'use strict';

  const hamburger  = document.getElementById('hamburger-btn');
  const mobileMenu = document.getElementById('mobile-menu');
  const mobileDropdownToggles = document.querySelectorAll('.mobile-dropdown-toggle');

  if (!hamburger || !mobileMenu) return;

  /* ── Hamburger toggle ─────────────────────────── */
  function openMenu() {
    mobileMenu.classList.add('is-open');
    hamburger.classList.add('is-open');
    hamburger.setAttribute('aria-expanded', 'true');
    hamburger.setAttribute('aria-label', 'Close navigation menu');
    mobileMenu.setAttribute('aria-hidden', 'false');
  }

  function closeMenu() {
    mobileMenu.classList.remove('is-open');
    hamburger.classList.remove('is-open');
    hamburger.setAttribute('aria-expanded', 'false');
    hamburger.setAttribute('aria-label', 'Open navigation menu');
    mobileMenu.setAttribute('aria-hidden', 'true');
  }

  hamburger.addEventListener('click', function () {
    const isOpen = hamburger.getAttribute('aria-expanded') === 'true';
    isOpen ? closeMenu() : openMenu();
  });

  /* ── Mobile accordion dropdowns ──────────────── */
  mobileDropdownToggles.forEach(function (toggle) {
    toggle.addEventListener('click', function () {
      const isExpanded = toggle.getAttribute('aria-expanded') === 'true';
      const subMenu = toggle.nextElementSibling; // the <ul class="mobile-dropdown">

      // Close all other open dropdowns first
      mobileDropdownToggles.forEach(function (other) {
        if (other !== toggle) {
          other.setAttribute('aria-expanded', 'false');
          const otherSub = other.nextElementSibling;
          if (otherSub) otherSub.classList.remove('is-open');
        }
      });

      // Toggle current
      if (isExpanded) {
        toggle.setAttribute('aria-expanded', 'false');
        if (subMenu) subMenu.classList.remove('is-open');
      } else {
        toggle.setAttribute('aria-expanded', 'true');
        if (subMenu) subMenu.classList.add('is-open');
      }
    });
  });

  /* ── Close menu on outside click ─────────────── */
  document.addEventListener('click', function (e) {
    const header = document.getElementById('site-header');
    if (header && !header.contains(e.target)) {
      closeMenu();
    }
  });

  /* ── Close on Escape key ──────────────────────── */
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      closeMenu();
      hamburger.focus();
    }
  });

  /* ── Close menu when a mobile nav link is clicked ── */
  const mobileLinks = mobileMenu.querySelectorAll('a');
  mobileLinks.forEach(function (link) {
    link.addEventListener('click', function () {
      closeMenu();
    });
  });

})();

// section 3:

// const cards =
// document.querySelectorAll(".facility-card");

// const observer =
// new IntersectionObserver(entries => {

//     entries.forEach(entry => {

//         if(entry.isIntersecting){

//             entry.target.classList.add("show");
//         }

//     });

// },{
//     threshold:0.2
// });

// cards.forEach(card=>{
//     observer.observe(card);
// });