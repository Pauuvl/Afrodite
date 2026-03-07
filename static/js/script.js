console.log("Afrodite funcionando correctamente");
var swiper = new Swiper(".product-swiper", {
  slidesPerView: 4,
  spaceBetween: 30,

  navigation: {
    nextEl: ".icon-arrow-right",
    prevEl: ".icon-arrow-left",
  },

  pagination: {
    el: ".swiper-pagination",
    clickable: true,
  },

  breakpoints: {
    0: {
      slidesPerView: 1
    },
    768: {
      slidesPerView: 2
    },
    992: {
      slidesPerView: 3
    },
    1200: {
      slidesPerView: 4
    }
  }
});