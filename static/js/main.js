// Add smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Add fade-in animation for elements
document.addEventListener('DOMContentLoaded', function() {
    const fadeElements = document.querySelectorAll('.fade-in');
    fadeElements.forEach(element => {
        element.style.opacity = '1';
    });
});

document.addEventListener('DOMContentLoaded', () => {
    // Manejo del menú móvil
    const menuButton = document.getElementById('menuButton');
    const menuContent = document.getElementById('menuContent');
    const closeMenu = document.getElementById('closeMenu');

    if (menuButton && menuContent && closeMenu) {
        menuButton.addEventListener('click', () => {
            menuContent.classList.remove('translate-x-full');
            document.body.style.overflow = 'hidden';
        });

        closeMenu.addEventListener('click', () => {
            menuContent.classList.add('translate-x-full');
            document.body.style.overflow = '';
        });

        // Cerrar menú al hacer clic fuera
        document.addEventListener('click', (e) => {
            if (!menuContent.contains(e.target) && !menuButton.contains(e.target)) {
                menuContent.classList.add('translate-x-full');
                document.body.style.overflow = '';
            }
        });
    }

    // Flash message auto-hide
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 300);
        }, 3000);
    });
});

// Add ripple effect to buttons
document.addEventListener('click', function(e) {
    const target = e.target;
    if (target.matches('button') || target.matches('.btn-primary') || target.matches('.action-button')) {
        const rect = target.getBoundingClientRect();
        const ripple = document.createElement('div');
        const diameter = Math.max(rect.width, rect.height);
        const radius = diameter / 2;

        ripple.style.width = ripple.style.height = `${diameter}px`;
        ripple.style.left = `${e.clientX - rect.left - radius}px`;
        ripple.style.top = `${e.clientY - rect.top - radius}px`;
        ripple.className = 'ripple';

        const existingRipple = target.querySelector('.ripple');
        if (existingRipple) {
            existingRipple.remove();
        }

        target.appendChild(ripple);

        setTimeout(() => {
            ripple.remove();
        }, 600);
    }
});

// Function to delete an image
function deleteImage(filename) {
    fetch(`/delete/${filename}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            // Handle success
            console.log(data.message);
            // Optionally remove the image from the UI
        } else if (data.error) {
            // Handle error
            console.error(data.error);
        }
    })
    .catch(error => console.error('Error:', error));
}

// Example usage (you can replace this with your actual implementation)
document.querySelectorAll('.delete-button').forEach(button => {
    button.addEventListener('click', (event) => {
        const filename = event.target.dataset.filename;
        deleteImage(filename);
    });
});
