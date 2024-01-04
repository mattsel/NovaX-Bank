$(document).ready(function () {
    // Function to handle smooth scrolling
    $('a[href^="#"]').on('click', function (e) {
        e.preventDefault();

        const target = $(this.getAttribute('href'));
        if (target.length) {
            $('html, body').stop().animate({
                scrollTop: target.offset().top - $('.navbar').height()
            }, 500);
        }
    });

    // Function to handle video playback based on scroll position
    function handleVideoPlayback() {
        var videoSection = $('#bankingProject .video-container');

        // Check if the video section is in the viewport
        if (isElementInViewport(videoSection[0])) {
            // Play the video if it's in the viewport
            videoSection.find('video')[0].play();
        } else {
            // Pause the video if it's not in the viewport
            videoSection.find('video')[0].pause();
        }
    }

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

    // Initial check for video playback on page load
    handleVideoPlayback();
});
