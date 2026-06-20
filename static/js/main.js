// ===== CropSense v2.0 — Main JS =====

// Auto-dismiss flash messages (toast style)
document.addEventListener('DOMContentLoaded', () => {
    const flashes = document.querySelectorAll('.flash');
    flashes.forEach(f => {
        setTimeout(() => {
            f.style.transition = 'all 0.4s ease';
            f.style.opacity = '0';
            f.style.transform = 'translateY(10px)';
            setTimeout(() => f.remove(), 400);
        }, 4000);
    });
});

// ===== TOAST SYSTEM =====
function showToast(msg, type = 'success') {
    const container = document.getElementById('flash-container') || (() => {
        const c = document.createElement('div');
        c.id = 'flash-container';
        c.className = 'flash-container';
        document.body.appendChild(c);
        return c;
    })();

    const icons = { success: 'check', danger: 'alert-circle', warning: 'alert-triangle', info: 'info-circle' };
    const toast = document.createElement('div');
    toast.className = `flash flash-${type}`;
    toast.innerHTML = `<i class="ti ti-${icons[type] || 'info-circle'}"></i> ${msg}`;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.transition = 'all 0.4s ease';
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(10px)';
        setTimeout(() => toast.remove(), 400);
    }, 3500);
}

// ===== SIDEBAR TOGGLE (mobile) =====
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    if (sidebar) sidebar.classList.toggle('open');
}

// Close sidebar when clicking outside on mobile
document.addEventListener('click', (e) => {
    const sidebar = document.getElementById('sidebar');
    const btn = document.querySelector('.mobile-menu-btn');
    if (sidebar && sidebar.classList.contains('open')) {
        if (!sidebar.contains(e.target) && e.target !== btn && !btn?.contains(e.target)) {
            sidebar.classList.remove('open');
        }
    }
});

// ===== PDF EXPORT =====
function downloadPDFReport() {
    // Show loading toast
    showToast('Generating your PDF report...', 'info');

    // Hit the backend PDF endpoint
    fetch('/farmer/report/pdf', { method: 'GET' })
        .then(res => {
            if (!res.ok) throw new Error('Server error');
            return res.blob();
        })
        .then(blob => {
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `CropSense_Report_${new Date().toISOString().slice(0,10)}.pdf`;
            document.body.appendChild(a);
            a.click();
            a.remove();
            URL.revokeObjectURL(url);
            showToast('PDF downloaded successfully!', 'success');
        })
        .catch(() => {
            // Fallback: open print dialog (browser-native PDF)
            showToast('Opening print dialog for PDF export...', 'warning');
            setTimeout(() => window.print(), 500);
        });
}

// ===== CONFIRM BEFORE DESTRUCTIVE ACTIONS =====
document.querySelectorAll('[data-confirm]').forEach(el => {
    el.addEventListener('click', e => {
        if (!confirm(el.dataset.confirm)) e.preventDefault();
    });
});

// ===== NUMBER COUNTER ANIMATION for stat cards =====
function animateCounter(el, target, duration = 1200) {
    const start = 0;
    const startTime = performance.now();
    const isFloat = target % 1 !== 0;

    function update(now) {
        const elapsed = now - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = start + (target - start) * eased;
        el.textContent = isFloat ? current.toFixed(2) : Math.floor(current);
        if (progress < 1) requestAnimationFrame(update);
    }
    requestAnimationFrame(update);
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.stat-value').forEach(el => {
        const raw = parseFloat(el.textContent);
        if (!isNaN(raw) && raw > 0) {
            el.textContent = '0';
            setTimeout(() => animateCounter(el, raw), 300);
        }
    });
});

// ===== TABLE SORT =====
document.querySelectorAll('th[data-sort]').forEach(th => {
    th.style.cursor = 'pointer';
    th.addEventListener('click', () => {
        const table = th.closest('table');
        const idx = Array.from(th.parentElement.children).indexOf(th);
        const asc = th.dataset.order !== 'asc';
        th.dataset.order = asc ? 'asc' : 'desc';
        const rows = Array.from(table.querySelectorAll('tbody tr'));
        rows.sort((a, b) => {
            const va = a.cells[idx]?.textContent.trim() || '';
            const vb = b.cells[idx]?.textContent.trim() || '';
            const na = parseFloat(va), nb = parseFloat(vb);
            if (!isNaN(na) && !isNaN(nb)) return asc ? na - nb : nb - na;
            return asc ? va.localeCompare(vb) : vb.localeCompare(va);
        });
        rows.forEach(r => table.querySelector('tbody').appendChild(r));
    });
});

// CropSense v3.0 additions

// Flash auto-dismiss (3s for success/info, stays for danger/warning)
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.flash.flash-success, .flash.flash-info').forEach(el => {
        setTimeout(() => el.style.opacity = '0', 3000);
        setTimeout(() => el.remove(), 3400);
    });
});
