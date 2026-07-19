// Theme Toggle Logic
document.addEventListener('DOMContentLoaded', () => {
    const themeToggleBtn = document.getElementById('theme-toggle');
    
    // Function to set theme
    const setTheme = (theme) => {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
    };

    // Get initial theme
    const getInitialTheme = () => {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            return savedTheme;
        }
        // Fallback to system preference
        const userPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        return userPrefersDark ? 'dark' : 'light';
    };

    // Apply initial theme immediately
    const initialTheme = getInitialTheme();
    setTheme(initialTheme);

    // Add click event listener to the toggle button
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            setTheme(newTheme);
        });
    }
});

// Immediately set the theme on document element before DOM is fully loaded to prevent flash
(function() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
    } else {
        const userPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        document.documentElement.setAttribute('data-theme', userPrefersDark ? 'dark' : 'light');
    }
})();
