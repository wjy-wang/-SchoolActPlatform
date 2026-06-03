<template>
  <div class="activity-detail">
    <!-- 返回按钮 -->
    <div class="back-nav">
      <el-button link @click="goBack">
        <el-icon><ArrowLeft /></el-icon>
        返回
      </el-button>
    </div>

    <!-- 活动详情卡片 -->
    <el-card class="activity-card" v-loading="activityLoading">
      <template #header>
        <div class="activity-header">
          <h2>{{ activity.title }}</h2>
          <div class="activity-actions">
            <el-tag :type="getStatusType(activity.status)">
              {{ getStatusText(activity.status) }}
            </el-tag>
            <!-- 编辑按钮 -->
            <el-button
              v-if="activity.can_edit"
              link
              type="primary"
              @click="goToEdit"
            >
              <el-icon><Edit /></el-icon>
              编辑
            </el-button>
            <!-- 删除按钮 -->
            <el-button
              v-if="activity.can_delete"
              link
              type="danger"
              @click="handleDeleteActivity"
            >
              <el-icon><Delete /></el-icon>
              删除
            </el-button>
          </div>
        </div>
      </template>

      <div class="activity-content">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-image
              :src="activity.poster || '/default-activity.png'"
              fit="cover"
              class="activity-poster"
            />
          </el-col>
          <el-col :span="16">
            <el-descriptions :column="1" border>
              <el-descriptions-item label="活动类型">
                {{ getTypeText(activity.type) }}
              </el-descriptions-item>
              <el-descriptions-item label="活动时间">
                {{ formatTime(activity.start_time) }} ~ {{ formatTime(activity.end_time) }}
              </el-descriptions-item>
              <el-descriptions-item label="活动地点">
                {{ activity.location }}
              </el-descriptions-item>
              <el-descriptions-item label="组织者">
                {{ activity.organizer }}
              </el-descriptions-item>
              <el-descriptions-item label="活动描述">
                {{ activity.description }}
              </el-descriptions-item>
              <el-descriptions-item label="报名人数">
                {{ activity.enrollment_count }} 人
              </el-descriptions-item>
            </el-descriptions>
            
            <!-- 操作按钮 -->
            <div class="activity-actions-row" v-if="userStore.isLoggedIn">
              <!-- 报名按钮 -->
              <el-button
                v-if="!activity.is_enrolled"
                type="primary"
                @click="handleEnroll"
              >
                <el-icon><User /></el-icon>
                报名活动
              </el-button>
              <el-button
                v-else
                type="success"
                @click="handleCancelEnroll"
              >
                <el-icon><User /></el-icon>
                已报名
              </el-button>
              
              <!-- 收藏按钮 -->
              <el-button
                v-if="!activity.is_favorited"
                type="info"
                @click="handleFavorite"
              >
                <el-icon><Star /></el-icon>
                收藏活动
              </el-button>
              <el-button
                v-else
                type="warning"
                @click="handleCancelFavorite"
              >
                <el-icon><Star /></el-icon>
                已收藏
              </el-button>
            </div>
            <div v-else class="login-prompt">
              <el-alert
                title="请先登录后再进行报名和收藏"
                type="info"
                :closable="false"
              >
                <template #default>
                  <el-button link type="primary" @click="goToLogin">去登录</el-button>
                </template>
              </el-alert>
            </div>
          </el-col>
        </el-row>
      </div>
    </el-card>

    <!-- 评论区域 -->
    <el-card class="comments-card">
      <template #header>
        <div class="comments-header">
          <h3>
            <el-icon><ChatDotRound /></el-icon>
            评论列表
            <el-tag v-if="commentsCount > 0" type="info" size="small">
              {{ commentsCount }}
            </el-tag>
          </h3>
        </div>
      </template>

      <!-- 评论输入框（需登录） -->
      <div v-if="userStore.isLoggedIn" class="comment-input-section">
        <el-input
          v-model="newComment"
          type="textarea"
          :rows="3"
          placeholder="写下你的评论..."
          maxlength="500"
          show-word-limit
          resize="none"
        />
        <div class="comment-actions">
          <el-button
            type="primary"
            :loading="submitting"
            :disabled="!newComment.trim()"
            @click="submitComment"
          >
            发布评论
          </el-button>
        </div>
      </div>
      <div v-else class="login-tip">
        <el-alert
          title="请先登录后再发表评论"
          type="info"
          :closable="false"
        >
          <template #default>
            <el-button link type="primary" @click="goToLogin">去登录</el-button>
          </template>
        </el-alert>
      </div>

      <!-- 评论列表 -->
      <div class="comments-list" v-loading="commentsLoading">
        <!-- 空评论提示 -->
        <el-empty
          v-if="!commentsLoading && comments.length === 0"
          description="暂无评论，快来发表第一条评论吧！"
        />

        <!-- 评论项 -->
        <div
          v-for="comment in comments"
          :key="comment.id"
          class="comment-item"
        >
          <div class="comment-avatar">
            <el-avatar
              :size="40"
              :src="getAvatarUrl(comment.user)"
            >
              {{ comment.user?.username?.charAt(0)?.toUpperCase() || 'U' }}
            </el-avatar>
          </div>
          <div class="comment-content">
            <div class="comment-header">
              <span class="comment-author">{{ comment.user?.username }}</span>
              <span class="comment-time">{{ formatTime(comment.created_at) }}</span>
              <!-- 删除按钮（仅管理员或评论作者可见） -->
              <el-button
                v-if="canDeleteComment(comment)"
                link
                type="danger"
                size="small"
                :loading="deletingId === comment.id"
                @click="handleDeleteComment(comment)"
              >
                <el-icon><Delete /></el-icon>
                删除
              </el-button>
            </div>
            <div class="comment-text">{{ comment.content }}</div>
          </div>
        </div>

        <!-- 分页 -->
        <div v-if="commentsCount > pageSize" class="pagination">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :total="commentsCount"
            :page-sizes="[10, 20, 50]"
            layout="total, sizes, prev, pager, next"
            @size-change="handleSizeChange"
            @current-change="handlePageChange"
          />
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft, ChatDotRound, Delete, Edit, Star, User } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { getActivityComments, createComment, deleteComment } from '@/api/comment'
import { getActivityDetail, deleteActivity, enrollActivity, cancelEnrollment, favoriteActivity, cancelFavorite } from '@/api/activity'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

