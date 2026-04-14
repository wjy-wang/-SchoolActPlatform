<template>
  <el-container class="password-container">
    <el-header class="header">
      <div class="header-left">
        <el-button link @click="goBack">
          <el-icon><ArrowLeft /></el-icon>
          返回
        </el-button>
        <h2>修改密码</h2>
      </div>
    </el-header>
    
    <el-main class="main-content">
      <el-card class="password-card">
        <template #header>
          <div class="card-header">
            <span>修改登录密码</span>
          </div>
        </template>
        
        <el-form
          ref="passwordFormRef"
          :model="passwordForm"
          :rules="passwordRules"
          label-width="120px"
          style="max-width: 500px"
        >
          <el-form-item label="原密码" prop="old_password">
            <el-input
              v-model="passwordForm.old_password"
              type="password"
              placeholder="请输入原密码"
              show-password
            />
          </el-form-item>
          
          <el-form-item label="新密码" prop="new_password">
            <el-input
              v-model="passwordForm.new_password"
              type="password"
              placeholder="请输入新密码"
              show-password
            />
          </el-form-item>
          
          <el-form-item label="确认新密码" prop="new_password_confirm">
            <el-input
              v-model="passwordForm.new_password_confirm"
              type="password"
              placeholder="请再次输入新密码"
              show-password
            />
          </el-form-item>
          
          <el-form-item>
            <el-button type="primary" :loading="loading" @click="handleChangePassword">
              确认修改
            </el-button>
            <el-button @click="goBack">取消</el-button>
          </el-form-item>
        </el-form>
        
        <el-alert
          title="密码安全提示"
          type="info"
          :closable="false"
          style="margin-top: 20px; max-width: 500px"
        >
          <template #default>
            <ul style="margin: 0; padding-left: 20px">
              <li>密码长度至少6位</li>
              <li>建议使用字母、数字和特殊字符的组合</li>
              <li>修改密码后需要重新登录</li>
            </ul>
          </template>
        </el-alert>
      </el-card>
    </el-main>
  </el-container>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import { changePassword } from '@/api/auth'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()
const passwordFormRef = ref()
const loading = ref(false)

const passwordForm = reactive({
  old_password: '',
  new_password: '',
  new_password_confirm: ''
})

const validateNewPassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入新密码'))
  } else if (value !== passwordForm.new_password) {
    callback(new Error('两次输入的新密码不一致'))
  } else {
    callback()
  }
}

const passwordRules = {
  old_password: [
    { required: true, message: '请输入原密码', trigger: 'blur' }
  ],
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6位', trigger: 'blur' }
  ],
  new_password_confirm: [
    { required: true, validator: validateNewPassword, trigger: 'blur' }
  ]
}

const handleChangePassword = async () => {
  const valid = await passwordFormRef.value.validate().catch(() => false)
  if (!valid) return
  
  loading.value = true
  try {
    await changePassword({
      old_password: passwordForm.old_password,
      new_password: passwordForm.new_password,
      new_password_confirm: passwordForm.new_password_confirm
    })
    ElMessage.success('密码修改成功，请重新登录')
    // 退出登录
    userStore.logout()
    router.push('/login')
  } catch (error) {
    ElMessage.error(error.response?.data?.message || '密码修改失败')
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  router.push('/home')
}
</script>

<style scoped>
.password-container {
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

.password-card {
  max-width: 800px;
  margin: 0 auto;
}

.card-header {
  font-weight: bold;
}
</style>
