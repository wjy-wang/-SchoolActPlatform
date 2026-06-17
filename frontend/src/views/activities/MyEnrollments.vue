<template>
  <div class="my-enrollments">
    <div class="header">
      <button class="back-btn" @click="goBack">返回</button>
      <h2>我的报名</h2>
      <button class="debug-btn" @click="showDebugModal = true">🔍 调试信息</button>
    </div>

    <div v-if="loading" class="loading">加载中...</div>

    <div v-else-if="error" class="empty error">
      <p>加载失败：{{ error }}</p>
      <button @click="fetchEnrollments">重试</button>
    </div>

    <div v-else-if="enrollments.length === 0" class="empty">
      暂无报名记录
    </div>

    <div v-else class="enrollment-list">
      <div
        v-for="enrollment in enrollments"
        :key="enrollment.id"
        class="enrollment-item"
        @click="goToActivity(enrollment.activity)"
      >
        <div class="enrollment-info">
          <h3>{{ enrollment.activity?.title || '未知活动' }}</h3>
          <div class="enrollment-meta">
            <span>活动类型：{{ getActivityType(enrollment.activity?.type) }}</span>
            <span>活动时间：{{ formatTime(enrollment.activity?.start_time) }}</span>
            <span>活动地点：{{ enrollment.activity?.location || '未知' }}</span>
            <span>报名时间：{{ formatTime(enrollment.created_at) }}</span>
            <span class="status-badge" :class="'status-' + enrollment.status">
              {{ enrollment.status === 0 ? '待确认' : '已确认' }}
            </span>
          </div>
        </div>
        <button class="btn-cancel" @click.stop="handleCancel(enrollment.id)">取消报名</button>
      </div>
    </div>

    <div v-if="showDebugModal" class="debug-modal" @click.self="showDebugModal = false">
      <div class="debug-modal-content">
        <div class="debug-modal-header">
          <h3>🔍 API调试信息 - 我的报名</h3>
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
import { getMyEnrollments, cancelEnrollment } from '@/api/activity'
import request from '@/utils/request'

const router = useRouter()
const enrollments = ref([])
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

const formatTime = (time) => {
  if (!time) return ''
  return new Date(time).toLocaleString('zh-CN')
}

const getActivityType = (type) => {
  const types = {
    0: '学术讲座',
    1: '体育竞技',
    2: '文艺演出',
    3: '社会实践'
  }
  return types[type] || '其他'
}

const fetchEnrollments = async () => {
  loading.value = true
  error.value = ''
  debugInfo.value = { url: '', status: 0, token: '', response: null, error: null }
  
  const token = localStorage.getItem('token')
  debugInfo.value.token = token
  
  try {
    debugInfo.value.url = '/api/enrollments/'
    
    const response = await getMyEnrollments()
    debugInfo.value.response = response
    debugInfo.value.status = 200
    
    enrollments.value = response.enrollments || []
  } catch (err) {
    error.value = err.message || '获取报名记录失败'
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
    await ElMessageBox.confirm('确定要取消报名吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await cancelEnrollment(id)
    ElMessage.success('取消报名成功')
    await fetchEnrollments()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('取消报名失败')
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
  fetchEnrollments()
})
</script>

<style scoped>
.my-enrollments {
  padding: 20px;
  max-width: 800px;
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

.enrollment-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.enrollment-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.enrollment-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.enrollment-info h3 {
  margin: 0 0 10px 0;
  font-size: 18px;
  color: #333;
}

.enrollment-meta {
  display: flex;
  gap: 15px;
  font-size: 14px;
  color: #666;
}

.status-badge {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.status-0 { background: #fff3e0; color: #f57c00; }
.status-1 { background: #e8f5e9; color: #388e3c; }

.btn-cancel {
  padding: 8px 16px;
  background: #f56c6c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
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
