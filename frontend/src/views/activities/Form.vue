<template>
  <div class="activity-form">
    <div class="form-header">
      <button class="back-btn" @click="goBack">返回</button>
      <h2>{{ isEdit ? '编辑活动' : '创建活动' }}</h2>
    </div>

    <form @submit.prevent="handleSubmit" class="form-content">
      <div class="form-group">
        <label>活动标题 *</label>
        <input
          v-model="form.title"
          type="text"
          required
          placeholder="请输入活动标题"
        >
      </div>

      <div class="form-group">
        <label>活动类型 *</label>
        <select v-model="form.type" required>
          <option :value="0">讲座</option>
          <option :value="1">比赛</option>
          <option :value="2">晚会</option>
        </select>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label>开始时间 *</label>
          <input
            v-model="form.start_time"
            type="datetime-local"
            required
          >
        </div>

        <div class="form-group">
          <label>结束时间 *</label>
          <input
            v-model="form.end_time"
            type="datetime-local"
            required
          >
        </div>
      </div>

      <div class="form-group">
        <label>活动地点 *</label>
        <input
          v-model="form.location"
          type="text"
          required
          placeholder="请输入活动地点"
        >
      </div>

      <div class="form-group">
        <label>组织者 *</label>
        <input
          v-model="form.organizer"
          type="text"
          required
          placeholder="请输入组织者"
        >
      </div>

      <div class="form-group">
        <label>活动海报URL</label>
        <input
          v-model="form.poster"
          type="url"
          placeholder="请输入海报图片URL（可选）"
        >
      </div>

      <div class="form-group">
        <label>活动描述 *</label>
        <textarea
          v-model="form.description"
          required
          placeholder="请输入活动描述"
          rows="8"
        ></textarea>
      </div>

      <div v-if="isEdit" class="form-group">
        <label>活动状态</label>
        <select v-model="form.status">
          <option :value="0">未开始</option>
          <option :value="1">进行中</option>
          <option :value="2">已结束</option>
        </select>
      </div>

      <div class="form-actions">
        <button type="submit" class="btn-submit" :disabled="submitting">
          {{ submitting ? '提交中...' : (isEdit ? '保存修改' : '创建活动') }}
        </button>
        <button type="button" class="btn-cancel" @click="goBack">取消</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { createActivity, updateActivity, getActivityDetail } from '@/api/activity'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const submitting = ref(false)
const loading = ref(false)

const isEdit = computed(() => !!route.params.id)

const form = reactive({
  title: '',
  type: 0,
  start_time: '',
  end_time: '',
  location: '',
  organizer: '',
  poster: '',
  description: '',
  status: 0
})

const fetchActivityDetail = async () => {
  if (!isEdit.value) return

  loading.value = true
  try {
    const response = await getActivityDetail(route.params.id)
    const activity = response.activity

    form.title = activity.title
    form.type = activity.type
    form.location = activity.location
    form.organizer = activity.organizer
    form.poster = activity.poster || ''
    form.description = activity.description
    form.status = activity.status

    if (activity.start_time) {
      form.start_time = formatDateTimeLocal(activity.start_time)
    }
    if (activity.end_time) {
      form.end_time = formatDateTimeLocal(activity.end_time)
    }
  } catch (error) {
    ElMessage.error('获取活动详情失败')
    router.push('/activities')
  } finally {
    loading.value = false
  }
}

const formatDateTimeLocal = (datetime) => {
  const date = new Date(datetime)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  return `${year}-${month}-${day}T${hours}:${minutes}`
}

const handleSubmit = async () => {
  if (form.start_time >= form.end_time) {
    ElMessage.warning('结束时间必须晚于开始时间')
    return
  }

  submitting.value = true
  try {
    const data = {
      ...form,
      start_time: new Date(form.start_time).toISOString(),
      end_time: new Date(form.end_time).toISOString()
    }

    if (isEdit.value) {
      await updateActivity(route.params.id, data)
      ElMessage.success('修改成功')
    } else {
      // 创建活动时不需要 status 字段
      delete data.status
      await createActivity(data)
      ElMessage.success('创建成功')
    }

    router.push('/activities')
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || (isEdit.value ? '修改失败' : '创建失败'))
  } finally {
    submitting.value = false
  }
}

const goBack = () => {
  router.back()
}

onMounted(() => {
  // 如果是创建活动，只有管理员可以访问
  if (!isEdit.value && !userStore.isAdmin) {
    ElMessage.error('只有管理员可以创建活动')
    router.push('/activities')
    return
  }
  fetchActivityDetail()
})
</script>

