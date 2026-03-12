<template>
  <div class="relative overflow-hidden bg-white">
    <!-- Navbar -->
    <nav class="relative flex items-center justify-between px-6 py-8 mx-auto max-w-7xl">
      <div class="flex items-center flex-1">
        <div class="flex items-center justify-between w-full md:w-auto">
          <a href="#" class="flex items-center space-x-2">
            <div class="p-2 rounded-lg bg-primary-600">
              <span class="font-bold text-white uppercase">ROTA</span>
            </div>
          </a>
        </div>
      </div>
      <div class="flex items-center space-x-4">
        <router-link to="/login" class="px-5 py-2 text-base font-medium transition-colors text-slate-600 hover:text-primary-600">
          Giriş Yap
        </router-link>
        <router-link to="/login" class="px-5 py-2 text-base font-medium text-white transition-all rounded-full bg-primary-600 hover:bg-primary-700 hover:shadow-lg">
          Ücretsiz Dene
        </router-link>
      </div>
    </nav>

    <!-- Hero Section -->
    <div class="relative pt-16 pb-32 overflow-hidden lg:pt-32">
      <div class="px-6 mx-auto max-w-7xl">
        <div class="text-center lg:text-left">
          <h1 class="text-5xl font-extrabold tracking-tight text-slate-900 md:text-6xl">
            <span class="block">Yapay Zeka ile</span>
            <span class="block text-primary-600">Satışlarınızı Otomatize Edin</span>
          </h1>
          <p class="max-w-xl mt-6 text-xl text-slate-500">
            Rota, potansiyel müşterilerinizi bulur, ihtiyaçlarını analiz eder ve onlara özel teklifler oluşturarak satış sürecinizi baştan sona hızlandırır.
          </p>
          <div class="mt-10 flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4 justify-center lg:justify-start">
            <router-link to="/login" class="px-8 py-4 text-lg font-bold text-white rounded-xl bg-primary-600 transition-all hover:scale-105 hover:bg-primary-700 shadow-xl shadow-primary-200">
              Hemen Başla
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>
