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

// Particles.js (efeito de fundo)
particlesJS("particles-js", {
  particles: {
    number: {
      value: 120,
      density: { enable: true, value_area: 1000 }
    },
    color: { value: "#ff0000" },
    shape: { type: "circle" },
    opacity: { value: 0.5, random: true },
    size: { value: 2.5, random: true },
    line_linked: {
      enable: true,
      distance: 130,
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
    events: { onhover: { enable: true, mode: "grab" } },
    modes: { grab: { distance: 150, line_linked: { opacity: 0.5 } } }
  },
  retina_detect: true
});

window.addEventListener('load', () => {
  const particles = document.getElementById('particles-js');
  const vanta = document.getElementById('vanta-bg');
  if (!particles || !vanta) return;

  const totalHeight = document.body.scrollHeight;
  const headerHeight = vanta.offsetHeight;

  particles.style.top = `${headerHeight}px`;
  particles.style.height = `${totalHeight - headerHeight}px`;
});

// Transição de idioma com overlay
const langToggles = document.querySelectorAll(".language-toggle");
langToggles.forEach((btn) => {
  btn.addEventListener("click", (e) => {
    e.preventDefault();
    const transition = document.getElementById("page-transition");
    if (transition) transition.classList.add("active");

    const target = btn.getAttribute("data-target");
    setTimeout(() => {
      window.location.href = target;
    }, 600);
  });
});

// ===== Modal de Projeto + botão de repositório (i18n + robust) =====
(function setupProjectModal() {
  const modal = document.getElementById('project-modal');
  if (!modal) return;

  const overlay = modal.querySelector('.project-modal__overlay');
  const closeEls = modal.querySelectorAll('[data-close-modal]');
  const mediaEl = document.getElementById('pm-media');
  const titleEl = document.getElementById('pm-title');
  const descEl = document.getElementById('pm-desc');
  const linkEl = document.getElementById('pm-link');

  const cards = document.querySelectorAll('.project-card');

  // Torna os cards focáveis para acessibilidade via teclado
  cards.forEach(c => c.setAttribute('tabindex', '0'));

  // Tradução automática do rótulo do botão pelo <html lang="...">
  const lang = (document.documentElement.getAttribute('lang') || 'pt-BR').toLowerCase();
  const LABELS = {
    available: lang.startsWith('en') ? 'View repository' : 'Ver repositório',
    unavailable: lang.startsWith('en') ? 'Repository unavailable' : 'Repositório indisponível'
  };

  // Garanta que o botão do modal é sempre clicável quando habilitado
  if (linkEl) {
    linkEl.style.pointerEvents = 'auto';
    linkEl.style.position = 'relative';
    linkEl.style.zIndex = '5';
    // Fallback explícito: abre em nova aba de qualquer forma
    linkEl.addEventListener('click', (e) => {
      // Se não houver href, não faz nada
      if (!linkEl.getAttribute('href')) {
        e.preventDefault();
        return;
      }
      e.stopPropagation(); // não fechar modal por engano
      // Alguns navegadores bloqueiam navegações se algo interceptar o clique
      // então garantimos a abertura programática
      const url = linkEl.getAttribute('href');
      if (url) {
        // deixa o default acontecer, mas também força a abertura
        // (o default será bloqueado se popup-blocker pegar; window.open ajuda)
        setTimeout(() => {
          try { window.open(url, '_blank', 'noopener'); } catch (_) {}
        }, 0);
      }
    });
  }

  function setRepoLink(linkValue) {
    if (!linkEl) return;
    const link = (linkValue || '').trim();

    if (link && link !== 'unavailable') {
      linkEl.textContent = LABELS.available;
      linkEl.setAttribute('href', link);
      linkEl.setAttribute('target', '_blank');
      linkEl.setAttribute('rel', 'noopener');
      linkEl.hidden = false;
      linkEl.classList.remove('disabled');
      linkEl.style.pointerEvents = 'auto';
    } else {
      linkEl.textContent = LABELS.unavailable;
      linkEl.removeAttribute('href');
      linkEl.hidden = false;               // visível, mas inativo
      linkEl.classList.add('disabled');
      linkEl.style.pointerEvents = 'none';
    }
  }

  function openModal({ title, media, description, link }) {
    titleEl.textContent = title || '';
    descEl.textContent = description || '';

    // <img> cobre PNG/JPG e GIF animado
    mediaEl.src = media || '';
    mediaEl.alt = title || 'Projeto';

    // Define estado/texto do botão conforme presença do link
    setRepoLink(link);

    modal.classList.add('is-open');
    modal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden'; // trava scroll no fundo
  }

  function closeModal() {
    modal.classList.remove('is-open');
    modal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    // limpar a mídia reinicia o GIF na próxima abertura
    mediaEl.src = '';
  }

  cards.forEach(card => {
    // Se houver <a> dentro do card (ex.: título com link), não navega — abre o modal
    card.querySelectorAll('a').forEach((a) => {
      a.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        const data = card.dataset;
        openModal({
          title: data.title,
          media: data.media,
          description: data.description,
          link: data.link
        });
      });
    });

    function handleOpen() {
      const data = card.dataset;
      openModal({
        title: data.title,
        media: data.media,
        description: data.description,
        link: data.link
      });
    }

    card.addEventListener('click', handleOpen);
    card.addEventListener('keypress', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        handleOpen();
      }
    });
  });

  closeEls.forEach(btn => btn.addEventListener('click', closeModal));
  if (overlay) overlay.addEventListener('click', closeModal);

  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('is-open')) {
      closeModal();
    }
  });
})();
