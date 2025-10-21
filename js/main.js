// Navbar scroll effect
const navbar = document.getElementById("navbar");
const scrollTop = document.getElementById("scrollTop");

window.addEventListener("scroll", () => {
    if (window.scrollY > 100) {
        navbar.classList.add("scrolled");
        scrollTop.classList.add("visible");
    } else {
        navbar.classList.remove("scrolled");
        scrollTop.classList.remove("visible");
    }
});

// Scroll to top functionality
scrollTop.addEventListener("click", () => {
    window.scrollTo({
        top: 0,
        behavior: "smooth",
    });
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute("href"));
        if (target) {
            target.scrollIntoView({
                behavior: "smooth",
                block: "start",
            });

            // Close mobile menu if it's open
            const mobileMenu = document.getElementById("mobileMenu");
            if (mobileMenu.classList.contains("active")) {
                mobileMenu.classList.remove("active");
            }
        }
    });
});

// Mobile menu functionality
const mobileMenuBtn = document.getElementById("mobileMenuBtn");
const mobileMenu = document.getElementById("mobileMenu");
const closeMenu = document.getElementById("closeMenu");

mobileMenuBtn.addEventListener("click", () => {
    mobileMenu.classList.add("active");
});

closeMenu.addEventListener("click", () => {
    mobileMenu.classList.remove("active");
});

// Close mobile menu when clicking on any mobile menu link
document.querySelectorAll(".mobile-menu-link").forEach((link) => {
    link.addEventListener("click", () => {
        mobileMenu.classList.remove("active");
    });
});

// Close mobile menu when clicking outside of it
document.addEventListener("click", (e) => {
    const isMobileMenuBtn = e.target.closest("#mobileMenuBtn");
    const isMobileMenu = e.target.closest("#mobileMenu");

    if (
        !isMobileMenuBtn &&
        !isMobileMenu &&
        mobileMenu.classList.contains("active")
    ) {
        mobileMenu.classList.remove("active");
    }
});

// Close mobile menu on escape key press
document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && mobileMenu.classList.contains("active")) {
        mobileMenu.classList.remove("active");
    }
});
