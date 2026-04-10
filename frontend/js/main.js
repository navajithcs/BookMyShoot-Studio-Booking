// Enhanced scroll reveal for elements with class 'reveal'
<<<<<<< HEAD
=======
function revealOnScroll() {
  const reveals = document.querySelectorAll('.reveal');
  const windowH = window.innerHeight;
  reveals.forEach((el, index) => {
    const rect = el.getBoundingClientRect();
    if (rect.top < windowH - 100) { 
      setTimeout(() => {
        el.classList.add('visible');
      }, index * 100);
    }
  });
}

// Add fade-in animation to sections on scroll
>>>>>>> fba2361 (Initial commit)
function animateSections() {
  const sections = document.querySelectorAll('section:not(.hero)');
  const windowH = window.innerHeight;
  
  sections.forEach(section => {
    const rect = section.getBoundingClientRect();
    if (rect.top < windowH - 150 && !section.classList.contains('animated')) {
      section.classList.add('animated');
      section.style.animation = 'fadeInUp 0.6s ease-out';
    }
  });
}

// Scroll event listeners
window.addEventListener('scroll', () => {
<<<<<<< HEAD
=======
  revealOnScroll();
>>>>>>> fba2361 (Initial commit)
  animateSections();
  updateNavbarBackground();
});

window.addEventListener('load', () => {
<<<<<<< HEAD
=======
  revealOnScroll();
>>>>>>> fba2361 (Initial commit)
  animateSections();
  document.body.classList.add('loaded');
});

<<<<<<< HEAD
// Navbar background on scroll ... existing code follows ...
=======
// Add loading animation
window.addEventListener('load', () => {
  document.body.classList.add('loaded');
});

// Navbar background on scroll
>>>>>>> fba2361 (Initial commit)
function updateNavbarBackground() {
  const navbar = document.getElementById('mainNavbar');
  if (navbar) {
    if (window.scrollY > 50) {
      navbar.style.background = 'rgba(255, 255, 255, 0.98)';
      navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
    } else {
      navbar.style.background = 'rgba(255, 255, 255, 0.95)';
      navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.05)';
    }
  }
}

// Email validation
function validateEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

// Phone number validation
function validatePhoneNumber(phone) {
  const phoneRegex = /^[\d\s\-\+\(\)]{10,15}$/;
  return phoneRegex.test(phone.replace(/\s/g, ''));
}

<<<<<<< HEAD
// Format path depending on subdirectories
function getRootPrefix() {
  const path = window.location.pathname;
  return (path.includes('/services/') || path.includes('/portfolio/')) ? '../' : '';
}

// Show profile information
function showProfile() {
  const user = JSON.parse(localStorage.getItem('user') || 'null');
  const pfx = getRootPrefix();

  if (user && user.user_type === 'photographer') {
    window.location.href = pfx + 'photographer-dashboard.html';
  } else if (user && user.user_type === 'admin') {
    window.location.href = pfx + 'admin-dashboard.html';
  } else {
    window.location.href = pfx + 'profile.html';
=======
// Show profile information
function showProfile() {
  const user = JSON.parse(localStorage.getItem('user') || 'null');
  if (user && user.user_type === 'photographer') {
    window.location.href = 'photographer-dashboard.html';
  } else if (user && user.user_type === 'admin') {
    window.location.href = 'admin-dashboard.html';
  } else {
    window.location.href = 'profile.html';
>>>>>>> fba2361 (Initial commit)
  }
}

// Logout function
function logout() {
  localStorage.removeItem('user');
<<<<<<< HEAD
  window.location.href = getRootPrefix() + 'index.html';
=======
  window.location.href = 'index.html';
>>>>>>> fba2361 (Initial commit)
}

// Toggle mobile menu
function toggleMobileMenu() {
  const nav = document.getElementById('mainNav');
  const toggle = document.getElementById('menuToggle');
  if (nav && toggle) {
    nav.classList.toggle('active');
    toggle.classList.toggle('active');
  }
}

// Smooth scroll to element
function smoothScrollTo(elementId) {
  const element = document.getElementById(elementId);
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}

// Counter animation for stats
function animateCounters() {
  const counters = document.querySelectorAll('.stat-number');
  counters.forEach(counter => {
    const target = parseInt(counter.textContent.replace(/\D/g, ''));
<<<<<<< HEAD
    if (isNaN(target)) return;
=======
>>>>>>> fba2361 (Initial commit)
    const duration = 2000;
    const increment = target / (duration / 16);
    let current = 0;
    
    const updateCounter = () => {
      current += increment;
      if (current < target) {
        counter.textContent = Math.floor(current) + '+';
        requestAnimationFrame(updateCounter);
      } else {
        counter.textContent = target + '+';
      }
    };
    
    updateCounter();
  });
}

// Intersection Observer for animations
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
<<<<<<< HEAD
  let delay = 0;
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      setTimeout(() => {
        entry.target.classList.add('visible');
        if (entry.target.classList.contains('stat-number') || entry.target.classList.contains('about-stats')) {
          animateCounters();
        }
      }, delay);
      delay += 150; // Stagger effect
      observer.unobserve(entry.target);
=======
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      if (entry.target.classList.contains('stat-number')) {
        animateCounters();
      }
>>>>>>> fba2361 (Initial commit)
    }
  });
}, observerOptions);

// Initialize observers when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.reveal').forEach(el => {
    observer.observe(el);
  });
});

// Add parallax effect to hero
window.addEventListener('scroll', () => {
  const hero = document.querySelector('.hero');
  if (hero) {
    const scrolled = window.pageYOffset;
    hero.style.backgroundPositionY = scrolled * 0.5 + 'px';
  }
});
<<<<<<< HEAD

document.addEventListener('DOMContentLoaded', () => {
  if (typeof lucide !== 'undefined') {
    lucide.createIcons();
  }
});

=======
>>>>>>> fba2361 (Initial commit)
