$(document).ready(function () {
    // Function to handle smooth scrolling
    $('a[href^="#"]').on('click', function (e) {
        e.preventDefault();

        const target = $($(this).prop('hash'));
        const navbarHeight = $('.navbar').outerHeight();

        if (target.length) {
            $('html, body').stop().animate({
                scrollTop: target.offset().top - navbarHeight
            }, 500);
        }
    });
});
