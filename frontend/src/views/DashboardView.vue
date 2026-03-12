<template>
  <div class="flex h-screen bg-slate-50">
    <!-- Sidebar -->
    <div class="w-64 bg-white border-r border-slate-200 p-6 space-y-8">
      <div class="flex items-center space-x-2">
        <div class="p-2 rounded-lg bg-primary-600">
          <span class="font-bold text-white uppercase">ROTA</span>
        </div>
      </div>
      <nav class="space-y-2">
        <a href="#" class="flex items-center space-x-3 px-4 py-3 bg-primary-50 text-primary-600 rounded-xl font-medium">
          <SearchIcon class="w-5 h-5" />
          <span>Müşteri Bul</span>
        </a>
        <a href="#" class="flex items-center space-x-3 px-4 py-3 text-slate-600 hover:bg-slate-50 rounded-xl transition-colors">
          <FileTextIcon class="w-5 h-5" />
          <span>Tekliflerim</span>
        </a>
      </nav>
      <div class="pt-8 mt-8 border-t border-slate-100">
        <button @click="logout" class="flex items-center space-x-3 px-4 py-3 text-slate-500 hover:text-red-600 transition-colors w-full">
          <LogOutIcon class="w-5 h-5" />
          <span>Çıkış Yap</span>
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- Search Bar Layer -->
      <div class="p-10 bg-white border-b border-slate-200">
        <h1 class="text-2xl font-bold text-slate-900 mb-6">Yeni Müşteriler Bul</h1>
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div class="md:col-span-1">
            <label class="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">İş / Niş</label>
            <input v-model="searchParams.niche" placeholder="Örn: Diş Hekimi" class="w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition-all" />
          </div>
          <div class="md:col-span-1">
            <label class="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Konum</label>
            <input v-model="searchParams.location" placeholder="Örn: İstanbul" class="w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition-all" />
          </div>
          <div class="md:col-span-1">
            <label class="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Detaylar</label>
            <input v-model="searchParams.details" placeholder="Örn: Web sitesi yok" class="w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition-all" />
          </div>
          <div class="flex items-end">
            <button @click="searchLeads" :disabled="searching" class="w-full bg-primary-600 hover:bg-primary-700 text-white font-bold py-3 px-6 rounded-xl transition-all shadow-lg shadow-primary-100 flex items-center justify-center space-x-2">
              <span v-if="searching">Aranıyor...</span>
              <span v-else>Listele</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Results Layer -->
      <div class="flex-1 overflow-y-auto p-10">
        <div v-if="leads.length === 0" class="h-full flex flex-col items-center justify-center text-slate-400">
          <div class="p-6 bg-white rounded-full mb-4">
             <SearchIcon class="w-12 h-12" />
          </div>
          <p>Henüz arama yapmadınız veya sonuç bulunamadı.</p>
        </div>

        <div v-else class="grid grid-cols-1 gap-6">
          <div v-for="lead in leads" :key="lead.id" class="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm hover:shadow-md transition-all flex flex-col md:flex-row justify-between items-start md:items-center">
            <div class="space-y-1">
              <h3 class="text-xl font-bold text-slate-900">{{ lead.name }}</h3>
              <p class="text-slate-500 flex items-center space-x-2">
                <GlobeIcon class="w-4 h-4" />
                <a :href="lead.website" target="_blank" class="hover:text-primary-600">{{ lead.website }}</a>
              </p>
              <div class="flex space-x-2 mt-2">
                <span class="px-2 py-1 bg-slate-100 text-slate-600 text-xs rounded-md">{{ lead.niche }}</span>
                <span class="px-2 py-1 bg-slate-100 text-slate-600 text-xs rounded-md">{{ lead.location }}</span>
              </div>
            </div>
            
            <div class="mt-4 md:mt-0 flex space-x-3">
               <button v-if="lead.status === 'found'" @click="analyzeLead(lead.id)" class="px-4 py-2 border border-primary-600 text-primary-600 hover:bg-primary-50 rounded-xl font-medium transition-colors">
                AI Analizi Yap
              </button>
              <button v-if="lead.status === 'analyzed'" @click="generateProposal(lead.id)" class="px-4 py-2 bg-primary-600 text-white hover:bg-primary-700 rounded-xl font-medium transition-colors">
                Teklif Oluştur
              </button>
              <button v-if="lead.status === 'proposal_generated'" @click="showProposal(lead)" class="px-4 py-2 bg-green-600 text-white hover:bg-green-700 rounded-xl font-medium transition-colors">
                Teklifi Gör
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal for Proposal/Analysis -->
    <div v-if="selectedLead" class="fixed inset-0 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-2xl max-w-2xl w-full max-h-[80vh] overflow-hidden flex flex-col shadow-2xl">
        <div class="p-6 border-b border-slate-100 flex justify-between items-center">
          <h2 class="text-xl font-bold">{{ selectedLead.name }} - Teklif</h2>
          <button @click="selectedLead = null" class="text-slate-400 hover:text-slate-600">
            <XIcon class="w-6 h-6" />
          </button>
        </div>
        <div class="p-10 overflow-y-auto space-y-6">
          <div>
            <h3 class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">AI ANALİZİ</h3>
            <p class="text-slate-700 whitespace-pre-wrap bg-slate-50 p-4 rounded-xl border border-slate-100 italic">{{ selectedLead.analysis }}</p>
          </div>
          <div>
            <h3 class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">OLUŞTURULAN TEKLİF</h3>
            <textarea v-model="selectedLead.proposal_text" rows="10" class="w-full p-6 bg-white border-2 border-primary-100 rounded-2xl text-slate-800 outline-none focus:border-primary-500 transition-all font-serif"></textarea>
          </div>
        </div>
        <div class="p-6 border-t border-slate-100 bg-slate-50 flex justify-end space-x-3">
          <button @click="selectedLead = null" class="px-6 py-2 text-slate-600 font-medium">Kapat</button>
          <button @click="sendProposal" class="px-8 py-2 bg-primary-600 text-white rounded-xl font-bold shadow-lg shadow-primary-200 hover:bg-primary-700 transition-all">Gönder (Simüle)</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Search as SearchIcon, FileText as FileTextIcon, LogOut as LogOutIcon, Globe as GlobeIcon, X as XIcon } from 'lucide-vue-next'