<style scoped>
/* 🎨 活动表单容器 - 柔和渐变背景 */
.activity-form {
  min-height: 100vh;
  padding: 40px 20px;
  background: linear-gradient(135deg, #f0f4ff 0%, #faf0ff 50%, #f5f0ff 100%);
  position: relative;
  overflow: hidden;
}

.activity-form::before {
  content: '';
  position: fixed;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle at 30% 20%, rgba(79, 70, 229, 0.03) 0%, transparent 50%),
              radial-gradient(circle at 70% 80%, rgba(124, 58, 237, 0.03) 0%, transparent 50%),
              radial-gradient(circle at 50% 50%, rgba(168, 85, 247, 0.02) 0%, transparent 50%);
  pointer-events: none;
}

/* 🎨 Form Header - 毛玻璃效果 */
.form-header {
  max-width: 800px;
  margin: 0 auto 32px;
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 24px 32px;
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.6);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  position: relative;
  z-index: 1;
}

.back-btn {
  padding: 12px 24px;
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.8);
  border-radius: 12px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  color: #4a5568;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  gap: 8px;
}

.back-btn::before {
  content: '←';
  font-size: 16px;
}

.back-btn:hover {
  background: rgba(79, 70, 229, 0.1);
  color: #4F46E5;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.1);
}

.form-header h2 {
  margin: 0;
  font-size: 30px;
  font-weight: 700;
  color: #1a1a2e;
  line-height: 1.5;
  letter-spacing: -0.5px;
}

/* 🎨 表单内容 - 毛玻璃卡片 */
.form-content {
  max-width: 800px;
  margin: 0 auto;
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  padding: 48px;
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.6);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  position: relative;
  z-index: 1;
}

/* 🎨 表单组 */
.form-group {
  margin-bottom: 28px;
  position: relative;
}

.form-group label {
  display: block;
  margin-bottom: 10px;
  font-weight: 600;
  color: #4a5568;
  font-size: 15px;
  letter-spacing: 0.3px;
}

.form-group label::after {
  content: '';
}

/* 🎨 表单输入框 */
.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 16px 20px;
  border: 2px solid rgba(229, 231, 235, 0.6);
  border-radius: 14px;
  font-size: 15px;
  box-sizing: border-box;
  background: rgba(255, 255, 255, 0.6);
  color: #1a1a2e;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-family: inherit;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: rgba(79, 70, 229, 0.4);
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.08), 0 8px 24px rgba(79, 70, 229, 0.1);
  transform: translateY(-1px);
}

.form-group input::placeholder,
.form-group textarea::placeholder {
  color: #9ca3af;
}

.form-group textarea {
  resize: vertical;
  line-height: 1.6;
  min-height: 180px;
}

/* 🎨 表单行 */
.form-row {
  display: flex;
  gap: 28px;
}

.form-row .form-group {
  flex: 1;
}

/* 🎨 表单操作按钮 */
.form-actions {
  display: flex;
  gap: 20px;
  margin-top: 40px;
  justify-content: flex-end;
  padding-top: 24px;
  border-top: 1px solid rgba(229, 231, 235, 0.4);
}

.btn-submit, .btn-cancel {
  padding: 16px 40px;
  border: none;
  border-radius: 14px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  letter-spacing: 0.5px;
}

.btn-submit {
  background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
  color: white;
  box-shadow: 0 6px 20px rgba(79, 70, 229, 0.35);
  position: relative;
  overflow: hidden;
}

.btn-submit::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.btn-submit:hover::before {
  left: 100%;
}

.btn-submit:hover {
  background: linear-gradient(135deg, #5B21B6 0%, #8B5CF6 100%);
  box-shadow: 0 10px 30px rgba(79, 70, 229, 0.45);
  transform: translateY(-3px);
}

.btn-submit:active {
  transform: translateY(-1px);
}

.btn-submit:disabled {
  background: linear-gradient(135deg, #cbd5e1 0%, #e2e8f0 100%);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.btn-submit:disabled::before {
  display: none;
}

.btn-cancel {
  background: rgba(255, 255, 255, 0.7);
  color: #6b7280;
  border: 2px solid rgba(229, 231, 235, 0.6);
}

.btn-cancel:hover {
  background: rgba(107, 114, 128, 0.08);
  color: #4a5568;
  border-color: rgba(107, 114, 128, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}
</style>
