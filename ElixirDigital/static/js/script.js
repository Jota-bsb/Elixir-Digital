// script.js - Funcionalidades gerais do site

// Hamburger Menu Toggle
function initializeHamburgerMenu() {
  const hamburger = document.querySelector(".hamburger")
  const navMenu = document.querySelector(".nav-menu")
  if (hamburger && navMenu) {
    hamburger.addEventListener("click", () => {
      hamburger.classList.toggle("active")
      navMenu.classList.toggle("active")
    })
    document.querySelectorAll(".nav-menu a").forEach((link) => {
      link.addEventListener("click", () => {
        hamburger.classList.remove("active")
        navMenu.classList.remove("active")
      })
    })
  }
}

// Theme Toggle
function initializeThemeToggle() {
  const themeToggle = document.getElementById("theme-toggle")
  if (themeToggle) {
    if (
      localStorage.getItem("theme") === "light" ||
      (window.matchMedia("(prefers-color-scheme: light)").matches && !localStorage.getItem("theme"))
    ) {
      document.body.classList.add("light-mode")
      themeToggle.checked = true
    }
    themeToggle.addEventListener("change", () => {
      if (themeToggle.checked) {
        document.body.classList.add("light-mode")
        localStorage.setItem("theme", "light")
      } else {
        document.body.classList.remove("light-mode")
        localStorage.setItem("theme", "dark")
      }
    })
  }
}

// Feedback Carousel
function initializeFeedbackCarousel() {
  const track = document.querySelector(".feedback-track")
  const slides = document.querySelectorAll(".feedback-slide")
  const dots = document.querySelectorAll(".carousel-dot")
  if (track && slides.length > 0 && dots.length > 0) {
    let currentIndex = 0
    function goToSlide(index) {
      if (index < 0) index = slides.length - 1
      if (index >= slides.length) index = 0
      track.style.transform = `translateX(-${index * 100}%)`
      dots.forEach((dot) => dot.classList.remove("active"))
      dots[index].classList.add("active")
      currentIndex = index
    }
    dots.forEach((dot, index) => {
      dot.addEventListener("click", () => {
        goToSlide(index)
      })
    })
    setInterval(() => {
      goToSlide(currentIndex + 1)
    }, 5000)
  }
}

// Star Rating System
function initializeStarRating() {
  const stars = document.querySelectorAll(".star");
  const ratingInput = document.getElementById("rating");
  if (!stars.length || !ratingInput) return;
  let selectedRating = parseInt(ratingInput.value) || 0;
  function updateStars(rating) {
    stars.forEach((star) => {
      const val = parseInt(star.getAttribute("data-rating"));
      if (val <= rating) star.classList.add("active");
      else star.classList.remove("active");
    });
  }
  stars.forEach((star) => {
    const val = parseInt(star.getAttribute("data-rating"));
    star.addEventListener("click", () => {
      selectedRating = val;
      ratingInput.value = selectedRating;
      updateStars(selectedRating);
    });
    star.addEventListener("mouseover", () => {
      updateStars(val);
    });
    star.addEventListener("mouseout", () => {
      updateStars(selectedRating);
    });
  });
  updateStars(selectedRating);
}

// Feedback Form Handling (AJAX)
function initializeFeedbackForm() {
  const feedbackForm = document.getElementById("feedbackForm");
  const ratingInput = document.getElementById("rating");
  const stars = document.querySelectorAll(".star");

  if (!feedbackForm) return;

  feedbackForm.addEventListener("submit", async function (e) {
    e.preventDefault();

    if (!ratingInput.value) {
      alert("Por favor, selecione uma avaliação com as estrelas.");
      return;
    }

    const formData = new FormData(feedbackForm);

    try {
      const response = await fetch("/salvar_feedback", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const text = await response.text();
        alert("Erro ao enviar feedback: " + text);
        return;
      }

      // Feedback enviado com sucesso
      const successMessage = document.getElementById("successMessage");
      if (successMessage) {
        successMessage.style.display = "block";
        successMessage.scrollIntoView({ behavior: "smooth" });
      }

      // Reset do formulário
      feedbackForm.reset();
      if (stars.length > 0) {
        stars.forEach((star) => star.classList.remove("active"));
      }
      ratingInput.value = "";

    } catch (err) {
      alert("Erro ao enviar feedback: " + err.message);
    }
  });
}

// Inicializa todos os componentes
document.addEventListener("DOMContentLoaded", () => {
  initializeHamburgerMenu()
  initializeThemeToggle()
  initializeFeedbackCarousel()
  initializeStarRating()
  initializeFeedbackForm()
})