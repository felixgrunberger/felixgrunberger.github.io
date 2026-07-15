(() => {
  const root = document.documentElement;
  const navbar = document.querySelector('.navbar');

  const updateHeader = () => {
    if (!navbar) return;
    root.style.setProperty('--header-height', `${navbar.getBoundingClientRect().height}px`);
    navbar.classList.toggle('is-scrolled', window.scrollY > 12);
  };
  updateHeader();
  window.addEventListener('resize', updateHeader, { passive: true });
  window.addEventListener('scroll', updateHeader, { passive: true });

  const panel = document.querySelector('[data-workflow-panel]');
  if (panel) {
    const steps = [...panel.querySelectorAll('[data-workflow-step]')];
    const response = panel.querySelector('[data-workflow-response]');
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    let activeIndex = 0;
    let timer = null;
    let userPaused = false;

    const summaries = steps.map(step => step.dataset.summary || '');
    let responseResizeTimer = null;

    const setResponseHeight = () => {
      if (!response) return;
      const previous = response.textContent;
      const previousVisibility = response.style.visibility;
      const previousPosition = response.style.position;
      const previousMinHeight = response.style.minHeight;
      response.style.minHeight = '0px';
      response.style.visibility = 'hidden';
      response.style.position = 'relative';
      let maxHeight = 0;
      summaries.forEach(summary => {
        response.textContent = summary;
        maxHeight = Math.max(maxHeight, Math.ceil(response.getBoundingClientRect().height));
      });
      response.textContent = previous;
      response.style.visibility = previousVisibility;
      response.style.position = previousPosition;
      response.style.minHeight = `${maxHeight}px`;
      if (previousMinHeight && !Number.isNaN(parseFloat(previousMinHeight))) {
        response.style.minHeight = `${Math.max(maxHeight, parseFloat(previousMinHeight))}px`;
      }
    };

    const handleResponseResize = () => {
      if (responseResizeTimer) window.clearTimeout(responseResizeTimer);
      responseResizeTimer = window.setTimeout(setResponseHeight, 120);
    };

    const activate = (index, focus = false) => {
      activeIndex = (index + steps.length) % steps.length;
      steps.forEach((step, idx) => {
        const active = idx === activeIndex;
        step.classList.toggle('is-active', active);
        step.setAttribute('aria-pressed', active ? 'true' : 'false');
        if (active && focus) step.focus({ preventScroll: true });
      });
      panel.dataset.activeStep = String(activeIndex + 1);
      if (response) {
        response.classList.add('is-updating');
        window.setTimeout(() => {
          response.textContent = steps[activeIndex].dataset.summary || '';
          response.classList.remove('is-updating');
        }, 90);
      }
    };

    steps.forEach((step, index) => {
      step.addEventListener('mouseenter', () => activate(index));
      step.addEventListener('focus', () => activate(index));
      step.addEventListener('click', () => {
        userPaused = true;
        activate(index);
        stopCycle();
      });
      step.addEventListener('keydown', event => {
        if (event.key === 'ArrowDown' || event.key === 'ArrowRight') {
          event.preventDefault(); userPaused = true; activate(index + 1, true); stopCycle();
        }
        if (event.key === 'ArrowUp' || event.key === 'ArrowLeft') {
          event.preventDefault(); userPaused = true; activate(index - 1, true); stopCycle();
        }
      });
    });

    const startCycle = () => {
      if (reducedMotion || userPaused || timer) return;
      timer = window.setInterval(() => activate(activeIndex + 1), 4200);
    };
    const stopCycle = () => {
      if (timer) window.clearInterval(timer);
      timer = null;
    };

    setResponseHeight();
    window.addEventListener('resize', handleResponseResize, { passive: true });

    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => entry.isIntersecting ? startCycle() : stopCycle());
    }, { threshold: .35 });
    observer.observe(panel);

    panel.addEventListener('pointermove', event => {
      if (reducedMotion || window.innerWidth < 900) return;
      const rect = panel.getBoundingClientRect();
      const x = ((event.clientX - rect.left) / rect.width) * 100;
      const y = ((event.clientY - rect.top) / rect.height) * 100;
      panel.style.setProperty('--pointer-x', `${x}%`);
      panel.style.setProperty('--pointer-y', `${y}%`);

    }, { passive: true });
    panel.addEventListener('pointerleave', () => {
      panel.style.setProperty('--pointer-x', '72%');
      panel.style.setProperty('--pointer-y', '20%');
    });
  }

  const revealItems = document.querySelectorAll('.reveal');
  if (revealItems.length) {
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reducedMotion) revealItems.forEach(item => item.classList.add('is-visible'));
    else {
      const revealObserver = new IntersectionObserver(entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            revealObserver.unobserve(entry.target);
          }
        });
      }, { threshold: .12, rootMargin: '0px 0px -40px' });
      revealItems.forEach(item => revealObserver.observe(item));
    }
  }
})();
