/* ── Hero Carousel ────────────────────────────────────────────────────────── */
(function () {
  const slides = document.querySelectorAll('.hero-slide');
  const dots = document.querySelectorAll('.hero-dot');
  const fills = document.querySelectorAll('.hero-progress-fill');
  if (!slides.length) return;

  let current = 0;
  let timer = null;

  function goTo(idx) {
    slides[current].classList.remove('active');
    dots[current]?.classList.remove('bg-white', 'w-6');
    dots[current]?.classList.add('bg-white/50', 'w-2');
    fills[current]?.classList.remove('running');
    fills[current] && (fills[current].style.animation = 'none');

    current = (idx + slides.length) % slides.length;

    slides[current].classList.add('active');
    dots[current]?.classList.add('bg-white', 'w-6');
    dots[current]?.classList.remove('bg-white/50', 'w-2');

    if (fills[current]) {
      fills[current].style.animation = 'none';
      // Force reflow
      void fills[current].offsetWidth;
      fills[current].classList.add('running');
    }
  }

  function next() { goTo(current + 1); }

  function startTimer() {
    clearInterval(timer);
    timer = setInterval(next, 4000);
  }

  // Dot click
  dots.forEach((dot, i) => dot.addEventListener('click', () => { goTo(i); startTimer(); }));

  // Prev/Next buttons
  document.getElementById('hero-prev')?.addEventListener('click', () => { goTo(current - 1); startTimer(); });
  document.getElementById('hero-next')?.addEventListener('click', () => { goTo(current + 1); startTimer(); });

  goTo(0);
  startTimer();
})();


/* ── Image Gallery ────────────────────────────────────────────────────────── */
(function () {
  const mainImg = document.getElementById('gallery-main');
  const thumbs = document.querySelectorAll('.gallery-thumb');
  if (!mainImg || !thumbs.length) return;

  thumbs.forEach(thumb => {
    thumb.addEventListener('click', () => {
      mainImg.src = thumb.dataset.src;
      thumbs.forEach(t => t.classList.remove('active'));
      thumb.classList.add('active');
    });
  });

  // Activate first thumb
  thumbs[0]?.classList.add('active');
})();


/* ── Donate Form — Anonymous Toggle ──────────────────────────────────────── */
(function () {
  const checkbox = document.getElementById('id_is_anonymous');
  const personalFields = document.getElementById('personal-fields');
  if (!checkbox || !personalFields) return;

  function toggle() {
    if (checkbox.checked) {
      personalFields.style.opacity = '0.4';
      personalFields.style.pointerEvents = 'none';
      personalFields.querySelectorAll('input, textarea').forEach(el => el.removeAttribute('required'));
    } else {
      personalFields.style.opacity = '1';
      personalFields.style.pointerEvents = '';
    }
  }

  checkbox.addEventListener('change', toggle);
  toggle();
})();


/* ── Contact Form — Character Counter ────────────────────────────────────── */
(function () {
  const textarea = document.getElementById('id_message');
  const counter = document.getElementById('message-counter');
  if (!textarea || !counter) return;

  function update() {
    const len = textarea.value.length;
    counter.textContent = len + ' حرف';
    counter.style.color = len < 10 ? '#dc2626' : '#6b7280';
  }
  textarea.addEventListener('input', update);
  update();
})();


/* ── Stats Counter Animation (IntersectionObserver) ────────────────────── */
(function () {
  const statEls = document.querySelectorAll('[data-count]');
  if (!statEls.length) return;

  function animateCount(el) {
    const target = parseInt(el.dataset.count, 10);
    const duration = 1800;
    const step = 16;
    const increment = target / (duration / step);
    let current = 0;

    const t = setInterval(() => {
      current += increment;
      if (current >= target) {
        current = target;
        clearInterval(t);
      }
      el.textContent = '+' + Math.floor(current).toLocaleString('ar-EG');
    }, step);
  }

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCount(entry.target);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.4 });

  statEls.forEach(el => observer.observe(el));
})();


