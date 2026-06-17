<template>
  <div class="enrollment-list-page">
    <div class="header">
      <button class="back-btn" @click="goBack">返回</button>
      <h2>报名名单</h2>
    </div>

    <div v-if="loading" class="loading">加载中...</div>

    <div v-else-if="enrollments.length === 0" class="empty">
      暂无报名记录
    </div>

    <div v-else class="enrollment-table">
      <el-table :data="enrollments" border>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="activity_title" label="活动名称" min-width="200" />
        <el-table-column prop="username" label="报名用户" width="120" />
        <el-table-column prop="student_id" label="学号" width="120" />
        <el-table-column prop="created_at" label="报名时间" width="180" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.status === 0 ? 'warning' : 'success'">
              {{ scope.row.status === 0 ? '待确认' : '已确认' }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getAllEnrollments } from '@/api/activity'

const router = useRouter()
const enrollments = ref([])
const loading = ref(false)

const fetchEnrollments = async () => {
  loading.value = true
  try {
    const response = await getAllEnrollments()
    enrollments.value = response.enrollments || []
  } catch (error) {
    ElMessage.error('获取报名名单失败')
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  router.push('/home')
}

onMounted(() => {
  fetchEnrollments()
})
</script>

<style scoped>
/* 🎨 报名名单容器 - 柔和渐变背景 */
.enrollment-list-page {
  min-height: 100vh;
  padding: 40px 20px;
  background: linear-gradient(135deg, #f0f4ff 0%, #faf0ff 50%, #f5f0ff 100%);
}

/* 🎨 Header - 毛玻璃效果 */
.header {
  max-width: 1400px;
  margin: 0 auto 32px;
  display: flex;
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
  margin: 0;
  font-size: 28px;
  font-weight: 600;
  color: #1a1a2e;
  line-height: 1.5;
}

/* 🎨 加载和空状态 */
.loading, .empty {
  text-align: center;
  padding: 80px 0;
  color: #6b7280;
  font-size: 18px;
  font-weight: 500;
}

/* 🎨 表格容器 - 毛玻璃效果 */
.enrollment-table {
  max-width: 1400px;
  margin: 0 auto;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

/* 🎨 Element Plus 表格样式覆盖 */
.enrollment-table :deep(.el-table) {
  background: transparent;
}

.enrollment-table :deep(.el-table__header-wrapper) {
  background: linear-gradient(135deg, rgba(79, 70, 229, 0.05) 0%, rgba(124, 58, 237, 0.05) 100%);
}

.enrollment-table :deep(.el-table__header th) {
  background: transparent;
  color: #1a1a2e;
  font-weight: 600;
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
}

.enrollment-table :deep(.el-table__body tr) {
  background: rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
}

.enrollment-table :deep(.el-table__body tr:hover) {
  background: rgba(79, 70, 229, 0.05);
  transform: translateY(-2px);
}

.enrollment-table :deep(.el-table__body td) {
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
  color: #4a5568;
}

/* 🎨 状态标签样式 */
.enrollment-table :deep(.el-tag) {
  border-radius: 8px;
  padding: 4px 12px;
  font-weight: 500;
}
</style>