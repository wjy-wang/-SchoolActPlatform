<template>
  <div class="activity-list">
    <div class="header">
      <button class="back-btn" @click="goBack">返回主页</button>
      <h2>活动列表</h2>
      <div class="actions">
        <select v-model="filterType" @change="handleFilter" class="filter-select">
          <option :value="null">全部类型</option>
          <option :value="0">讲座</option>
          <option :value="1">比赛</option>
          <option :value="2">晚会</option>
        </select>
        <select v-model="filterStatus" @change="handleFilter" class="filter-select">
          <option :value="null">全部状态</option>
          <option :value="0">未开始</option>
          <option :value="1">进行中</option>
          <option :value="2">已结束</option>
        </select>
      </div>
    </div>

    <div v-if="loading" class="loading">加载中...</div>

    <div v-else-if="activities.length === 0" class="empty">
      暂无活动
    </div>

    <div v-else class="activity-grid">
      <div
        v-for="activity in activities"
        :key="activity.id"
        class="activity-card"
      >
        <div class="card-poster" @click="goToDetail(activity.id)">
          <img v-if="activity.poster" :src="activity.poster" :alt="activity.title">
          <div v-else class="poster-placeholder">暂无海报</div>
        </div>
        <div class="card-content">
          <h3 class="card-title" @click="goToDetail(activity.id)">{{ activity.title }}</h3>
          <div class="card-info">
            <span class="type-badge" :class="'type-' + activity.type">
              {{ getTypeName(activity.type) }}
            </span>
            <span class="status-badge" :class="'status-' + activity.status">
              {{ getStatusName(activity.status) }}
            </span>
          </div>
          <div class="card-details">
            <p><i class="icon-time"></i> {{ formatTime(activity.start_time) }}</p>
            <p><i class="icon-location"></i> {{ activity.location }}</p>
            <p><i class="icon-user"></i> {{ activity.created_by_name }}</p>
            <p><i class="icon-enroll"></i> {{ activity.enrollment_count }} 人已报名</p>
          </div>
        </div>
        <div v-if="isAdmin" class="card-actions">
          <button class="btn-edit" @click="goToEdit(activity.id)">编辑</button>
          <button class="btn-delete" @click="handleDelete(activity.id)">删除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { getActivityList, deleteActivity } from '@/api/activity'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()
const activities = ref([])
const loading = ref(false)
const filterType = ref(null)
const filterStatus = ref(null)

const isAdmin = computed(() => userStore.user?.role === 1)

const getTypeName = (type) => {
  const types = { 0: '讲座', 1: '比赛', 2: '晚会' }
  return types[type] || '未知'
}

const getStatusName = (status) => {
  const statuses = { 0: '未开始', 1: '进行中', 2: '已结束' }
  return statuses[status] || '未知'
}

const formatTime = (time) => {
  if (!time) return ''
  return new Date(time).toLocaleString('zh-CN')
}

const handleFilter = async () => {
  await fetchActivities()
}

const fetchActivities = async () => {
  loading.value = true
  try {
    const params = {}
    if (filterType.value !== null) params.type = filterType.value
    if (filterStatus.value !== null) params.status = filterStatus.value

    const response = await getActivityList(params)
    activities.value = response.activities || []
  } catch (error) {
    ElMessage.error('获取活动列表失败')
  } finally {
    loading.value = false
  }
}

const goToDetail = (id) => {
  router.push(`/activities/${id}`)
}

const goToEdit = (id) => {
  router.push(`/activities/${id}/edit`)
}

const handleDelete = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除这个活动吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteActivity(id)
    ElMessage.success('删除成功')
    await fetchActivities()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const goBack = () => {
  router.push('/home')
}

onMounted(() => {
  fetchActivities()
})
</script>

