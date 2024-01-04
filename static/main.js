// Wait for the document to be fully loaded before executing the JavaScript
$(document).ready(function () {
    // Function to handle smooth scrolling
    $('a[href^="#"]').on('click', function (e) {
        e.preventDefault();

        const targetElement = $(this.getAttribute('href'));
        if (targetElement.length) {
            // Adjust scroll offset to account for fixed navbar
            var offset = targetElement.offset().top - $('.navbar').height();
            // Animate scroll to the target element
            $('html, body').stop().animate({
                scrollTop: offset
            }, 500);
        }
    });

    // Function to check if an element is in the viewport
    function isElementInViewport(el) {
        var rect = el.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }

    // Event listener for scroll events
    $(window).scroll(function () {
        // Call the function to handle video playback on scroll
        handleVideoPlayback();
    });

    // Function to handle video playback based on scroll position
    function handleVideoPlayback() {
        // Your existing code for video playback logic goes here
    }
});
