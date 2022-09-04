jQuery(document).ready(function($) {
    $(".clickable-row").click(function() {
        window.location = $(this).data("href");
    });
});

jQuery(document).ready(function($) {
    $(".clickable-column").click(function() {
        window.location = $(this).data("href");
    });
});
