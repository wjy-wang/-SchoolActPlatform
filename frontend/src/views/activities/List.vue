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
.activity-list {
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
  font-size: 14px;
}

.header h2 {
  flex: 1;
  margin: 0;
  font-size: 24px;
  color: #333;
}

.actions {
  display: flex;
  gap: 10px;
}

.filter-select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
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
  display: flex;
  flex-direction: column;
}

.card-poster {
  width: 100%;
  height: 180px;
  overflow: hidden;
  background: #f5f5f5;
  cursor: pointer;
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
  flex: 1;
}

.card-title {
  margin: 0 0 10px 0;
  font-size: 18px;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  cursor: pointer;
}

.card-title:hover {
  color: #409eff;
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

.card-actions {
  display: flex;
  border-top: 1px solid #f0f0f0;
}

.card-actions button {
  flex: 1;
  padding: 10px;
  border: none;
  cursor: pointer;
  font-size: 14px;
}

.btn-edit {
  background: #409eff;
  color: white;
}

.btn-edit:hover {
  background: #66b1ff;
}

.btn-delete {
  background: #f56c6c;
  color: white;
  border-left: 1px solid #f0f0f0;
}

.btn-delete:hover {
  background: #f78989;
}
</style>
