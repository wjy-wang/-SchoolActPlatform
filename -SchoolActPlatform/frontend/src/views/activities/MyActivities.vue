<template>
  <div class="my-activities">
    <div class="header">
      <button class="back-btn" @click="goBack">返回</button>
      <h2>我的活动</h2>
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
        @click="goToDetail(activity.id)"
      >
        <div class="card-poster">
          <img v-if="activity.poster" :src="activity.poster" :alt="activity.title">
          <div v-else class="poster-placeholder">暂无海报</div>
        </div>
        <div class="card-content">
          <h3 class="card-title">{{ activity.title }}</h3>
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
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { getMyActivities } from '@/api/activity'

const router = useRouter()
const userStore = useUserStore()
const activities = ref([])
const loading = ref(false)

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
.my-activities {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  gap: 15px;
}

.back-btn {
  padding: 8px 16px;
  background: #f5f5f5;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.header h2 {
  flex: 1;
  margin: 0;
  font-size: 24px;
}

.btn-create {
  padding: 10px 20px;
  background: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.loading, .empty {
  text-align: center;
  padding: 60px 0;
  color: #999;
  font-size: 16px;
}

.activity-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.activity-card {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.activity-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.card-poster {
  width: 100%;
  height: 180px;
  overflow: hidden;
  background: #f5f5f5;
}

.card-poster img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.poster-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
}

.card-content {
  padding: 15px;
}

.card-title {
  margin: 0 0 10px 0;
  font-size: 18px;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-info {
  display: flex;
  gap: 8px;
  margin-bottom: 10px;
}

.type-badge, .status-badge {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.type-0 { background: #e3f2fd; color: #1976d2; }
.type-1 { background: #fff3e0; color: #f57c00; }
.type-2 { background: #fce4ec; color: #c2185b; }

.status-0 { background: #f5f5f5; color: #666; }
.status-1 { background: #e8f5e9; color: #388e3c; }
.status-2 { background: #ffebee; color: #d32f2f; }

.card-details {
  font-size: 14px;
  color: #666;
}

.card-details p {
  margin: 4px 0;
  display: flex;
  align-items: center;
  gap: 6px;
}
</style>
