<template>
  <div class="my-favorites">
    <div class="header">
      <button class="back-btn" @click="goBack">返回</button>
      <h2>我的收藏</h2>
    </div>

    <div v-if="loading" class="loading">加载中...</div>

    <div v-else-if="favorites.length === 0" class="empty">
      暂无收藏记录
    </div>

    <div v-else class="favorite-grid">
      <div
        v-for="favorite in favorites"
        :key="favorite.id"
        class="favorite-card"
        @click="goToActivity(favorite.activity)"
      >
        <div class="card-content">
          <h3>{{ favorite.activity_title }}</h3>
          <div class="card-info">
            <span class="type-badge" :class="'type-' + favorite.activity_type">
              {{ getTypeName(favorite.activity_type) }}
            </span>
            <span>{{ formatTime(favorite.activity_start_time) }}</span>
            <span>{{ favorite.activity_location }}</span>
          </div>
        </div>
        <button class="btn-cancel" @click.stop="handleCancel(favorite.id)">取消收藏</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getMyFavorites, cancelFavorite } from '@/api/activity'

const router = useRouter()
const favorites = ref([])
const loading = ref(false)

const getTypeName = (type) => {
  const types = { 0: '讲座', 1: '比赛', 2: '晚会' }
  return types[type] || '未知'
}

const formatTime = (time) => {
  if (!time) return ''
  return new Date(time).toLocaleString('zh-CN')
}

const fetchFavorites = async () => {
  loading.value = true
  try {
    const response = await getMyFavorites()
    favorites.value = response.favorites || []
  } catch (error) {
    ElMessage.error('获取收藏记录失败')
  } finally {
    loading.value = false
  }
}

const handleCancel = async (id) => {
  try {
    await ElMessageBox.confirm('确定要取消收藏吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await cancelFavorite(id)
    ElMessage.success('取消收藏成功')
    await fetchFavorites()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('取消收藏失败')
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
  fetchFavorites()
})
</script>

<style scoped>
.my-favorites {
  padding: 20px;
  max-width: 1200px;
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

.favorite-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.favorite-card {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.favorite-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.card-content {
  padding: 15px;
}

.card-content h3 {
  margin: 0 0 10px 0;
  font-size: 18px;
  color: #333;
}

.card-info {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  font-size: 14px;
  color: #666;
}

.type-badge {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.type-0 { background: #e3f2fd; color: #1976d2; }
.type-1 { background: #fff3e0; color: #f57c00; }
.type-2 { background: #fce4ec; color: #c2185b; }

.btn-cancel {
  width: 100%;
  padding: 10px;
  background: #f5f5f5;
  color: #666;
  border: none;
  cursor: pointer;
}

.btn-cancel:hover {
  background: #ffe4e4;
  color: #f56c6c;
}
</style>
