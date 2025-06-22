'use_strict';

function toggleSidebar() {
  const sidebar = document.querySelector('.sidebar');
  const logoText = document.querySelector('.logo-text');
  sidebar.classList.toggle('collapsed');
  logoText.classList.toggle('hide');
}

document.addEventListener('DOMContentLoaded', () => {
    function highlightActiveLink() {
        const dashboardLink = document.getElementById('dashboard-link')
        const transactionsLink = document.getElementById('transactions-link')
        const uploadLink = document.getElementById('upload-link')
        const reportsLink = document.getElementById('reports-link')

        const pathName = window.location.pathname;
        const pageName = pathName.split("/")[1]

        if (pageName == 'dashboard') {
            dashboardLink.classList.toggle('active');
        }
        if (pageName == 'transactions') {
            transactionsLink.classList.toggle('active');
        }
        if (pageName == 'upload') {
            uploadLink.classList.toggle('active');
        }
        if (pageName == 'reports') {
            reportsLink.classList.toggle('active');
        }

    }

    highlightActiveLink();
});