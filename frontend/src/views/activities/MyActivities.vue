<template>
  <div class="my-activities">
    <div class="header">
      <button class="back-btn" @click="goBack">返回</button>
      <h2>管理活动</h2>
      <button class="btn-create" @click="goToCreate">创建活动</button>
    </div>

    <div v-if="loading" class="loading">加载中...</div>

    <div v-else-if="activities.length === 0" class="empty">
      暂无创建的活动
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
            <p><i class="icon-enroll"></i> {{ activity.enrollment_count }} 人已报名</p>
          </div>
          <div class="card-actions">
            <button class="btn-edit" @click="goToEdit(activity.id)">编辑</button>
            <button class="btn-delete" @click="handleDelete(activity)">删除</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { getMyActivities, deleteActivity } from '@/api/activity'

const router = useRouter()
const userStore = useUserStore()
const activities = ref([])
const loading = ref(false)
const deletingId = ref(null)

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

const fetchActivities = async () => {
  loading.value = true
  try {
    const response = await getMyActivities()
    activities.value = response.activities || []
  } catch (error) {
    ElMessage.error('获取活动列表失败')
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  router.push('/home')
}

const goToCreate = () => {
  router.push('/activities/create')
}

const goToDetail = (id) => {
  router.push(`/activities/${id}`)
}

const goToEdit = (id) => {
  router.push(`/activities/edit/${id}`)
}

const handleDelete = async (activity) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除活动「${activity.title}」吗？此操作不可恢复。`,
      '确认删除',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'btn-danger'
      }
    )
    
    deletingId.value = activity.id
    await deleteActivity(activity.id)
    ElMessage.success('删除成功')
    activities.value = activities.value.filter(a => a.id !== activity.id)
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  } finally {
    deletingId.value = null
  }
}

onMounted(() => {
  if (!userStore.isAdmin) {
    ElMessage.error('只有管理员可以访问此页面')
    router.push('/home')
    return
  }
  fetchActivities()
})
</script>

<style scoped>
/* 🎨 我的活动容器 - 柔和渐变背景 */
.my-activities {
  min-height: 100vh;
  padding: 40px 20px;
  background: linear-gradient(135deg, #f0f4ff 0%, #faf0ff 50%, #f5f0ff 100%);
  position: relative;
  overflow: hidden;
}

.my-activities::before {
  content: '';
  position: fixed;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle at 30% 20%, rgba(79, 70, 229, 0.03) 0%, transparent 50%),
              radial-gradient(circle at 70% 80%, rgba(124, 58, 237, 0.03) 0%, transparent 50%),
              radial-gradient(circle at 50% 50%, rgba(168, 85, 247, 0.02) 0%, transparent 50%);
  pointer-events: none;
}

/* 🎨 Header - 毛玻璃效果 */
.header {
  max-width: 1400px;
  margin: 0 auto 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 24px;
  padding: 24px 32px;
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.6);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  position: relative;
  z-index: 1;
}

.back-btn {
  padding: 12px 24px;
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.8);
  border-radius: 12px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  color: #4a5568;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  gap: 8px;
}

.back-btn::before {
  content: '←';
  font-size: 16px;
}

.back-btn:hover {
  background: rgba(79, 70, 229, 0.1);
  color: #4F46E5;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.1);
}

.header h2 {
  flex: 1;
  margin: 0;
  font-size: 30px;
  font-weight: 700;
  color: #1a1a2e;
  line-height: 1.5;
  letter-spacing: -0.5px;
}

/* 🎨 创建活动按钮 - 渐变蓝紫色 */
.btn-create {
  padding: 16px 36px;
  background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
  color: white;
  border: none;
  border-radius: 14px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  box-shadow: 0 6px 20px rgba(79, 70, 229, 0.35);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.btn-create::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.btn-create:hover::before {
  left: 100%;
}

.btn-create:hover {
  background: linear-gradient(135deg, #5B21B6 0%, #8B5CF6 100%);
  box-shadow: 0 10px 30px rgba(79, 70, 229, 0.45);
  transform: translateY(-3px);
}

.btn-create:active {
  transform: translateY(-1px);
}

/* 🎨 加载和空状态 */
.loading, .empty {
  text-align: center;
  padding: 100px 0;
  color: #6b7280;
  font-size: 18px;
  font-weight: 500;
  position: relative;
  z-index: 1;
}

/* 🎨 活动网格 - Grid布局 */
.activity-grid {
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 28px;
  padding: 0 20px;
  position: relative;
  z-index: 1;
}

/* 🎨 活动卡片 - 毛玻璃效果 */
.activity-card {
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-radius: 20px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.6);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.activity-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 48px rgba(79, 70, 229, 0.15);
  background: rgba(255, 255, 255, 0.9);
}

/* 🎨 海报区域 */
.card-poster {
  width: 100%;
  height: 220px;
  overflow: hidden;
  background: linear-gradient(135deg, rgba(79, 70, 229, 0.05) 0%, rgba(124, 58, 237, 0.05) 100%);
  position: relative;
  cursor: pointer;
}

.card-poster::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 70px;
  background: linear-gradient(to top, rgba(255, 255, 255, 0.9), transparent);
}

.card-poster img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.activity-card:hover .card-poster img {
  transform: scale(1.08);
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
  padding: 24px;
}

.card-title {
  margin: 0 0 16px 0;
  font-size: 22px;
  font-weight: 700;
  color: #1a1a2e;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  line-height: 1.5;
  cursor: pointer;
  transition: color 0.3s ease;
}

.card-title:hover {
  color: #4F46E5;
}

/* 🎨 标签样式 - 圆点 + 文字 */
.card-info {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.type-badge, .status-badge {
  padding: 8px 14px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.3s ease;
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
  margin-bottom: 20px;
}

.card-details p {
  margin: 10px 0;
  display: flex;
  align-items: center;
  gap: 10px;
}

/* 🎨 卡片操作按钮 */
.card-actions {
  display: flex;
  gap: 12px;
  padding-top: 16px;
  border-top: 1px solid rgba(229, 231, 235, 0.4);
}

.btn-edit, .btn-delete {
  flex: 1;
  padding: 12px 20px;
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.btn-edit {
  background: linear-gradient(135deg, rgba(79, 70, 229, 0.08) 0%, rgba(124, 58, 237, 0.08) 100%);
  color: #4F46E5;
  border: 1px solid rgba(79, 70, 229, 0.2);
}

.btn-edit:hover {
  background: linear-gradient(135deg, rgba(79, 70, 229, 0.15) 0%, rgba(124, 58, 237, 0.15) 100%);
  color: #4338ca;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.15);
}

.btn-delete {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.08) 0%, rgba(236, 72, 153, 0.08) 100%);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.btn-delete:hover {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(236, 72, 153, 0.15) 100%);
  color: #dc2626;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.15);
}
</style>
