<template>
  <div class="flex min-h-screen items-center justify-center bg-slate-50 px-4">
    <div class="w-full max-w-md space-y-8 rounded-2xl bg-white p-10 shadow-xl border border-slate-100">
      <div class="text-center">
        <div class="mx-auto flex h-12 w-12 items-center justify-center rounded-xl bg-primary-600 text-white font-bold text-xl">R</div>
        <h2 class="mt-6 text-3xl font-extrabold text-slate-900">{{ isRegister ? 'Hesap Oluştur' : 'Hoş Geldiniz' }}</h2>
        <p class="mt-2 text-sm text-slate-500">
          {{ isRegister ? 'Hemen başlayın ve müşteri bulmaya odaklanın' : 'Giriş yaparak müşterilerini bulmaya devam et' }}
        </p>
      </div>
      <form class="mt-8 space-y-6" @submit.prevent="handleSubmit">
        <div class="space-y-4 rounded-md shadow-sm">
          <div v-if="isRegister">
            <label for="name" class="block text-sm font-medium text-slate-700">Ad Soyad</label>
            <input v-model="form.full_name" id="name" type="text" required class="block w-full rounded-lg border border-slate-300 px-3 py-2 mt-1 focus:border-primary-500 focus:ring-primary-500 sm:text-sm" />
          </div>
          <div>
            <label for="email" class="block text-sm font-medium text-slate-700">E-posta Adresi</label>
            <input v-model="form.email" id="email" type="email" required class="block w-full rounded-lg border border-slate-300 px-3 py-2 mt-1 focus:border-primary-500 focus:ring-primary-500 sm:text-sm" />
          </div>
          <div>
            <label for="password" class="block text-sm font-medium text-slate-700">Şifre</label>
            <input v-model="form.password" id="password" type="password" required class="block w-full rounded-lg border border-slate-300 px-3 py-2 mt-1 focus:border-primary-500 focus:ring-primary-500 sm:text-sm" />
          </div>
        </div>

        <div>
          <button type="submit" :disabled="loading" class="group relative flex w-full justify-center rounded-xl bg-primary-600 px-4 py-3 text-sm font-semibold text-white transition-all hover:bg-primary-700 focus:outline-none disabled:opacity-50">
            {{ isRegister ? 'Kayıt Ol' : 'Giriş Yap' }}
          </button>
        </div>
        
        <div class="text-center mt-4">
          <button type="button" @click="isRegister = !isRegister" class="text-sm font-medium text-primary-600 hover:text-primary-500">
            {{ isRegister ? 'Zaten hesabınız var mı? Giriş yapın' : 'Hesabınız yok mu? Kayıt olun' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const router = useRouter()
const isRegister = ref(false)
const loading = ref(false)

const form = reactive({
  email: '',
  password: '',
  full_name: ''
})

const handleSubmit = async () => {
  loading.value = true
  try {
    if (isRegister.value) {
      await api.post('/auth/register', form)
      isRegister.value = false
    } else {
      const loginForm = new FormData()
      loginForm.append('username', form.email)
      loginForm.append('password', form.password)
      const res = await api.post('/auth/login', loginForm)
      localStorage.setItem('token', res.data.access_token)
      router.push('/dashboard')
    }
  } catch (err) {
    alert(err.response?.data?.detail || 'Bir hata oluştu')
  } finally {
    loading.value = false
  }
}
</script>
