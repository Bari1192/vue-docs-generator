<template>
  <div class="container mx-auto my-12 relative overflow-hidden">
    <div class="carousel-container h-full min-w-full min-h-[70dvh]" @mouseenter="stopAutoplay"
      @mouseleave="startAutoplay">
      <div v-for="(movie, index) in movies" :key="index" :class="['carousel-item absolute w-full h-full transition-transform duration-1000 ease-in-out',
        { 'active-slide': index === activeIndex }
      ]" :style="getSlideTransform(index)">
        <img :src="movie.imageUrl" :alt="movie.title"
          class="w-full h-full object-cover rounded-lg shadow-xl overflow-hidden">
        <div
          class="absolute  right-0 top-0 bg-gradient-to-b from-black to-transparent p-12 pb-24 text-white rounded-r-lg overflow-hidden">
          <h3 class="text-4xl font-bold mb-2">{{ movie.title }}</h3>
          <p class="text-xl">Nézd meg most a moziban!</p>
        </div>
      </div>
    </div>

    <!-- Navigációs gombok -->
    <button @click="prevSlide"
      class="carousel-control-btn absolute left-4 top-1/2 -translate-y-1/2 bg-gray-800 bg-opacity-50 text-white p-3 rounded-full hover:bg-opacity-75 transition-all duration-300 z-10">
      <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
      </svg>
    </button>
    <button @click="nextSlide"
      class="carousel-control-btn absolute right-4 top-1/2 -translate-y-1/2 bg-gray-800 bg-opacity-50 text-white p-3 rounded-full hover:bg-opacity-75 transition-all duration-300 z-10">
      <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
      </svg>
    </button>

    <!-- Indikátorok -->
    <div class="carousel-indicators absolute bottom-4 left-1/2 -translate-x-1/2 flex space-x-2 z-10">
      <button v-for="(movie, index) in movies" :key="'indicator-' + index" @click="goToSlide(index)"
        :class="['w-4 h-4 rounded-full bg-gray-400 hover:bg-pink-500 transition-colors duration-300', { 'bg-pink-600': index === activeIndex }]"></button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const movies = ref([
]);

const activeIndex = ref(0);
let autoplayInterval = null;
const autoplayDelay = 3000;


const nextSlide = () => {
  activeIndex.value = (activeIndex.value + 1) % movies.value.length;
};

const prevSlide = () => {
  activeIndex.value = (activeIndex.value - 1 + movies.value.length) % movies.value.length;
};

const goToSlide = (index) => {
  activeIndex.value = index;
};

const startAutoplay = () => {
  stopAutoplay(); // Biztos, hogy nincs futó intervallum
  autoplayInterval = setInterval(nextSlide, autoplayDelay);
};

const stopAutoplay = () => {
  if (autoplayInterval) {
    clearInterval(autoplayInterval);
    autoplayInterval = null;
  }
};

const getSlideTransform = (index) => {
  const offset = (index - activeIndex.value) * 100; // 100% az adott elem szélessége
  return `transform: translateX(${offset}%); opacity: ${index === activeIndex.value ? 1 : 0.5}; z-index: ${index === activeIndex.value ? 5 : 1};`;
};


onMounted(() => {
  startAutoplay();
});

onUnmounted(() => {
  stopAutoplay();
});
</script>

<style scoped>
/* A perspektíva és 3D stílusok már nem kellenek a sima csúsztatáshoz, de a biztonság kedvéért itt hagyhatók, vagy törölhetők. */
.perspective-1000 {
  /* perspective: 1000px; */
}

.transform-style-preserve-3d {
  /* transform-style: preserve-3d; */
}

.backface-hidden {
  /* backface-visibility: hidden; */
}

.carousel-container {
  overflow: hidden;
  position: relative;
}

.carousel-item {
  /* transform-origin: center center; */
  /* A 3D-s forgáshoz tartozó transzformációk már nem kellenek */
  left: 0;
  /* Alapértelmezett pozíció */
  top: 0;
}

/* Az aktív slide mindig az első legyen, a többi eltolva */
.carousel-item.active-slide {
  transform: translateX(0%) !important;
  opacity: 1 !important;
  z-index: 5 !important;
}
</style>