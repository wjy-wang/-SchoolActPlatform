<template>
  <div class="activity-detail">
    <div v-if="loading" class="loading">加载中...</div>

    <div v-else-if="activity" class="detail-content">
      <div class="detail-header">
        <button class="back-btn" @click="goBack">返回列表</button>
        <h2>{{ activity.title }}</h2>
        <div class="actions">
          <button v-if="isAdmin" class="btn-edit" @click="goToEdit">编辑活动</button>
          <button v-if="isAdmin" class="btn-delete" @click="handleDelete">删除活动</button>
        </div>
      </div>

      <div class="detail-body">
        <div class="poster-section">
          <img v-if="activity.poster" :src="activity.poster" :alt="activity.title">
          <div v-else class="poster-placeholder">暂无海报</div>
        </div>

        <div class="info-section">
          <div class="info-row">
            <span class="label">活动类型：</span>
            <span class="type-badge" :class="'type-' + activity.type">{{ getTypeName(activity.type) }}</span>
          </div>
          <div class="info-row">
            <span class="label">活动状态：</span>
            <span class="status-badge" :class="'status-' + activity.status">{{ getStatusName(activity.status) }}</span>
          </div>
          <div class="info-row">
            <span class="label">开始时间：</span>
            <span>{{ formatTime(activity.start_time) }}</span>
          </div>
          <div class="info-row">
            <span class="label">结束时间：</span>
            <span>{{ formatTime(activity.end_time) }}</span>
          </div>
          <div class="info-row">
            <span class="label">活动地点：</span>
            <span>{{ activity.location }}</span>
          </div>
          <div class="info-row">
            <span class="label">组织者：</span>
            <span>{{ activity.organizer }}</span>
          </div>
          <div class="info-row">
            <span class="label">创建者：</span>
            <span>{{ activity.created_by_name }}</span>
          </div>
          <div class="info-row">
            <span class="label">报名人数：</span>
            <span>{{ activity.enrollment_count }} 人</span>
          </div>

          <div class="user-actions">
            <button
              v-if="isLoggedIn && !activity.is_enrolled"
              class="btn-enroll"
              @click="handleEnroll"
              :disabled="activity.status === 2"
            >
              报名参加
            </button>
            <button
              v-else-if="isLoggedIn && activity.is_enrolled"
              class="btn-cancel-enroll"
              @click="handleCancelEnroll"
            >
              取消报名
            </button>

            <button
              v-if="isLoggedIn && !activity.is_favorited"
              class="btn-favorite"
              @click="handleFavorite"
            >
              收藏
            </button>
            <button
              v-else-if="isLoggedIn && activity.is_favorited"
              class="btn-cancel-favorite"
              @click="handleCancelFavorite"
            >
              取消收藏
            </button>
          </div>
        </div>
      </div>

      <div class="description-section">
        <h3>活动描述</h3>
        <p>{{ activity.description }}</p>
      </div>

      <div class="comments-section">
        <h3>评论 ({{ comments.length }})</h3>

        <div v-if="isLoggedIn" class="comment-form">
          <textarea
            v-model="newComment"
            placeholder="请输入评论内容..."
            class="comment-input"
          ></textarea>
          <button class="btn-submit-comment" @click="handleSubmitComment">发表评论</button>
        </div>
        <div v-else class="login-tip">
          请登录后发表评论
        </div>

        <div class="comments-list">
          <div v-for="comment in comments" :key="comment.id" class="comment-item">
            <div class="comment-header">
              <span class="comment-user">{{ comment.username }}</span>
              <span v-if="comment.user_role === 1" class="admin-tag">管理员</span>
              <span class="comment-time">{{ formatTime(comment.created_at) }}</span>
              <button
                v-if="isLoggedIn && (comment.user === userId || isAdmin)"
                class="btn-delete-comment"
                @click="handleDeleteComment(comment.id)"
              >
                删除
              </button>
            </div>
            <div class="comment-content">{{ comment.content }}</div>
          </div>

          <div v-if="comments.length === 0" class="no-comments">
            暂无评论
          </div>
        </div>
      </div>
    </div>

    <div v-else class="not-found">
      活动不存在
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/user'
import {
  getActivityDetail,
  enrollActivity,
  cancelEnrollment,
  favoriteActivity,
  cancelFavorite,
  getActivityComments,
  createComment,
  deleteComment,
  deleteActivity
} from '@/api/activity'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const activity = ref(null)
const comments = ref([])
const newComment = ref('')
const loading = ref(false)

const isLoggedIn = computed(() => userStore.isLoggedIn)
const isAdmin = computed(() => userStore.user?.role === 1)
const userId = computed(() => userStore.user?.id)

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

const fetchActivityDetail = async () => {
  loading.value = true
  try {
    const response = await getActivityDetail(route.params.id)
    activity.value = response.activity
  } catch (error) {
    ElMessage.error('获取活动详情失败')
  } finally {
    loading.value = false
  }
}

const fetchComments = async () => {
  try {
    const response = await getActivityComments(route.params.id)
    comments.value = response.comments || []
  } catch (error) {
    console.error('获取评论失败:', error)
  }
}

const handleEnroll = async () => {
  try {
    await enrollActivity({ activity: route.params.id })
    ElMessage.success('报名成功')
    await fetchActivityDetail()
  } catch (error) {
    ElMessage.error(error.response?.data?.activity?.[0] || '报名失败')
  }
}

