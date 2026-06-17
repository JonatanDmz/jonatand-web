(function () {
  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in-view');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
  );

  document.querySelectorAll(
    '.animate-fade-in-up, .animate-fade-in, .animate-scale-in, .animate-slide-left, .animate-slide-right'
  ).forEach(function (el) {
    observer.observe(el);
  });
})();
