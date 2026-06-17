<template>
  <div class="my-favorites">
    <div class="header">
      <button class="back-btn" @click="goBack">返回</button>
      <h2>我的收藏</h2>
      <button class="debug-btn" @click="showDebugModal = true">🔍 调试信息</button>
    </div>

    <div v-if="loading" class="loading">加载中...</div>

    <div v-else-if="error" class="empty error">
      <p>加载失败：{{ error }}</p>
      <button @click="fetchFavorites">重试</button>
    </div>

    <div v-else-if="favorites.length === 0" class="empty">
      暂无收藏记录
    </div>

    <div v-else class="favorite-grid">
      <div
        v-for="favorite in favorites"
        :key="favorite.id"
        class="favorite-card"
        @click="goToActivity(favorite.activity)"
      >
        <div class="card-content">
          <h3>{{ favorite.activity?.title || '未知活动' }}</h3>
          <div class="card-info">
            <span class="type-badge" :class="'type-' + favorite.activity?.type">
              {{ getTypeName(favorite.activity?.type) }}
            </span>
            <span>{{ formatTime(favorite.activity?.start_time) }}</span>
            <span>{{ favorite.activity?.location || '未知' }}</span>
          </div>
        </div>
        <button class="btn-cancel" @click.stop="handleCancel(favorite.id)">取消收藏</button>
      </div>
    </div>

    <div v-if="showDebugModal" class="debug-modal" @click.self="showDebugModal = false">
      <div class="debug-modal-content">
        <div class="debug-modal-header">
          <h3>🔍 API调试信息 - 我的收藏</h3>
          <button class="close-btn" @click="showDebugModal = false">×</button>
        </div>
        <div class="debug-modal-body">
          <div class="debug-section">
            <h4>📋 请求信息</h4>
            <p><strong>URL:</strong> {{ debugInfo.url }}</p>
            <p><strong>状态码:</strong> <span :class="debugInfo.status >= 200 && debugInfo.status < 300 ? 'success' : 'error'">{{ debugInfo.status }}</span></p>
            <p><strong>Token:</strong> {{ debugInfo.token ? debugInfo.token.slice(0, 20) + '...' : '无' }}</p>
          </div>
          <div class="debug-section">
            <h4>📦 响应数据</h4>
            <pre>{{ JSON.stringify(debugInfo.response, null, 2) }}</pre>
          </div>
          <div class="debug-section" v-if="debugInfo.error">
            <h4>❌ 错误信息</h4>
            <pre class="error">{{ debugInfo.error }}</pre>
          </div>
          <div class="debug-section">
            <h4>🔑 本地存储</h4>
            <p><strong>token存在:</strong> {{ localStorage.getItem('token') ? '是' : '否' }}</p>
            <p><strong>userInfo:</strong> {{ localStorage.getItem('userInfo') ? '已保存' : '无' }}</p>
          </div>
        </div>
        <div class="debug-modal-footer">
          <button @click="copyDebugInfo">复制信息</button>
          <button @click="showDebugModal = false">关闭</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getMyFavorites, cancelFavorite } from '@/api/activity'

const router = useRouter()
const favorites = ref([])
const loading = ref(false)
const error = ref('')
const showDebugModal = ref(false)
const debugInfo = ref({
  url: '',
  status: 0,
  token: '',
  response: null,
  error: null
})

const getTypeName = (type) => {
  const types = { 0: '讲座', 1: '比赛', 2: '晚会' }
  return types[type] || '未知'
}

const formatTime = (time) => {
  if (!time) return ''
  return new Date(time).toLocaleString('zh-CN')
}

const fetchFavorites = async () => {
  loading.value = true
  error.value = ''
  debugInfo.value = { url: '', status: 0, token: '', response: null, error: null }
  
  const token = localStorage.getItem('token')
  debugInfo.value.token = token
  
  try {
    debugInfo.value.url = '/api/favorites/'
    
    const response = await getMyFavorites()
    debugInfo.value.response = response
    debugInfo.value.status = 200
    
    favorites.value = response.favorites || []
  } catch (err) {
    error.value = err.message || '获取收藏记录失败'
    debugInfo.value.error = err.message || '未知错误'
    debugInfo.value.status = err.response?.status || 0
    debugInfo.value.response = err.response?.data || null
    ElMessage.error(error.value)
  } finally {
    loading.value = false
  }
}

