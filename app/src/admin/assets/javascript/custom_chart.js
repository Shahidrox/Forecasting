import '/src/admin/assets/javascript/chart.js'

$("#inputState").on("change", function() {
  var slug = $(this).val();
  handleChart(slug);
});

var handleChart = function(slug) {
  if(slug == "") {
    return;
  }
  $.ajax({
    url: "/forecasting/"+slug,
    type: "GET",
    success: function(data) {
      if(window.forecastedChart){
        window.forecastedChart.destroy();
      }

      var html_id = document.getElementById("chart-user-acquisition"); // Get the canvas element
      var ctx = html_id.getContext('2d'); // Get the context of the canvas element
      window.forecastedChart = new Chart(ctx, {
        // type: 'bar', // Vertical bar chart
        type: 'line', // Line chart
        data: {
          labels: data.months, // X-axis labels
          datasets: [{
            label: 'Forecasted Inventory',
            data: data.forecasted_inventory, // Data points
            backgroundColor: 'rgba(54, 162, 235, 0.2)', // Bar color
            borderColor: 'rgba(54, 162, 235, 1)', // Bar border color
            borderWidth: 1 // Border width
          }]
        },
        options: {
          scales: {
            x: {
              ticks: {
                color: 'white' // X-axis font color
              },
              grid: {
                color: 'rgba(255, 255, 255, 0.2)' // X-axis grid line color
              }
            },
            y: {
              ticks: {
                color: 'white' // Y-axis font color
              },
              grid: {
                color: 'rgba(255, 255, 255, 0.2)' // Y-axis grid line color
              }
            }
          },
          plugins: {
            legend: {
              labels: {
                color: 'white' // Legend font color
              }
            },
            tooltip: {
              callbacks: {
                title: function(tooltipItems) {
                  return tooltipItems[0].label;
                },
                label: function(tooltipItem) {
                  return tooltipItem.label + ': ' + tooltipItem.raw;
                }
              },
              titleColor: 'white', // Tooltip title color
              bodyColor: 'white' // Tooltip body color
            }
          }
        }
      });
    },
    error: function(err) {
      console.log(err);
    }
  });
}

var handleUploadCsv = function() {
  var fileInput = document.getElementById('csvFileInput');
  fileInput.addEventListener('change', function(event) {
    var file = event.target.files[0];
    if (file) {
      $('#page-loader').removeClass('opacity-0').addClass('opacity-1');
      var formData = new FormData();
      formData.append('file', file);
      $.ajax({
        url: '/train_model',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
          alert(response.message)
          window.location.reload();
        },
        error: function(error) {
          alert(error.responseJSON.message)
        },
          complete: function() {
            $('#page-loader').removeClass('opacity-1').addClass('opacity-0')
          }
      });
    } else {
      throw new Error('No file selected');
    }
  });
}

var FormPlugins = function() {
  "use strict";
  return {
    init: function() {
      let slug = $("#inputState").val();
      handleChart(slug);
      handleUploadCsv()
    }
  };
}();

$(document).ready(function() {
  FormPlugins.init();
});



// let t=document.getElementById("list-user-acquisition")
// let data = [
// {source:"Organic Search",color:"bg-primary",visits:243.2,percentage:32.4,opacity:1,up:!0}
// ]
// let e = ""
// data.forEach(l=>{
// e+=`<div class="d-flex align-items-start">
    // <i class="w-2.5 h-2.5 mt-1.5 rounded-circle me-3 ${l.color}"></i>
        // <div class="flex-grow-1 d-flex align-items-center flex-wrap">
        // <div class="flex-grow-1">${l.source}</div>
        // <div class="fs-5 fw-medium text-end w-14">${l.visits}</div>
        // <div class="w-20 text-end d-none d-sm-block">
        // <div class="badge rounded-pill fs-8 ms-auto text-body-emphasis d-inline-flex align-items-center mt-n1 bg-success bg-opacity-50 ${l.up?"bg-success":"bg-danger"}">
            // ${l.percentage}%
            // <i class="ph fs-5 ms-1 ${l.up?"ph-arrow-circle-up":"ph-arrow-circle-down"}"></i>
        // </div>
        // </div>
        // <div class="progress w-100 my-4 h-0.5" role="progressbar" aria-valuenow="${l.percentage}" aria-valuemin="0" aria-valuemax="100">
        // <div class="progress-bar ${l.color}" style="width: ${l.percentage}%"></div>
        // </div>
    // </div>
    // </div>`,
    // t.innerHTML=e
// })