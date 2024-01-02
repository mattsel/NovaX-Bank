// Wait for the document to be fully loaded before executing the JavaScript
$(document).ready(function () {

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

    // Event listener for smooth scrolling to anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            const targetElement = document.querySelector(this.getAttribute('href'));
            if (targetElement) {
                // Adjust scroll offset to account for fixed navbar
                var offset = targetElement.offsetTop - $('.navbar').height();
                // Animate scroll to the target element
                $('html, body').stop().animate({
                    scrollTop: offset
                }, 500);
            }
        });
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

    // Event listener for scroll events
    $(window).scroll(function () {
        // Call the function to handle video playback on scroll
        handleVideoPlayback();
    });

    // Initial check for video playback on page load
    handleVideoPlayback();
});
