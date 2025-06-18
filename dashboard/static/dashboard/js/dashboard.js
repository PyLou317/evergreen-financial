'use strict';

document.addEventListener('DOMContentLoaded', () => {
  const totalExpensesChart = document.getElementById('total-expense-chart');
  const monthlyIncomeChart = document.getElementById('monthly-income-chart');
  const totalIncomeChart = document.getElementById('total-income-chart');
  const expenseByMonthChart = document.getElementById('expense-by-month-chart');
  let myChart;

  // ------- Total Expense Chart ------- //
  fetch('/dashboard/category_expense_json/')
    .then((resp) => resp.json())
    .then((categoryExpensesData) => {
      // 'transactionsData' is now the JSON list from Django
      console.log('Fetched categoryExpenseData:', categoryExpensesData);

      const categoryLabels = categoryExpensesData.map((item) => item.category);
      const categoryExpenseTotals = categoryExpensesData.map((item) => parseFloat(item.total_expense));

      const backgroundColors = [
        'rgb(91, 155, 206)', // Muted Blue (#5B9BCE)
        'rgb(143, 184, 196)', // Desaturated Teal-Blue (#8FB8C4)
        'rgb(174, 197, 208)', // Light Gray-Blue (#AEC5D0)
        'rgb(176, 199, 185)', // Soft, Muted Gray-Green (#B0C7B9)
        'rgb(198, 216, 190)', // Lighter Desaturated Green (#C6D8BE)
        'rgb(217, 215, 210)', // Very Light, Neutral Warm Gray (#D9D7D2)
        'rgb(230, 230, 235)', // Very Light Cool Gray (#E6E6EB)
        'rgb(199, 169, 179)', // Very Soft Muted Rose (#C7A9B3)
        'rgb(123, 166, 199)', // Slightly deeper muted blue (#7BA6C7)
        'rgb(162, 191, 200)', // Mid-tone desaturated teal (#A2BFC8)
        'rgb(193, 209, 216)', // Cool light gray (#C1D1D8)
        'rgb(206, 221, 210)', // Pale desaturated green (#CEDDD2)
        'rgb(223, 233, 217)', // Very light greenish-gray (#DFE9D9)
        'rgb(235, 235, 208)', // Very light warm yellow-gray (#EBEBD0)
        'rgb(241, 241, 241)', // Off-white neutral gray (#F1F1F1)
        'rgb(158, 173, 196)', // Desaturated blue-gray (#9EADC4)
        'rgb(181, 199, 209)', // Pale, cool blue-gray (#B5C7D1)
        'rgb(204, 214, 204)', // Soft, very light green-gray (#CCD6CC)
        'rgb(217, 215, 224)', // Pale lavender-gray (#D9D7E0)
        'rgb(224, 219, 219)', // Light rosy gray (#E0DBDB)
      ];

      new Chart(totalExpensesChart, {
        type: 'doughnut',
        data: {
          labels: categoryLabels, // Use category labels for x-axis
          datasets: [
            {
              label: 'Total Expenses per Category', // Dataset label (for chart title/description)
              data: categoryExpenseTotals, // Expense totals for all categories (single dataset)
              backgroundColor: backgroundColors,
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              display: false,
              position: 'right',
            },
            tooltip: {
              enabled: true,
            },
          },
        },
      });
    });

  // ------- Monthly Income Chart ------- //
  fetch('/dashboard/income_total_json/')
    .then((resp) => resp.json())
    .then((monthlyIncomeData) => {
      console.log('Fetched monthlyIncomeData:', monthlyIncomeData);

      const categoryLabels = monthlyIncomeData.map((item) => item.month);
      const monthlyIncomeTotals = monthlyIncomeData.map((item) => parseFloat(item.total_income));

      const monthlyIncome = new Chart(monthlyIncomeChart, {
        type: 'line',
        data: {
          labels: categoryLabels,
          datasets: [
            {
              label: 'Total Income',
              data: monthlyIncomeTotals,
              borderWidth: 3,
              fill: {
                target: 'origin',
                above: 'rgb(91, 155, 206, 0.5)',
              },
              borderColor: 'rgb(91, 155, 206)',
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            x: {
              grid: {
                display: false,
              },
            },
            y: {
              beginAtZero: true,
              grid: {
                display: true,
              },
            },
          },
          plugins: {
            legend: {
              display: false,
            },
            tooltip: {
              usePointStyle: true,
              callbacks: {
                labelPointStyle: function (context) {
                  return {
                    pointStyle: 'triangle',
                    rotation: 0,
                  };
                },
                labelColor: function (context) {
                  return {
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgb(75, 192, 192)',
                    borderWidth: 2,
                    borderDash: [2, 2],
                    borderRadius: 2,
                  };
                },
              },
            },
          },
        },
      });
    });

  const monthSelector = document.getElementById('month-selector');

  if (monthSelector) {
    monthSelector.addEventListener('change', renderChart); // Use renderChart function
    renderChart(); // Initial chart render
  }

  function getSelectedMonth() {
    return monthSelector ? monthSelector.value : null;
  }

  // ------- Monthly Expense Chart ------- //
  function renderChart() {
    fetch('/dashboard/monthly_expense_json/')
      .then((resp) => resp.json())
      .then((monthlyExpenseData) => {
        // Filter data by selected month
        const selectedMonth = getSelectedMonth();
        const filteredData = monthlyExpenseData.filter((item) => item.month === selectedMonth);

        const labels = new Set(filteredData.map((row) => row.month));
        // Create Labels
        const uniqueMonthLabels = filteredData.reduce((uniqueMonths, item) => {
          if (!uniqueMonths.includes(item.month)) {
            uniqueMonths.push(item.month);
          }
          return uniqueMonths;
        }, []);

        const datasets = [];
        const categoryExpenseMap = {}; // To group expenses by category

        // Group expenses by category
        filteredData.forEach((item) => {
          const category = item.category;
          const month = item.month;
          const totalExpense = item.total_expense;

          if (!categoryExpenseMap[category]) {
            categoryExpenseMap[category] = {}; // Initialize category if not present
          }
          // Take the absolute value of expense totals for chart display:
          categoryExpenseMap[category][month] = Math.abs(totalExpense); // Store expense for month in category map as absolute value
        });

        const colors = [
          'rgb(91, 155, 206)', // Muted Blue (#5B9BCE)
          'rgb(143, 184, 196)', // Desaturated Teal-Blue (#8FB8C4)
          'rgb(174, 197, 208)', // Light Gray-Blue (#AEC5D0)
          'rgb(176, 199, 185)', // Soft, Muted Gray-Green (#B0C7B9)
          'rgb(198, 216, 190)', // Lighter Desaturated Green (#C6D8BE)
          'rgb(217, 215, 210)', // Very Light, Neutral Warm Gray (#D9D7D2)
          'rgb(230, 230, 235)', // Very Light Cool Gray (#E6E6EB)
          'rgb(199, 169, 179)', // Very Soft Muted Rose (#C7A9B3)
          'rgb(123, 166, 199)', // Slightly deeper muted blue (#7BA6C7)
          'rgb(162, 191, 200)', // Mid-tone desaturated teal (#A2BFC8)
          'rgb(193, 209, 216)', // Cool light gray (#C1D1D8)
          'rgb(206, 221, 210)', // Pale desaturated green (#CEDDD2)
          'rgb(223, 233, 217)', // Very light greenish-gray (#DFE9D9)
          'rgb(235, 235, 208)', // Very light warm yellow-gray (#EBEBD0)
          'rgb(241, 241, 241)', // Off-white neutral gray (#F1F1F1)
          'rgb(158, 173, 196)', // Desaturated blue-gray (#9EADC4)
          'rgb(181, 199, 209)', // Pale, cool blue-gray (#B5C7D1)
          'rgb(204, 214, 204)', // Soft, very light green-gray (#CCD6CC)
          'rgb(217, 215, 224)', // Pale lavender-gray (#D9D7E0)
          'rgb(224, 219, 219)', // Light rosy gray (#E0DBDB)
        ];

        let i = 0;

        // Create datasets from categoryExpenseMap
        for (const categoryName in categoryExpenseMap) {
          const monthlyExpenseMapForCategory = categoryExpenseMap[categoryName];
          const expenseDataForChart = uniqueMonthLabels.map((monthLabel, monthIndex) => {
            const monthString = monthLabel;
            return monthlyExpenseMapForCategory[monthString] || 0; // Get expense for this month or 0 if no data
          });

          datasets.push({
            label: categoryName,
            data: expenseDataForChart,
            backgroundColor: colors[i % colors.length],
            borderColor: colors[i % colors.length],
            borderWidth: 1,
          });
          i++;
        }
        console.log(datasets);

        // Destroy blank  chart to allow for a new cahrt to render with data
        if (myChart) {
          myChart.destroy();
        }

        myChart = new Chart(expenseByMonthChart, {
          type: 'bar',
          data: {
            labels: uniqueMonthLabels,
            datasets: datasets,
          },
          options: {
            tooltip: {
              enabled: true,
            },
              responsive: true,
              scales: {
                  y: {
                      type: 'logarithmic',
                    }
              },
            plugins: {
              legend: {
                display: true,
                position: 'left',
              },
            },
          },
        });
      });
  }
});