/* ── Donate Form — Quick Amount Buttons ─────────────────────────────────── */
(function () {
  const amountInput = document.getElementById('id_amount');
  const buttons = document.querySelectorAll('.quick-amt');
  if (!amountInput || !buttons.length) return;

  window.setAmount = function (val) {
    amountInput.value = val;
    buttons.forEach(b => {
      const isActive = parseInt(b.textContent.replace('$', '').trim()) === val;
      b.classList.toggle('border-primary', isActive);
      b.classList.toggle('text-primary', isActive);
      b.classList.toggle('bg-primary/5', isActive);
    });
  };

  amountInput.addEventListener('input', () => {
    buttons.forEach(b => {
      b.classList.remove('border-primary', 'text-primary', 'bg-primary/5');
    });
  });
})();


/* ── Toast Notifications ─────────────────────────────────────────────────── */
const TOAST_DURATION = 4500;

function showToast(text, type) {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const isError = type === 'error';
  const titles = { success: 'تمّ بنجاح', error: 'حدث خطأ' };
  const colors = isError
    ? { border: '#fca5a5', bar: '#ef4444', iconBg: '#fef2f2', iconColor: '#dc2626' }
    : { border: '#86efac', bar: '#22c55e', iconBg: '#f0fdf4', iconColor: '#16a34a' };

  const iconSvg = isError
    ? '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>'
    : '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M20 6L9 17l-5-5"/></svg>';

  const toast = document.createElement('div');
  toast.style.cssText = `
    position:relative;overflow:hidden;
    display:flex;align-items:center;gap:14px;
    padding:14px 16px;border-radius:16px;
    background:#fff;border:1px solid ${colors.border};
    box-shadow:0 10px 40px rgba(0,0,0,0.12);
    pointer-events:auto;min-width:300px;max-width:400px;
    opacity:0;transform:translateY(-20px) scale(0.97);
    transition:opacity 0.4s cubic-bezier(.22,1,.36,1),transform 0.4s cubic-bezier(.22,1,.36,1);
  `;

  toast.innerHTML = `
    <div style="width:40px;height:40px;border-radius:12px;background:${colors.iconBg};
                display:flex;align-items:center;justify-content:center;flex-shrink:0;color:${colors.iconColor};">
      ${iconSvg}
    </div>
    <div style="flex:1;min-width:0;">
      <div style="font-size:0.875rem;font-weight:700;color:#1a1a1a;margin-bottom:2px;">
        ${titles[type] || titles.success}
      </div>
      <div style="font-size:0.78rem;color:#6b7280;line-height:1.5;">${text}</div>
    </div>
    <button onclick="this.parentElement.remove()"
            style="width:24px;height:24px;border-radius:8px;border:none;background:transparent;
                   cursor:pointer;display:flex;align-items:center;justify-content:center;
                   color:#9ca3af;flex-shrink:0;font-size:1rem;line-height:1;padding:0;">✕</button>
    <div style="position:absolute;bottom:0;right:0;left:0;height:3px;background:#f3f4f6;">
      <div class="toast-bar" style="height:100%;background:${colors.bar};
           width:100%;transition:width ${TOAST_DURATION}ms linear;"></div>
    </div>
  `;

  container.appendChild(toast);

  requestAnimationFrame(() => {
    toast.style.opacity = '1';
    toast.style.transform = 'translateY(0) scale(1)';
    const bar = toast.querySelector('.toast-bar');
    if (bar) requestAnimationFrame(() => { bar.style.width = '0%'; });
  });

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(-16px) scale(0.97)';
    setTimeout(() => toast.remove(), 400);
  }, TOAST_DURATION);
}

// Fire toasts from server-rendered [data-toast] elements
setTimeout(function () {
  document.querySelectorAll('[data-toast]').forEach(function (el) {
    showToast(el.textContent.trim(), el.dataset.type || 'success');
  });
}, 100);



/* ── Mobile Nav Toggle ────────────────────────────────────────────────────── */
(function () {
  const btn = document.getElementById('mobile-menu-btn');
  const menu = document.getElementById('mobile-menu');
  if (!btn || !menu) return;

  btn.addEventListener('click', () => {
    menu.classList.toggle('hidden');
  });
})();
