// Explainer tokens for GSAP. The clock is motion-style's: symmetric ease, three durations, linear only for exact events.
(function () {
  window.EASE = {
    move:   "power2.inOut",  // resizes, travel, anything carrying words
    settle: "power2.inOut",  // colour drains, opacity
    exact:  "none",          // geometry of an exact event only: an edge at constant speed, a pointer switch
  };
  window.DUR = { tick: 0.25, shape: 0.75, words: 1.4, hold: 1.0, handoffHold: 0.6, crossfade: 0.5 };
  window.SPEED = { edge: 1200 }; // px per second for every exact edge
  window.tok = function (name) { return getComputedStyle(document.documentElement).getPropertyValue(name).trim(); };
  if (window.gsap) gsap.defaults({ ease: window.EASE.move, duration: window.DUR.shape });
})();
