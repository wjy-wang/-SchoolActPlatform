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
.activity-form {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.form-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 30px;
}

.back-btn {
  padding: 8px 16px;
  background: #f5f5f5;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.form-header h2 {
  margin: 0;
  font-size: 24px;
}

.form-content {
  background: #fff;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: #333;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  box-sizing: border-box;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #409eff;
}

.form-group textarea {
  resize: vertical;
  line-height: 1.6;
}

.form-row {
  display: flex;
  gap: 20px;
}

.form-row .form-group {
  flex: 1;
}

.form-actions {
  display: flex;
  gap: 15px;
  margin-top: 30px;
}

.btn-submit, .btn-cancel {
  padding: 12px 30px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}

.btn-submit {
  background: #409eff;
  color: white;
}

.btn-submit:hover {
  background: #66b1ff;
}

.btn-submit:disabled {
  background: #a0cfff;
  cursor: not-allowed;
}

.btn-cancel {
  background: #909399;
  color: white;
}

.btn-cancel:hover {
  background: #a6a9ad;
}
</style>
