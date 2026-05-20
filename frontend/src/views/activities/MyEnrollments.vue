<template>
  <div class="my-enrollments">
    <div class="header">
      <button class="back-btn" @click="goBack">返回</button>
      <h2>我的报名</h2>
    </div>

    <div v-if="loading" class="loading">加载中...</div>

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
          <h3>{{ enrollment.activity_title }}</h3>
          <div class="enrollment-meta">
            <span>报名时间：{{ formatTime(enrollment.created_at) }}</span>
            <span class="status-badge" :class="'status-' + enrollment.status">
              {{ enrollment.status === 0 ? '待确认' : '已确认' }}
            </span>
          </div>
        </div>
        <button class="btn-cancel" @click.stop="handleCancel(enrollment.id)">取消报名</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getMyEnrollments, cancelEnrollment } from '@/api/activity'

const router = useRouter()
const enrollments = ref([])
const loading = ref(false)

const formatTime = (time) => {
  if (!time) return ''
  return new Date(time).toLocaleString('zh-CN')
}

const fetchEnrollments = async () => {
  loading.value = true
  try {
    const response = await getMyEnrollments()
    enrollments.value = response.enrollments || []
  } catch (error) {
    ElMessage.error('获取报名记录失败')
  } finally {
    loading.value = false
  }
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

const goToActivity = (activityId) => {
  router.push(`/activities/${activityId}`)
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
</style>