const handleCancelEnroll = async () => {
  try {
    await ElMessageBox.confirm('确定要取消报名吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    const enrollmentId = activity.value.enrollment_id
    if (enrollmentId) {
      await cancelEnrollment(enrollmentId)
      ElMessage.success('取消报名成功')
      await fetchActivityDetail()
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('取消报名失败')
    }
  }
}

const handleFavorite = async () => {
  try {
    await favoriteActivity({ activity: route.params.id })
    ElMessage.success('收藏成功')
    await fetchActivityDetail()
  } catch (error) {
    ElMessage.error(error.response?.data?.activity?.[0] || '收藏失败')
  }
}

const handleCancelFavorite = async () => {
  try {
    const favoriteId = activity.value.favorite_id
    if (favoriteId) {
      await cancelFavorite(favoriteId)
      ElMessage.success('取消收藏成功')
      await fetchActivityDetail()
    }
  } catch (error) {
    ElMessage.error('取消收藏失败')
  }
}

const handleSubmitComment = async () => {
  if (!newComment.value.trim()) {
    ElMessage.warning('请输入评论内容')
    return
  }
  try {
    await createComment({
      activity: route.params.id,
      content: newComment.value
    })
    ElMessage.success('评论成功')
    newComment.value = ''
    await fetchComments()
  } catch (error) {
    ElMessage.error('评论失败')
  }
}

const handleDeleteComment = async (commentId) => {
  try {
    await ElMessageBox.confirm('确定要删除这条评论吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteComment(commentId)
    ElMessage.success('删除成功')
    await fetchComments()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleDelete = async () => {
  try {
    await ElMessageBox.confirm('确定要删除这个活动吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteActivity(route.params.id)
    ElMessage.success('删除成功')
    router.push('/activities')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const goBack = () => {
  router.push('/activities')
}

const goToEdit = () => {
  router.push(`/activities/form/${route.params.id}`)
}

onMounted(() => {
  fetchActivityDetail()
  fetchComments()
})
</script>

<style scoped>
.activity-detail {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.loading, .not-found {
  text-align: center;
  padding: 60px 0;
  color: #999;
  font-size: 16px;
}

.detail-header {
  display: flex;
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

.detail-header h2 {
  flex: 1;
  margin: 0;
  font-size: 24px;
}

.detail-header .actions {
  display: flex;
  gap: 10px;
}

.btn-edit, .btn-delete {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-edit {
  background: #409eff;
  color: white;
}

.btn-delete {
  background: #f56c6c;
  color: white;
}

.detail-body {
  display: flex;
  gap: 30px;
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.poster-section {
  flex: 0 0 400px;
}

.poster-section img {
  width: 100%;
  border-radius: 8px;
}

.poster-placeholder {
  width: 400px;
  height: 300px;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  border-radius: 8px;
}

.info-section {
  flex: 1;
}

.info-row {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  font-size: 16px;
}

.info-row .label {
  color: #666;
  margin-right: 10px;
}

.type-badge, .status-badge {
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 14px;
}

.type-0 { background: #e3f2fd; color: #1976d2; }
.type-1 { background: #fff3e0; color: #f57c00; }
.type-2 { background: #fce4ec; color: #c2185b; }

.status-0 { background: #f5f5f5; color: #666; }
.status-1 { background: #e8f5e9; color: #388e3c; }
.status-2 { background: #ffebee; color: #d32f2f; }

.user-actions {
  display: flex;
  gap: 15px;
  margin-top: 30px;
}

.btn-enroll, .btn-cancel-enroll, .btn-favorite, .btn-cancel-favorite {
  padding: 12px 30px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}

.btn-enroll {
  background: #409eff;
  color: white;
}

.btn-cancel-enroll {
  background: #909399;
  color: white;
}

.btn-favorite {
  background: #e6a23c;
  color: white;
}

.btn-cancel-favorite {
  background: #909399;
  color: white;
}

.description-section {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.description-section h3 {
  margin: 0 0 15px 0;
  font-size: 18px;
}

.description-section p {
  line-height: 1.8;
  color: #333;
  white-space: pre-wrap;
}

.comments-section {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.comments-section h3 {
  margin: 0 0 20px 0;
  font-size: 18px;
}

.comment-form {
  margin-bottom: 30px;
}

.comment-input {
  width: 100%;
  height: 100px;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  resize: vertical;
  margin-bottom: 10px;
}

.btn-submit-comment {
  padding: 10px 20px;
  background: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.login-tip {
  text-align: center;
  padding: 20px;
  color: #999;
  background: #f5f5f5;
  border-radius: 4px;
  margin-bottom: 20px;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.comment-item {
  padding: 15px;
  background: #f9f9f9;
  border-radius: 4px;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.comment-user {
  font-weight: bold;
  color: #333;
}

.admin-tag {
  padding: 2px 6px;
  background: #f56c6c;
  color: white;
  font-size: 12px;
  border-radius: 2px;
}

.comment-time {
  color: #999;
  font-size: 12px;
  margin-left: auto;
}

.btn-delete-comment {
  padding: 4px 10px;
  background: #f56c6c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.comment-content {
  line-height: 1.6;
  color: #333;
}

.no-comments {
  text-align: center;
  padding: 30px;
  color: #999;
}
</style>
