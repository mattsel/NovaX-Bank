document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('.navbar a');

    navLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent default anchor behavior

            const targetId = this.getAttribute('href').substring(1); // Get target section ID
            const targetSection = document.getElementById(targetId);

            if (targetSection) {
                // Scroll to the target section with an offset
                targetSection.scrollIntoView({ behavior: 'smooth', block: 'start', inline: 'nearest', scrollMarginTop: 100 });
            }
        });
    });
});