<style scoped>
/* 🎨 活动列表容器 - 柔和渐变背景 */
.activity-list {
  min-height: 100vh;
  padding: 40px 20px;
  background: linear-gradient(135deg, #f0f4ff 0%, #faf0ff 50%, #f5f0ff 100%);
}

/* 🎨 Header - 毛玻璃效果 */
.header {
  max-width: 1400px;
  margin: 0 auto 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 24px;
  padding: 20px 24px;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.back-btn {
  padding: 12px 24px;
  background: rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 12px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  color: #4a5568;
  transition: all 0.3s ease;
}

.back-btn:hover {
  background: rgba(79, 70, 229, 0.1);
  color: #4F46E5;
  transform: translateY(-2px);
}

.header h2 {
  flex: 1;
  margin: 0;
  font-size: 28px;
  font-weight: 600;
  color: #1a1a2e;
  line-height: 1.5;
}

/* 🎨 筛选器 */
.actions {
  display: flex;
  gap: 12px;
}

.filter-select {
  padding: 12px 20px;
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 12px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  background: rgba(255, 255, 255, 0.5);
  color: #4a5568;
  transition: all 0.3s ease;
  min-width: 120px;
}

.filter-select:hover {
  background: rgba(255, 255, 255, 0.7);
  border-color: rgba(79, 70, 229, 0.3);
}

.filter-select:focus {
  outline: none;
  border-color: #4F46E5;
  box-shadow: 0 4px 16px rgba(79, 70, 229, 0.15);
}

/* 🎨 加载和空状态 */
.loading, .empty {
  text-align: center;
  padding: 80px 0;
  color: #6b7280;
  font-size: 18px;
  font-weight: 500;
}

/* 🎨 活动网格 - Grid布局 */
.activity-grid {
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
  padding: 0 20px;
}

/* 🎨 活动卡片 - 毛玻璃效果 */
.activity-card {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
}

.activity-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(79, 70, 229, 0.15);
  background: rgba(255, 255, 255, 0.85);
}

/* 🎨 海报区域 */
.card-poster {
  width: 100%;
  height: 200px;
  overflow: hidden;
  background: linear-gradient(135deg, rgba(79, 70, 229, 0.05) 0%, rgba(124, 58, 237, 0.05) 100%);
  cursor: pointer;
  position: relative;
}

.card-poster::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 60px;
  background: linear-gradient(to top, rgba(255, 255, 255, 0.8), transparent);
}

.card-poster img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.activity-card:hover .card-poster img {
  transform: scale(1.05);
}

.poster-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  font-size: 16px;
  font-weight: 500;
}

/* 🎨 卡片内容 */
.card-content {
  padding: 20px;
  flex: 1;
}

.card-title {
  margin: 0 0 12px 0;
  font-size: 20px;
  font-weight: 600;
  color: #1a1a2e;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  cursor: pointer;
  transition: all 0.3s ease;
  line-height: 1.5;
}

.card-title:hover {
  color: #4F46E5;
}

/* 🎨 标签样式 - 圆点 + 文字 */
.card-info {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.type-badge, .status-badge {
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 6px;
}

.type-badge::before, .status-badge::before {
  content: '';
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
}

.type-0 {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
}

.type-1 {
  background: rgba(79, 70, 229, 0.1);
  color: #4F46E5;
}

.type-2 {
  background: rgba(236, 72, 153, 0.1);
  color: #ec4899;
}

.status-0 {
  background: rgba(107, 114, 128, 0.1);
  color: #6b7280;
}

.status-1 {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
}

.status-2 {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

/* 🎨 详情信息 */
.card-details {
  font-size: 14px;
  color: #6b7280;
  line-height: 1.6;
}

.card-details p {
  margin: 8px 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 🎨 操作按钮 */
.card-actions {
  display: flex;
  border-top: 1px solid rgba(255, 255, 255, 0.3);
}

.card-actions button {
  flex: 1;
  padding: 12px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-edit {
  background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
  color: white;
}

.btn-edit:hover {
  background: linear-gradient(135deg, #5B21B6 0%, #8B5CF6 100%);
  filter: brightness(1.1);
}

.btn-delete {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  border-left: 1px solid rgba(255, 255, 255, 0.3);
}

.btn-delete:hover {
  background: linear-gradient(135deg, #f87171 0%, #ef4444 100%);
  filter: brightness(1.1);
}
</style>