const copyDebugInfo = () => {
  const info = JSON.stringify(debugInfo.value, null, 2)
  navigator.clipboard.writeText(info).then(() => {
    ElMessage.success('已复制调试信息')
  }).catch(() => {
    ElMessage.warning('复制失败，请手动复制')
  })
}

const handleCancel = async (id) => {
  try {
    await ElMessageBox.confirm('确定要取消收藏吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await cancelFavorite(id)
    ElMessage.success('取消收藏成功')
    await fetchFavorites()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('取消收藏失败')
    }
  }
}

const goBack = () => {
  router.push('/home')
}

const goToActivity = (activity) => {
  if (activity && activity.id) {
    router.push(`/activities/${activity.id}`)
  }
}

onMounted(() => {
  fetchFavorites()
})
</script>

<style scoped>
.my-favorites {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
}

.back-btn {
  padding: 8px 16px;
  background: #f5f5f5;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.header h2 {
  margin: 0;
  font-size: 24px;
}

.loading, .empty {
  text-align: center;
  padding: 60px 0;
  color: #999;
  font-size: 16px;
}

.favorite-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.favorite-card {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.favorite-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.card-content {
  padding: 15px;
}

.card-content h3 {
  margin: 0 0 10px 0;
  font-size: 18px;
  color: #333;
}

.card-info {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  font-size: 14px;
  color: #666;
}

.type-badge {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.type-0 { background: #e3f2fd; color: #1976d2; }
.type-1 { background: #fff3e0; color: #f57c00; }
.type-2 { background: #fce4ec; color: #c2185b; }

.btn-cancel {
  width: 100%;
  padding: 10px;
  background: #f5f5f5;
  color: #666;
  border: none;
  cursor: pointer;
}

.btn-cancel:hover {
  background: #ffe4e4;
  color: #f56c6c;
}

.debug-btn {
  padding: 8px 16px;
  background: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  margin-left: auto;
}

.debug-btn:hover {
  background: #66b1ff;
}

.empty.error {
  color: #f56c6c;
}

.empty.error button {
  margin-top: 10px;
  padding: 8px 16px;
  background: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.debug-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.debug-modal-content {
  background: #fff;
  border-radius: 8px;
  width: 90%;
  max-width: 800px;
  max-height: 80vh;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.debug-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background: #f5f7fa;
  border-bottom: 1px solid #ebeef5;
}

.debug-modal-header h3 {
  margin: 0;
  font-size: 16px;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #999;
}

.close-btn:hover {
  color: #333;
}

.debug-modal-body {
  padding: 20px;
  max-height: 60vh;
  overflow-y: auto;
}

.debug-section {
  margin-bottom: 20px;
}

.debug-section h4 {
  margin: 0 0 10px 0;
  font-size: 14px;
  color: #606266;
}

.debug-section p {
  margin: 5px 0;
  font-size: 13px;
  color: #303133;
}

.debug-section pre {
  background: #f5f7fa;
  padding: 10px;
  border-radius: 4px;
  overflow-x: auto;
  font-size: 12px;
  color: #303133;
  max-height: 200px;
  overflow-y: auto;
}

.debug-section pre.error {
  background: #fef0f0;
  color: #f56c6c;
}

.debug-section .success {
  color: #67c23a;
}

.debug-section .error {
  color: #f56c6c;
}

.debug-modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 15px 20px;
  border-top: 1px solid #ebeef5;
}

.debug-modal-footer button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.debug-modal-footer button:first-child {
  background: #f5f7fa;
  color: #606266;
}

.debug-modal-footer button:last-child {
  background: #409eff;
  color: white;
}
</style>
