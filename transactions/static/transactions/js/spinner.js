'use_strict';

// let spinnerTimeout;

export function showSpinner() {
  const statContainers = document.querySelectorAll('.db-card .card-body');
  const statSpinners = document.querySelectorAll('.spinner-for-stat');
  const statDataDisplays = document.querySelectorAll('.stat-data');

  const tableSpinner = document.querySelector('.spinner-for-table');
  const tableDataContainer = document.querySelector('#transaction-table');

  const datas = document.querySelectorAll('.data');
  const spinners = document.querySelectorAll('.loader-div');

  // --- Show Spinners and Hide Data for Stat Bars ---
  if (statSpinners.length > 0 && statSpinners.length === statDataDisplays.length) {
    for (let i = 0; i < statSpinners.length; i++) {
      console.log(`spinner ${i + 1} loaded`);
      statSpinners[i].style.display = 'flex';
      statDataDisplays[i].style.display = 'none';
      statDataDisplays[i].textContent = '';
    }
  } else {
    console.warn("showSpinner: Stat bar spinners and/or data displays not found or counts don't match.");
  }
  // --- Show Spinner and Hide Data for Main Table ---
  if (tableSpinner && tableDataContainer) {
    tableSpinner.style.display = 'flex';
    tableDataContainer.style.display = 'none';
  } else {
    console.warn('showSpinner: Main table spinner or data container not found.');
  }

  console.log('All relevant spinners shown and data hidden.');
}

export function hideSpinner() {
  const statSpinners = document.querySelectorAll('.spinner-for-stat');
  const statDataDisplays = document.querySelectorAll('.stat-data');

  const tableSpinner = document.querySelector('.spinner-for-table');
  const tableDataContainer = document.querySelector('#transaction-table');

  const datas = document.querySelectorAll('.data');
  const spinners = document.querySelectorAll('.loader-div');

  setTimeout(() => {
    if (statSpinners.length > 0 && statSpinners.length === statDataDisplays.length) {
      for (let i = 0; i < statSpinners.length; i++) {
        statSpinners[i].style.display = 'none'; // Hide stat spinner
        statDataDisplays[i].style.display = 'block'; // Show stat data display
      }
    }

    // --- Hide Spinner and Show Data for Main Table ---
    if (tableSpinner && tableDataContainer) {
      tableSpinner.style.display = 'none';
      tableDataContainer.style.display = 'block';
    }

    console.log('All relevant spinners hidden and data shown after delay.');
  }, 1000);
}

export function forceHideSpinner() {
  const spinners = document.querySelectorAll('.loader-div');
  if (spinners) {
    for (const spinner of spinners) {
      clearTimeout(spinnerTimeout);
      spinner.classList.add = 'visually-hidden';
    }
  }
}
