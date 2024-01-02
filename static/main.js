$(document).ready(function () {
    function isElementInViewport(el) {
        var rect = el.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            const targetElement = document.querySelector(this.getAttribute('href'));
            if (targetElement) {
                var offset = targetElement.offsetTop - $('.navbar').height();
                $('html, body').stop().animate({
                    scrollTop: offset
                }, 500);
            }
        });
    });

    function handleVideoPlayback() {
        var videoSection = $('#bankingProject .video-container');

        if (isElementInViewport(videoSection[0])) {
            videoSection.find('video')[0].play();
        } else {
            videoSection.find('video')[0].pause();
        }
    }

    $(window).scroll(function () {
        handleVideoPlayback();
    });

    handleVideoPlayback();
});