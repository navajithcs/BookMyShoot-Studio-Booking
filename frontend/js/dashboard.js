/* ═══════════════════════════════════════════════════════════
   BookMyShoot — Dashboard Utilities v2.0
   Shared JS for dark mode, toasts, search, export, etc.
   ═══════════════════════════════════════════════════════════ */

const DashApp = (() => {
  const API_URL = 'http://localhost:5000/api';

  /* ── Dark Mode ── */
  function initTheme() {
    const saved = localStorage.getItem('bms-theme') || 'light';
    document.documentElement.setAttribute('data-theme', saved);
    updateThemeIcon(saved);
  }

  function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme') || 'light';
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('bms-theme', next);
    updateThemeIcon(next);
  }

  function updateThemeIcon(theme) {
    document.querySelectorAll('.theme-toggle').forEach(btn => {
      const moon = btn.querySelector('.icon-moon');
      const sun = btn.querySelector('.icon-sun');
      if (moon && sun) {
        moon.style.display = theme === 'dark' ? 'none' : 'inline';
        sun.style.display = theme === 'dark' ? 'inline' : 'none';
      }
    });
  }

  /* ── Toast System ── */
  let toastContainer = null;
  function ensureToastContainer() {
    if (!toastContainer) {
      toastContainer = document.createElement('div');
      toastContainer.className = 'toast-container';
      document.body.appendChild(toastContainer);
    }
  }

  function showToast(title, message, type = 'info', duration = 4000) {
    ensureToastContainer();
    const icons = {
      success: '✓', warning: '⚠', danger: '✕', info: 'ℹ'
    };
    const colors = {
      success: 'var(--success-500)', warning: 'var(--warning-500)',
      danger: 'var(--danger-500)', info: 'var(--brand-500)'
    };
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `
      <span class="toast-icon" style="color:${colors[type] || colors.info}">${icons[type] || icons.info}</span>
      <div class="toast-body">
        <div class="toast-title">${escapeHtml(title)}</div>
        ${message ? `<div class="toast-message">${escapeHtml(message)}</div>` : ''}
      </div>
      <button class="toast-close" onclick="this.closest('.toast').remove()">×</button>
    `;
    toastContainer.appendChild(toast);
    if (duration > 0) {
      setTimeout(() => {
        toast.classList.add('removing');
        setTimeout(() => toast.remove(), 200);
      }, duration);
    }
    return toast;
  }

  /* ── Sidebar Toggle (mobile) ── */
  function initSidebar() {
    const toggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('dashSidebar');
    const overlay = document.getElementById('sidebarOverlay');

    if (toggle && sidebar) {
      toggle.addEventListener('click', () => {
        sidebar.classList.toggle('open');
        if (overlay) overlay.classList.toggle('show');
      });
    }
    if (overlay && sidebar) {
      overlay.addEventListener('click', () => {
        sidebar.classList.remove('open');
        overlay.classList.remove('show');
      });
    }
    // Close sidebar on link click (mobile)
    document.querySelectorAll('.sidebar-link').forEach(link => {
      link.addEventListener('click', () => {
        if (window.innerWidth <= 768 && sidebar) {
          sidebar.classList.remove('open');
          if (overlay) overlay.classList.remove('show');
        }
      });
    });
  }

  /* ── Notification Panel ── */
  function initNotifPanel() {
    const btn = document.getElementById('notifBtn');
    const panel = document.getElementById('notifPanel');
    const overlay = document.getElementById('notifOverlay');
    const closeBtn = document.getElementById('notifClose');

    const open = () => { panel?.classList.add('open'); overlay?.classList.add('show'); };
    const close = () => { panel?.classList.remove('open'); overlay?.classList.remove('show'); };

    if (btn) btn.addEventListener('click', open);
    if (closeBtn) closeBtn.addEventListener('click', close);
    if (overlay) overlay.addEventListener('click', close);
  }

  /* ── User Dropdown ── */
  function initUserDropdown() {
    const trigger = document.getElementById('userDropdownTrigger');
    const menu = document.getElementById('userDropdown');
    if (!trigger || !menu) return;

    trigger.addEventListener('click', (e) => {
      e.stopPropagation();
      menu.closest('.dropdown').classList.toggle('open');
    });
    document.addEventListener('click', () => {
      menu.closest('.dropdown')?.classList.remove('open');
    });
  }

  /* ── Global Search ── */
  function initSearch(onSearch) {
    const searchInput = document.getElementById('globalSearch');
    if (!searchInput) return;
    let debounceTimer;
    searchInput.addEventListener('input', (e) => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        if (typeof onSearch === 'function') onSearch(e.target.value);
      }, 300);
    });
    // Keyboard shortcut: Ctrl+K or Cmd+K
    document.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        searchInput.focus();
      }
    });
  }

  /* ── Data Export ── */
  function exportCSV(data, filename = 'export.csv') {
    if (!data || !data.length) {
      showToast('Export', 'No data to export', 'warning');
      return;
    }
    const headers = Object.keys(data[0]);
    const csv = [
      headers.join(','),
      ...data.map(row => headers.map(h => {
        let val = row[h] ?? '';
        val = String(val).replace(/"/g, '""');
        return `"${val}"`;
      }).join(','))
    ].join('\n');

    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();
    URL.revokeObjectURL(link.href);
    showToast('Export Complete', `${data.length} rows exported as CSV`, 'success');
  }

  /* ── Pagination ── */
  function createPagination(containerId, totalItems, currentPage, pageSize, onPageChange) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const totalPages = Math.ceil(totalItems / pageSize);
    if (totalPages <= 1) { container.innerHTML = ''; return; }

    let html = `<div class="pagination">`;
    html += `<button class="page-btn" ${currentPage <= 1 ? 'disabled' : ''} onclick="event.preventDefault();" data-page="${currentPage - 1}">←</button>`;

    const range = getPageRange(currentPage, totalPages);
    range.forEach(p => {
      if (p === '...') {
        html += `<span class="page-btn" style="pointer-events:none;border:none;">…</span>`;
      } else {
        html += `<button class="page-btn ${p === currentPage ? 'active' : ''}" data-page="${p}">${p}</button>`;
      }
    });

    html += `<button class="page-btn" ${currentPage >= totalPages ? 'disabled' : ''} data-page="${currentPage + 1}">→</button>`;
    html += `</div>`;

    container.innerHTML = html;
    container.querySelectorAll('.page-btn[data-page]').forEach(btn => {
      btn.addEventListener('click', () => {
        const page = parseInt(btn.dataset.page);
        if (page >= 1 && page <= totalPages && typeof onPageChange === 'function') {
          onPageChange(page);
        }
      });
    });
  }

  function getPageRange(current, total) {
    if (total <= 7) return Array.from({ length: total }, (_, i) => i + 1);
    if (current <= 3) return [1, 2, 3, 4, '...', total];
    if (current >= total - 2) return [1, '...', total - 3, total - 2, total - 1, total];
    return [1, '...', current - 1, current, current + 1, '...', total];
  }

  /* ── Table Sorting ── */
  function initSortableTable(tableId, data, renderFn) {
    const table = document.getElementById(tableId);
    if (!table) return;

    let sortCol = null;
    let sortDir = 'asc';

    table.querySelectorAll('th.sortable').forEach(th => {
      th.addEventListener('click', () => {
        const col = th.dataset.sort;
        if (sortCol === col) {
          sortDir = sortDir === 'asc' ? 'desc' : 'asc';
        } else {
          sortCol = col;
          sortDir = 'asc';
        }

        // Update UI
        table.querySelectorAll('th.sortable').forEach(t => {
          t.classList.remove('sorted-asc', 'sorted-desc');
        });
        th.classList.add(`sorted-${sortDir}`);

        // Sort data
        const sorted = [...data].sort((a, b) => {
          let va = a[col], vb = b[col];
          if (typeof va === 'string') va = va.toLowerCase();
          if (typeof vb === 'string') vb = vb.toLowerCase();
          if (va < vb) return sortDir === 'asc' ? -1 : 1;
          if (va > vb) return sortDir === 'asc' ? 1 : -1;
          return 0;
        });

        if (typeof renderFn === 'function') renderFn(sorted);
      });
    });
  }

  /* ── Counter Animation ── */
  function animateValue(el, target, duration = 1200) {
    if (!el) return;
    const start = parseInt(el.textContent) || 0;
    const diff = target - start;
    const startTime = performance.now();

    function tick(now) {
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
      el.textContent = Math.round(start + diff * eased);
      if (progress < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  /* ── Auth Guard ── */
  function getUser() {
    try { return JSON.parse(localStorage.getItem('user')); } catch { return null; }
  }

  function requireAuth(allowedRoles = []) {
    const user = getUser();
    if (!user) { window.location.href = 'login.html'; return null; }
    if (allowedRoles.length && !allowedRoles.includes(user.user_type)) {
      window.location.href = 'index.html';
      return null;
    }
    return user;
  }

  function logout() {
    const user = getUser();
    if (user) {
      fetch(`${API_URL}/logout`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: user.id })
      }).catch(() => {});
    }
    localStorage.removeItem('user');
    window.location.href = 'login.html';
  }

  /* ── Loader ── */
  function showLoader(show) {
    const el = document.getElementById('pageLoader');
    if (el) el.classList.toggle('show', show);
  }

  /* ── Date Formatting ── */
  function formatDate(dateStr) {
    if (!dateStr) return '—';
    const d = new Date(dateStr);
    return d.toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' });
  }

  function formatCurrency(amount) {
    return '₹' + Number(amount || 0).toLocaleString('en-IN');
  }

  function timeAgo(dateStr) {
    if (!dateStr) return '';
    const now = new Date();
    const past = new Date(dateStr);
    const diff = (now - past) / 1000;
    if (diff < 60) return 'Just now';
    if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
    if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
    if (diff < 604800) return `${Math.floor(diff / 86400)}d ago`;
    return formatDate(dateStr);
  }

  /* ── HTML Safety ── */
  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  /* ── Auto-init ── */
  function init(opts = {}) {
    initTheme();
    initSidebar();
    initNotifPanel();
    initUserDropdown();
    if (opts.onSearch) initSearch(opts.onSearch);

    // Wire theme toggles
    document.querySelectorAll('.theme-toggle').forEach(btn => {
      btn.addEventListener('click', toggleTheme);
    });

    // Keyboard ESC to close panels
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        document.getElementById('notifPanel')?.classList.remove('open');
        document.getElementById('notifOverlay')?.classList.remove('show');
        document.querySelectorAll('.dropdown.open').forEach(d => d.classList.remove('open'));
      }
    });
  }

  // Public API
  return {
    API_URL,
    init,
    toggleTheme,
    showToast,
    showLoader,
    exportCSV,
    createPagination,
    initSortableTable,
    animateValue,
    getUser,
    requireAuth,
    logout,
    formatDate,
    formatCurrency,
    timeAgo,
    escapeHtml,
    initSearch
  };
})();
