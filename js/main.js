// Expand/Collapse
document.addEventListener('click', function(e) {
  const header = e.target.closest('.expand-header');
  if (!header) return;
  const body = header.nextElementSibling;
  const arrow = header.querySelector('.expand-arrow');
  if (body) body.classList.toggle('open');
  if (arrow) arrow.classList.toggle('open');
});

// Mark active nav link
document.addEventListener('DOMContentLoaded', function() {
  const path = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.top-nav .nav-links a').forEach(a => {
    const href = a.getAttribute('href').split('/').pop();
    if (href === path) a.classList.add('active');
  });
});
