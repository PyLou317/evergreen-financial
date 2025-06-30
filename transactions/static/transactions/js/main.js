import { fetchData } from './API.js';
import { renderHTML, renderStatsBar } from './UI.js';
import { showSpinner, forceHideSpinner, hideSpinner } from './spinner.js';
import { setupPagination } from './pagination.js';
import { getCategories } from './category_filters.js';

document.addEventListener('DOMContentLoaded', () => {
  const apiUrl = '/transactions/transactions_api/';
  const pageData = document.querySelector('.data');
  const tableContent = document.querySelector('[transaction-row-container]');
  const previousPageBtn = document.querySelector('.previous-page a.previousUrl');
  const nextPageBtn = document.querySelector('.next-page a.nextUrl');
  const searchInput = document.querySelector('[transaction-search-bar]');

  showSpinner();

  // Debounce function (from lodash)
  function debounce(func, delay) {
    let timeoutId;
    return function (...args) {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => {
        func.apply(this, args);
      }, delay);
    };
  }

  async function main(url = apiUrl) {
    try {
      const data = await fetchData(url);
      getCategories(data.categories);
      hideSpinner();
      renderStatsBar(data.stats);
      renderHTML(data.results);
      setupPagination(data, main);

      const categoryFilters = document.querySelectorAll('.category-filter-badge');
      const clearFilterBtn = document.querySelector('.clear-filter-btn');

      categoryFilters.forEach((button) => {
        button.addEventListener('click', async () => {
          const categoryName = button.textContent;
          const filterBtn = document.querySelector('.filter-badge');
          const btnColor = getComputedStyle(filterBtn).getPropertyValue('--accent-color');

          categoryFilters.forEach((btn) => {
            btn.style.backgroundColor = '';
            btn.style.backgroundImage = '';
          });
          button.style.backgroundImage = btnColor;

          const params = new URLSearchParams();
          params.append('category', categoryName);
          const filterUrl = `${apiUrl}?${params.toString()}`;

          clearFilterBtn.classList.remove('hidden');
          filterBtn.classList.add('hidden');

          try {
            const filterData = await fetchData(filterUrl);
            if (clearFilterBtn) {
              clearFilterBtn.addEventListener('click', () => {
                main();
                categoryFilters.forEach((btn) => {
                  btn.style.backgroundColor = '';
                  btn.style.backgroundImage = '';
                });
                clearFilterBtn.classList.add('hidden');
                filterBtn.classList.remove('hidden');
              });
            }
            renderStatsBar(filterData.stats);
            renderHTML(filterData.results);
            setupPagination(filterData, main);
            hideSpinner();
          } catch (error) {
            console.log('Error fetching filtered data:', error);
            forceHideSpinner();
          }
        });
      });
    } catch (error) {
      console.log('Error fetching Data:', error);
    }
  }

  // ----- Search Function ----- //
  const handleSearch = debounce((event) => {
    const searchTerm = event.target.value.trim();
    const searchUrl = searchTerm ? `${apiUrl}?search=${searchTerm}` : apiUrl;
    main(searchUrl);
  }, 300);

  searchInput.addEventListener('input', handleSearch);

  // ----- Pagination Controls ----- //
  previousPageBtn.addEventListener('click', (event) => {
    event.preventDefault();
    if (previousPageBtn.parentElement.classList.contains('disabled')) {
      return;
    }
    const previousUrl = previousPageBtn.href;
    if (previousUrl) {
      main(previousUrl);
    }
  });

  nextPageBtn.addEventListener('click', (event) => {
    event.preventDefault();
    if (nextPageBtn.parentElement.classList.contains('disabled')) {
      return;
    }
    const nextUrl = nextPageBtn.href;
    if (nextUrl) {
      main(nextUrl);
    }
  });

  main();
});
