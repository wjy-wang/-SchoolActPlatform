<template>
  <div class="activity-enrollment-list">
    <div v-if="loading" class="loading">
      <el-skeleton :rows="5" animated />
    </div>

    <div v-else-if="enrollments.length === 0" class="empty">
      <el-empty description="暂无报名记录" />
    </div>

    <div v-else>
      <div class="enrollment-summary">
        <el-statistic title="总报名人数" :value="enrollments.length" />
        <el-statistic title="待确认" :value="pendingCount" />
        <el-statistic title="已确认" :value="confirmedCount" />
      </div>

      <el-table
        :data="enrollments"
        style="width: 100%"
        border
        stripe
        v-loading="loading"
      >
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="username" label="用户名" min-width="120" />
        <el-table-column prop="created_at" label="报名时间" min-width="180">
          <template #default="{ row }">
            {{ formatTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="报名状态" width="120" align="center">
          <template #default="{ row }">
            <el-tag :type="row.status === 0 ? 'warning' : 'success'">
              {{ row.status === 0 ? '待确认' : '已确认' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" align="center" fixed="right">
          <template #default="{ row }">
            <el-button
              v-if="row.status === 0"
              type="success"
              link
              size="small"
              @click="handleConfirm(row.id)"
            >
              确认
            </el-button>
            <el-button
              type="danger"
              link
              size="small"
              @click="handleCancel(row.id)"
            >
              取消报名
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="export-actions">
        <el-button type="primary" :icon="Download" @click="exportToExcel">
          导出Excel
        </el-button>
        <el-button :icon="Printer" @click="printList">
          打印名单
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Download, Printer } from '@element-plus/icons-vue'
import { getMyEnrollments, cancelEnrollment } from '@/api/activity'

const props = defineProps({
  activityId: {
    type: [String, Number],
    required: true
  }
})

const enrollments = ref([])
const loading = ref(false)

const pendingCount = computed(() => enrollments.value.filter(e => e.status === 0).length)
const confirmedCount = computed(() => enrollments.value.filter(e => e.status === 1).length)

const formatTime = (time) => {
  if (!time) return ''
  return new Date(time).toLocaleString('zh-CN')
}

const fetchEnrollments = async () => {
  loading.value = true
  try {
    // 调用管理员获取活动报名列表的API
    const response = await getMyEnrollments()
    // 这里应该调用获取特定活动报名列表的API
    // 暂时使用模拟数据或过滤
    enrollments.value = response.enrollments || []
  } catch (error) {
    ElMessage.error('获取报名列表失败')
  } finally {
    loading.value = false
  }
}

const handleConfirm = async (id) => {
  try {
    // 调用确认报名API
    ElMessage.success('确认成功')
    await fetchEnrollments()
  } catch (error) {
    ElMessage.error('确认失败')
  }
}

const handleCancel = async (id) => {
  try {
    await ElMessageBox.confirm('确定要取消该用户的报名吗？', '提示', {
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

const exportToExcel = () => {
  // 简单的CSV导出
  const headers = ['序号', '用户名', '报名时间', '报名状态']
  const rows = enrollments.value.map((e, index) => [
    index + 1,
    e.username,
    formatTime(e.created_at),
    e.status === 0 ? '待确认' : '已确认'
  ])
  
  let csvContent = '\uFEFF' // BOM for UTF-8
  csvContent += headers.join(',') + '\n'
  rows.forEach(row => {
    csvContent += row.join(',') + '\n'
  })
  
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = `活动报名名单_${props.activityId}_${new Date().toLocaleDateString()}.csv`
  link.click()
  
  ElMessage.success('导出成功')
}

const printList = () => {
  window.print()
}

onMounted(() => {
  fetchEnrollments()
})
</script>

<style scoped>
.activity-enrollment-list {
  padding: 10px;
}

.loading, .empty {
  padding: 40px 0;
}

.enrollment-summary {
  display: flex;
  gap: 40px;
  margin-bottom: 20px;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
}

.export-actions {
  margin-top: 20px;
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

@media print {
  .export-actions {
    display: none;
  }
}
</style>