import api from '../api'

const router = useRouter()
const leads = ref([])
const searching = ref(false)
const selectedLead = ref(null)

const searchParams = reactive({
  niche: '',
  location: '',
  details: ''
})

const fetchLeads = async () => {
  try {
    const res = await api.get('/leads/')
    leads.value = res.data
  } catch (err) {
    console.error(err)
  }
}

const searchLeads = async () => {
  if (!searchParams.niche || !searchParams.location) return
  searching.value = true
  try {
    const res = await api.post('/leads/search', searchParams)
    leads.value = [...res.data, ...leads.value]
  } catch (err) {
    alert('Arama başarısız oldu')
  } finally {
    searching.value = false
  }
}

const analyzeLead = async (id) => {
  try {
    const res = await api.post(`/leads/${id}/analyze`)
    const index = leads.value.findIndex(l => l.id === id)
    leads.value[index] = res.data
  } catch (err) {
    alert('Analiz yapılamadı')
  }
}

const generateProposal = async (id) => {
  try {
    const res = await api.post(`/leads/${id}/generate-proposal`)
    const index = leads.value.findIndex(l => l.id === id)
    leads.value[index] = res.data
  } catch (err) {
    alert('Teklif oluşturulamadı')
  }
}

const showProposal = (lead) => {
  selectedLead.value = { ...lead }
}

const sendProposal = () => {
  alert('Teklif başarıyla gönderildi (Simüle edildi)')
  selectedLead.value = null
}

const logout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}

onMounted(fetchLeads)
</script>
