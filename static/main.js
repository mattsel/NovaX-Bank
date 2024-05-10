document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('.navbar a');

    navLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            const href = this.getAttribute('href');
            
            // Check if the link is meant for smooth scrolling within the page
            if (href.startsWith('#')) {
                event.preventDefault(); // Prevent default anchor behavior

                const targetId = href.substring(1); // Get target section ID
                const targetSection = document.getElementById(targetId);

                if (targetSection) {
                    // Scroll to the target section with an offset
                    targetSection.scrollIntoView({ behavior: 'smooth', block: 'start', inline: 'nearest' });
                }
            }
        });
    });
});
