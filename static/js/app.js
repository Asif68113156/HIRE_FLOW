document.addEventListener('DOMContentLoaded', () => {
    // Initialize Boostrap Toasts
    var toastElList = [].slice.call(document.querySelectorAll('.toast'));
    var toastList = toastElList.map(function(toastEl) {
        return new bootstrap.Toast(toastEl, { autohide: true, delay: 5000 });
    });

    // Make the add candidate form slightly more dynamic on mobile
    const moveBtn = document.querySelector('form button[type="submit"]');
    if (moveBtn) {
        document.querySelectorAll('form').forEach(f => {
            f.addEventListener('submit', () => {
                const b = f.querySelector('button[type="submit"]');
                if (b) {
                    b.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...';
                    b.disabled = true;
                }
            });
        });
    }
});
