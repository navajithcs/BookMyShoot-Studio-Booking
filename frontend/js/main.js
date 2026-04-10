// Enhanced scroll reveal for elements with class 'reveal'
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
  animateSections();
  updateNavbarBackground();
});

window.addEventListener('load', () => {
  animateSections();
  document.body.classList.add('loaded');
});

// Navbar background on scroll ... existing code follows ...
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
  }
}

// Logout function
function logout() {
  localStorage.removeItem('user');
  window.location.href = getRootPrefix() + 'index.html';
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
    if (isNaN(target)) return;
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

document.addEventListener('DOMContentLoaded', () => {
  if (typeof lucide !== 'undefined') {
    lucide.createIcons();
  }
});

