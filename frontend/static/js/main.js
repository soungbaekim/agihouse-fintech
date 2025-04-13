// Main JavaScript for Finance Analyzer

document.addEventListener('DOMContentLoaded', function() {
  // Initialize any charts if they exist on the page
  initializeCharts();
  
  // Add event listeners for interactive elements
  setupEventListeners();
});

// Initialize charts based on available data
function initializeCharts() {
  // Check if we're on a page with charts
  if (document.getElementById('spending-by-category-chart')) {
    // Parse any chart data from the page
    const chartDataElement = document.getElementById('chart-data');
    if (chartDataElement) {
      try {
        const chartData = JSON.parse(chartDataElement.textContent);
        createSpendingByCategoryChart(chartData.spending_by_category);
        createMonthlySpendingChart(chartData.monthly_spending);
      } catch (e) {
        console.error('Error parsing chart data:', e);
      }
    }
  }
}

// Create spending by category pie chart
function createSpendingByCategoryChart(data) {
  const ctx = document.getElementById('spending-by-category-chart').getContext('2d');
  
  // Extract categories and amounts
  const categories = Object.keys(data);
  const amounts = Object.values(data);
  
  // Generate colors
  const colors = categories.map((_, i) => 
    `hsl(${(i * 360 / categories.length) % 360}, 70%, 60%)`
  );
  
  new Chart(ctx, {
    type: 'pie',
    data: {
      labels: categories,
      datasets: [{
        data: amounts,
        backgroundColor: colors,
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'right',
        },
        title: {
          display: true,
          text: 'Spending by Category'
        }
      }
    }
  });
}

// Create monthly spending bar chart
function createMonthlySpendingChart(data) {
  if (!document.getElementById('monthly-spending-chart')) return;
  
  const ctx = document.getElementById('monthly-spending-chart').getContext('2d');
  
  // Extract months and category data
  const months = Object.keys(data);
  const categories = new Set();
  
  // Find all unique categories
  months.forEach(month => {
    Object.keys(data[month]).forEach(category => {
      categories.add(category);
    });
  });
  
  // Prepare datasets
  const categoryArray = Array.from(categories);
  const datasets = categoryArray.map((category, index) => {
    return {
      label: category,
      data: months.map(month => data[month][category] || 0),
      backgroundColor: `hsl(${(index * 360 / categoryArray.length) % 360}, 70%, 60%)`,
      borderColor: `hsl(${(index * 360 / categoryArray.length) % 360}, 70%, 50%)`,
      borderWidth: 1
    };
  });
  
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: months,
      datasets: datasets
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          stacked: true
        },
        y: {
          stacked: true,
          beginAtZero: true
        }
      },
      plugins: {
        title: {
          display: true,
          text: 'Monthly Spending by Category'
        }
      }
    }
  });
}

// Set up event listeners for interactive elements
function setupEventListeners() {
  // File upload preview
  const fileInput = document.getElementById('fileInput');
  if (fileInput) {
    fileInput.addEventListener('change', function() {
      const fileNameDisplay = document.getElementById('selectedFileName');
      if (fileNameDisplay) {
        fileNameDisplay.textContent = this.files[0] ? this.files[0].name : 'No file selected';
      }
    });
  }
  
  // Collapsible sections
  const collapsibles = document.querySelectorAll('.collapsible-header');
  collapsibles.forEach(header => {
    header.addEventListener('click', function() {
      this.classList.toggle('active');
      const content = this.nextElementSibling;
      if (content.style.maxHeight) {
        content.style.maxHeight = null;
      } else {
        content.style.maxHeight = content.scrollHeight + 'px';
      }
    });
  });
  
  // Add file validation for uploads
  const uploadForm = document.getElementById('uploadForm');
  if (uploadForm) {
    uploadForm.addEventListener('submit', function(e) {
      const fileInput = document.getElementById('fileInput');
      if (fileInput && fileInput.files.length === 0) {
        e.preventDefault();
        alert('Please select a file to upload.');
      }
    });
  }
}

// Toggle between views if needed
function toggleView(viewId) {
  const views = document.querySelectorAll('.view-container');
  views.forEach(view => {
    view.style.display = 'none';
  });
  
  document.getElementById(viewId).style.display = 'block';
}

// Format currency values
function formatCurrency(value) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(value);
}

// Format percentage values
function formatPercentage(value) {
  return new Intl.NumberFormat('en-US', {
    style: 'percent',
    minimumFractionDigits: 1,
    maximumFractionDigits: 1
  }).format(value / 100);
}
