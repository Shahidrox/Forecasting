$(document).ready(function() {
  $('[data-simplebar]').each(function() {
    new SimpleBar(this);
  });

  $(".menu-sub").each(function() {
    $(this).find("> a").each(function() {
      var $link = $(this);
      var $submenu = $link.next(); // Assuming the submenu is the next sibling
      var $menuSub = $link.closest(".menu-sub");
      var isActive = $menuSub.hasClass("active");
      var isAnimating = false;

      function toggleMenu() {
        isActive = !isActive;
        $menuSub.toggleClass("opened", isActive);

        if (isActive) {
          isAnimating = true;
          $submenu.css({
            height: "0px",
            opacity: "0",
            display: "block"
          });
          setTimeout(function() {
            $submenu.css({
              height: $submenu[0].scrollHeight + "px",
              opacity: "1"
            });
            setTimeout(function() {
              $submenu.css("height", "");
              isAnimating = false;
            }, 300);
          }, 0);
        } else {
          isAnimating = true;
          $submenu.css({
            height: $submenu[0].scrollHeight + "px",
            opacity: "0"
          });
          setTimeout(function() {
            $submenu.css("height", "0px");
            setTimeout(function() {
              $submenu.css("display", "none");
              isAnimating = false;
            }, 300);
          }, 0);
        }
      }

      $link.on("click", function(e) {
        e.preventDefault();
        if (!isAnimating) {
          toggleMenu();
        }
      });
    });
  });

  var page = $(document.documentElement).data('page');
  
  $(".menu > li > a").each(function() {
    var linkText = $(this).text().toLowerCase().replace(/\s/g, "-");
    if (page === linkText) {
      $(this).parent().addClass("active");
    }
  });

  $(".menu-sub > ul > li > a").each(function() {
    var submenuText = $(this).closest(".menu-sub").text().toLowerCase().replace(/\s/g, "-");
    var linkText = $(this).text().toLowerCase().replace(/\s/g, "-");
    if (page === `${submenuText}-${linkText}`) {
      $(this).addClass("active");
      $(this).closest(".menu-sub").addClass("opened active");
    }
  });
});