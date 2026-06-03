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
.enrollment-list-page {
  padding: 20px;
  max-width: 1000px;
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

.enrollment-table {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>