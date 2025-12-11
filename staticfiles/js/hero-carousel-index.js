document.addEventListener('DOMContentLoaded', function () {
    const slides = document.querySelectorAll('.hero-slide');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const indicators = document.querySelectorAll('.carousel-indicators button');
    const heroButtons = document.querySelector('.hero-btn-group');

    let currentIndex = 0;
    const totalSlides = slides.length;
    let autoSlideInterval;

    // Función para mostrar slide
    function showSlide(index) {
        // Quitar clase active de todos
        slides.forEach(slide => slide.classList.remove('active'));
        indicators.forEach(ind => ind.classList.remove('active'));

        // Añadir clase active al actual
        slides[index].classList.add('active');
        indicators[index].classList.add('active');

        // Mostrar/ocultar botones solo en el primer slide
        if (index === 0) {
            heroButtons.style.opacity = '1';
            heroButtons.style.visibility = 'visible';
        } else {
            heroButtons.style.opacity = '0';
            heroButtons.style.visibility = 'hidden';
        }
    }

    // Siguiente slide
    function nextSlide() {
        currentIndex = (currentIndex + 1) % totalSlides;
        showSlide(currentIndex);
    }

    // Slide anterior
    function prevSlide() {
        currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
        showSlide(currentIndex);
    }

    // Eventos de indicadores
    indicators.forEach((indicator, idx) => {
        indicator.addEventListener('click', () => {
            currentIndex = idx;
            showSlide(currentIndex);
            resetAutoSlide();
        });
    });

    // Eventos de botones
    nextBtn.addEventListener('click', () => {
        nextSlide();
        resetAutoSlide();
    });

    prevBtn.addEventListener('click', () => {
        prevSlide();
        resetAutoSlide();
    });

    // Auto-slide cada 6 segundos
    function startAutoSlide() {
        autoSlideInterval = setInterval(nextSlide, 6000);
    }

    function resetAutoSlide() {
        clearInterval(autoSlideInterval);
        startAutoSlide();
    }

    // Iniciar
    showSlide(currentIndex);
    startAutoSlide();
});