// 活动数据
const activity = ref({
  id: null,
  title: '',
  type: 0,
  status: 0,
  start_time: '',
  end_time: '',
  location: '',
  organizer: '',
  description: '',
  poster: '',
  can_edit: false,
  can_delete: false,
  is_enrolled: false,
  is_favorited: false,
  enrollment_count: 0
})
const activityLoading = ref(false)
const enrollmentId = ref(null)
const favoriteId = ref(null)

// 评论数据
const comments = ref([])
const commentsLoading = ref(false)
const commentsCount = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const newComment = ref('')
const submitting = ref(false)
const deletingId = ref(null)

// 获取活动ID
const activityId = computed(() => route.params.id)

// 判断是否可以删除评论
const canDeleteComment = (comment) => {
  if (!userStore.isLoggedIn) return false
  // 管理员可以删除任何评论
  if (userStore.isAdmin) return true
  // 普通用户只能删除自己的评论
  return comment.user?.id === userStore.userInfo?.id
}

// 获取头像URL
const getAvatarUrl = (user) => {
  // 可以根据需要返回默认头像或用户头像
  return null
}

// 获取状态类型
const getStatusType = (status) => {
  const types = { 0: 'info', 1: 'success', 2: 'danger' }
  return types[status] || 'info'
}

// 获取状态文本
const getStatusText = (status) => {
  const texts = { 0: '未开始', 1: '进行中', 2: '已结束' }
  return texts[status] || '未知'
}

// 获取类型文本
const getTypeText = (type) => {
  const texts = { 0: '讲座', 1: '比赛', 2: '晚会' }
  return texts[type] || '其他'
}

// 格式化时间
const formatTime = (time) => {
  if (!time) return '-'
  return new Date(time).toLocaleString('zh-CN')
}

// 返回上一页
const goBack = () => {
  router.back()
}

// 去登录
const goToLogin = () => {
  router.push('/login')
}

// 获取活动详情
const fetchActivityDetail = async () => {
  activityLoading.value = true
  try {
    const res = await getActivityDetail(activityId.value)
    activity.value = res.activity
  } catch (error) {
    ElMessage.error('获取活动详情失败')
  } finally {
    activityLoading.value = false
  }
}

// 跳转到编辑页面
const goToEdit = () => {
  router.push(`/activities/${activityId.value}/edit`)
}

// 删除活动
const handleDeleteActivity = async () => {
  try {
    await ElMessageBox.confirm('确定要删除这个活动吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await deleteActivity(activityId.value)
    ElMessage.success('活动删除成功')
    router.push('/activities')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('活动删除失败')
    }
  }
}

