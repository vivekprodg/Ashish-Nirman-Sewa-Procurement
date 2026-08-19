/* ==========================================================================
   ASHISH NIRMAN SEWA - DASHBOARD INTERACTIVE SCRIPT
   ========================================================================== */

$(document).ready(function() {
  
  // 1. Calculate and Animate Reservoir Fuel Progress Bars
  function initReservoirBars() {
    $('.res-bar').each(function() {
      var $bar = $(this);
      var stock = parseFloat($bar.attr('data-stock')) || 0;
      var capacity = parseFloat($bar.attr('data-cap')) || 1;
      
      // Calculate percentage clamped between 0% and 100%
      var percentage = Math.min(100, Math.max(0, (stock / capacity) * 100));
      percentage = Math.round(percentage * 10) / 10;
      
      // Find the label container in the current reservoir item
      var $label = $bar.closest('.res-item').find('.res-pct-label');
      
      // Apply dynamic threshold colors based on capacity levels
      if (percentage <= 20) {
        $bar.css('background', 'linear-gradient(135deg, #ef4444 0%, #f87171 100%)');
        $label.html('<span style="color: #ef4444; font-weight: 700;">' + percentage + '% (Low Fuel)</span>');
      } else if (percentage <= 45) {
        $bar.css('background', 'linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%)');
        $label.html('<span style="color: #d97706; font-weight: 600;">' + percentage + '% (Moderate)</span>');
      } else {
        $bar.css('background', 'linear-gradient(135deg, #fa8005 0%, #ff9d3b 100%)');
        $label.html('<span style="color: #10b981; font-weight: 600;">' + percentage + '% Full</span>');
      }
      
      // Animate width expansion smoothly
      setTimeout(function() {
        $bar.css({
          'width': percentage + '%',
          'transition': 'width 1.2s cubic-bezier(0.4, 0, 0.2, 1)'
        });
      }, 150);
    });
  }

  // Initialize reservoir calculations on load
  initReservoirBars();

  // 2. Automated Flash Message Banner Dismissals
  if ($('.msgon').length > 0) {
    var msg = $('.msgon').first().val();
    if (msg === 'done') {
      $('.success_ban').fadeIn(400).delay(4000).fadeOut(400);
    } else if (msg === 'error') {
      $('.error_ban').fadeIn(400).delay(4000).fadeOut(400);
    }
  }

  // 3. KPI Metric Cards Counter Effect
  $('.metric-card').on('mouseenter', function() {
    $(this).find('.metric-icon').css('transform', 'scale(1.1) rotate(5deg)');
  }).on('mouseleave', function() {
    $(this).find('.metric-icon').css('transform', 'scale(1) rotate(0deg)');
  });

  // 4. Smooth Close for Alert Boxes
  $('.action-alert .alert-btn').on('click', function(e) {
    // Allows default navigation link while applying a micro-click effect
    $(this).css('transform', 'scale(0.96)');
  });

});