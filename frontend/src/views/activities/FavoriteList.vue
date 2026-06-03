<template>
  <div class="favorite-list-page">
    <div class="header">
      <button class="back-btn" @click="goBack">返回</button>
      <h2>收藏名单</h2>
    </div>

    <div v-if="loading" class="loading">加载中...</div>

    <div v-else-if="favorites.length === 0" class="empty">
      暂无收藏记录
    </div>

    <div v-else class="favorite-table">
      <el-table :data="favorites" border>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="activity_title" label="活动名称" min-width="200" />
        <el-table-column prop="username" label="收藏用户" width="120" />
        <el-table-column prop="student_id" label="学号" width="120" />
        <el-table-column prop="created_at" label="收藏时间" width="180" />
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getAllFavorites } from '@/api/activity'

const router = useRouter()
const favorites = ref([])
const loading = ref(false)

const fetchFavorites = async () => {
  loading.value = true
  try {
    const response = await getAllFavorites()
    favorites.value = response.favorites || []
  } catch (error) {
    ElMessage.error('获取收藏名单失败')
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  router.push('/home')
}

onMounted(() => {
  fetchFavorites()
})
</script>

<style scoped>
.favorite-list-page {
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

.favorite-table {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>