// 报名活动
const handleEnroll = async () => {
  try {
    const res = await enrollActivity({ activity: activityId.value })
    ElMessage.success('报名成功')
    activity.value.is_enrolled = true
    activity.value.enrollment_count++
    enrollmentId.value = res.enrollment.id
  } catch (error) {
    ElMessage.error('报名失败')
  }
}

// 取消报名
const handleCancelEnroll = async () => {
  try {
    if (enrollmentId.value) {
      await cancelEnrollment(enrollmentId.value)
    } else {
      // 如果没有 enrollmentId，尝试通过活动ID取消
      // 这里可能需要调用一个新的API或使用其他方式
      ElMessage.error('无法取消报名')
      return
    }
    ElMessage.success('取消报名成功')
    activity.value.is_enrolled = false
    activity.value.enrollment_count--
    enrollmentId.value = null
  } catch (error) {
    ElMessage.error('取消报名失败')
  }
}

// 收藏活动
const handleFavorite = async () => {
  try {
    const res = await favoriteActivity({ activity: activityId.value })
    ElMessage.success('收藏成功')
    activity.value.is_favorited = true
    favoriteId.value = res.favorite.id
  } catch (error) {
    ElMessage.error('收藏失败')
  }
}

// 取消收藏
const handleCancelFavorite = async () => {
  try {
    if (favoriteId.value) {
      await cancelFavorite(favoriteId.value)
    } else {
      ElMessage.error('无法取消收藏')
      return
    }
    ElMessage.success('取消收藏成功')
    activity.value.is_favorited = false
    favoriteId.value = null
  } catch (error) {
    ElMessage.error('取消收藏失败')
  }
}

// 获取评论列表
const fetchComments = async () => {
  commentsLoading.value = true
  try {
    const res = await getActivityComments(activityId.value, {
      page: currentPage.value,
      page_size: pageSize.value
    })
    comments.value = res.results || []
    commentsCount.value = res.count || 0
  } catch (error) {
    ElMessage.error('获取评论列表失败')
  } finally {
    commentsLoading.value = false
  }
}

// 提交评论
const submitComment = async () => {
  const content = newComment.value.trim()
  if (!content) {
    ElMessage.warning('评论内容不能为空')
    return
  }

  submitting.value = true
  try {
    await createComment(activityId.value, { content })
    ElMessage.success('评论发布成功')
    newComment.value = ''
    // 刷新评论列表
    currentPage.value = 1
    await fetchComments()
  } catch (error) {
    ElMessage.error('评论发布失败')
  } finally {
    submitting.value = false
  }
}

// 删除评论
const handleDeleteComment = async (comment) => {
  try {
    await ElMessageBox.confirm('确定要删除这条评论吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    deletingId.value = comment.id
    await deleteComment(comment.id)
    ElMessage.success('评论删除成功')
    await fetchComments()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('评论删除失败')
    }
  } finally {
    deletingId.value = null
  }
}

// 分页大小变化
const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  fetchComments()
}

// 页码变化
const handlePageChange = (page) => {
  currentPage.value = page
  fetchComments()
}

// 监听活动ID变化
watch(() => activityId.value, () => {
  if (activityId.value) {
    fetchActivityDetail()
    fetchComments()
  }
})

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

.back-nav {
  margin-bottom: 20px;
}

.activity-card {
  margin-bottom: 20px;
}

.activity-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.activity-header h2 {
  margin: 0;
  font-size: 20px;
}

.activity-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.activity-actions-row {
  display: flex;
  gap: 12px;
  margin-top: 20px;
}

.login-prompt {
  margin-top: 15px;
}

.activity-poster {
  width: 100%;
  height: 200px;
  border-radius: 8px;
}

.comments-card {
  margin-top: 20px;
}

.comments-header {
  display: flex;
  align-items: center;
}

.comments-header h3 {
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
}

.comment-input-section {
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #ebeef5;
}

.comment-actions {
  margin-top: 10px;
  text-align: right;
}

.login-tip {
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #ebeef5;
}

.comments-list {
  min-height: 200px;
}

.comment-item {
  display: flex;
  gap: 12px;
  padding: 16px 0;
  border-bottom: 1px solid #ebeef5;
}

.comment-item:last-child {
  border-bottom: none;
}

.comment-avatar {
  flex-shrink: 0;
}

.comment-content {
  flex: 1;
  min-width: 0;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.comment-author {
  font-weight: 500;
  color: #303133;
}

.comment-time {
  font-size: 12px;
  color: #909399;
}

.comment-text {
  color: #606266;
  line-height: 1.6;
  word-break: break-word;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>
