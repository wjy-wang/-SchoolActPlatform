<template>
  <el-container class="profile-container">
    <el-header class="header">
      <div class="header-left">
        <el-button link @click="goBack">
          <el-icon><ArrowLeft /></el-icon>
          返回
        </el-button>
        <h2>个人信息管理</h2>
      </div>
    </el-header>
    
    <el-main class="main-content">
      <el-card class="profile-card">
        <template #header>
          <div class="card-header">
            <span>修改个人信息</span>
          </div>
        </template>
        
        <el-form
          ref="profileFormRef"
          :model="profileForm"
          :rules="profileRules"
          label-width="100px"
          style="max-width: 500px"
        >
          <el-form-item label="用户名" prop="username">
            <el-input v-model="profileForm.username" placeholder="请输入用户名" />
          </el-form-item>
          
          <el-form-item label="学号" prop="student_id">
            <el-input v-model="profileForm.student_id" placeholder="请输入学号" />
          </el-form-item>
          
          <el-form-item label="邮箱" prop="email">
            <el-input v-model="profileForm.email" placeholder="请输入邮箱" />
          </el-form-item>
          
          <el-form-item label="手机号" prop="phone">
            <el-input v-model="profileForm.phone" placeholder="请输入手机号" />
          </el-form-item>
          
          <el-form-item>
            <el-button type="primary" :loading="loading" @click="handleUpdate">
              保存修改
            </el-button>
            <el-button @click="goBack">取消</el-button>
          </el-form-item>
        </el-form>
      </el-card>
      
      <el-card class="profile-card" style="margin-top: 20px">
        <template #header>
          <div class="card-header">
            <span>当前信息</span>
          </div>
        </template>
        
        <el-descriptions :column="2" border>
          <el-descriptions-item label="用户名">{{ userStore.userInfo?.username }}</el-descriptions-item>
          <el-descriptions-item label="学号">{{ userStore.userInfo?.student_id }}</el-descriptions-item>
          <el-descriptions-item label="邮箱">{{ userStore.userInfo?.email }}</el-descriptions-item>
          <el-descriptions-item label="手机号">{{ userStore.userInfo?.phone }}</el-descriptions-item>
          <el-descriptions-item label="角色">
            <el-tag :type="userStore.userInfo?.role === 1 ? 'danger' : 'success'">
              {{ userStore.userInfo?.role === 1 ? '管理员' : '普通用户' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="注册时间">
            {{ formatDate(userStore.userInfo?.date_joined) }}
          </el-descriptions-item>
        </el-descriptions>
      </el-card>
    </el-main>
  </el-container>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { updateProfile } from '@/api/auth'

const router = useRouter()
const userStore = useUserStore()
const profileFormRef = ref()
const loading = ref(false)

const profileForm = reactive({
  username: '',
  student_id: '',
  email: '',
  phone: ''
})

const profileRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  student_id: [
    { required: true, message: '请输入学号', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ]
}

onMounted(() => {
  // 加载当前用户信息
  const userInfo = userStore.userInfo
  if (userInfo) {
    profileForm.username = userInfo.username || ''
    profileForm.student_id = userInfo.student_id || ''
    profileForm.email = userInfo.email || ''
    profileForm.phone = userInfo.phone || ''
  }
})

const handleUpdate = async () => {
  const valid = await profileFormRef.value.validate().catch(() => false)
  if (!valid) return
  
  loading.value = true
  try {
    const res = await updateProfile(profileForm)
    ElMessage.success('修改成功')
    // 更新本地存储的用户信息
    if (res.user) {
      userStore.updateUserInfo(res.user)
    }
  } catch (error) {
    ElMessage.error(error.response?.data?.message || '修改失败')
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  router.push('/home')
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN')
}
</script>

<style scoped>
.profile-container {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.header {
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-left h2 {
  margin: 0;
  font-size: 18px;
  color: #303133;
}

.main-content {
  padding: 20px;
}

.profile-card {
  max-width: 800px;
  margin: 0 auto;
}

.card-header {
  font-weight: bold;
}
</style>
