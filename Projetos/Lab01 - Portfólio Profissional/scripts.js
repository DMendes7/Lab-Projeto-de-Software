// scripts.js

// Inicializar Vanta.js
VANTA.NET({
  el: "#vanta-bg",
  mouseControls: true,
  touchControls: true,
  gyroControls: false,
  minHeight: 200.00,
  minWidth: 200.00,
  scale: 1.00,
  scaleMobile: 1.00,
  color: 0xff0000,
  backgroundColor: 0x000000,
  points: 13.00,
  maxDistance: 23.00
});

// Animação de elementos ao aparecerem na tela
function animateElements() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate');
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.section, .project-card, .timeline-item').forEach(el => {
    observer.observe(el);
  });
}

// Scroll suave para links internos
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    e.preventDefault();
    const targetId = this.getAttribute('href');
    if (targetId === '#') return;
    const targetElement = document.querySelector(targetId);
    if (targetElement) {
      window.scrollTo({
        top: targetElement.offsetTop - 80,
        behavior: 'smooth'
      });
    }
  });
});

// Inicializar animações ao carregar
window.addEventListener('DOMContentLoaded', () => {
  animateElements();
});

particlesJS("particles-js", {
  particles: {
    number: {
      value: 120, // Aumente esse valor para mais densidade
      density: {
        enable: true,
        value_area: 1000 // Pode reduzir para deixar ainda mais próximas
      }
    },
    color: { value: "#ff0000" },
    shape: { type: "circle" },
    opacity: {
      value: 0.5,
      random: true
    },
    size: {
      value: 2.5, // Reduza se quiser partículas menores
      random: true
    },
    line_linked: {
      enable: true,
      distance: 130, // Reduza para deixar mais interligado
      color: "#ff0000",
      opacity: 0.3,
      width: 1
    },
    move: {
      enable: true,
      speed: 1.2,
      direction: "none",
      out_mode: "out"
    }
  },
  interactivity: {
    events: {
      onhover: { enable: true, mode: "grab" }
    },
    modes: {
      grab: {
        distance: 150,
        line_linked: { opacity: 0.5 }
      }
    }
  },
  retina_detect: true
});

window.addEventListener('load', () => {
  const particles = document.getElementById('particles-js');
  const totalHeight = document.body.scrollHeight;
  const headerHeight = document.getElementById('vanta-bg').offsetHeight;

  particles.style.top = `${headerHeight}px`;
  particles.style.height = `${totalHeight - headerHeight}px`;
});

const langToggles = document.querySelectorAll(".language-toggle");

langToggles.forEach((btn) => {
  btn.addEventListener("click", (e) => {
    e.preventDefault();
    const transition = document.getElementById("page-transition");
    transition.classList.add("active");

    const target = btn.getAttribute("data-target");
    setTimeout(() => {
      window.location.href = target;
    }, 600);
  });
});