<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="card-header">
          <h2>校园活动发布平台</h2>
          <p>用户登录</p>
        </div>
      </template>
      
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        label-position="top"
        @keyup.enter="handleLogin"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名/学号/邮箱"
            :prefix-icon="User"
            size="large"
          />
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            :prefix-icon="Lock"
            size="large"
            show-password
          />
        </el-form-item>
        
        <el-form-item>
          <el-checkbox v-model="loginForm.remember_me">记住密码</el-checkbox>
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            :loading="loading"
            @click="handleLogin"
            style="width: 100%"
          >
            登录
          </el-button>
        </el-form-item>
        
        <div class="form-footer">
          <el-link type="primary" @click="goToRegister">还没有账号？立即注册</el-link>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()
const loginFormRef = ref()
const loading = ref(false)

const loginForm = reactive({
  username: '',
  password: '',
  remember_me: false
})

const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6位', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  console.log('[DEBUG Login] handleLogin called')
  console.log('[DEBUG Login] username:', loginForm.username)
  console.log('[DEBUG Login] password:', loginForm.password)
  
  const valid = await loginFormRef.value.validate().catch(() => false)
  console.log('[DEBUG Login] form valid:', valid)
  if (!valid) return
  
  loading.value = true
  try {
    console.log('[DEBUG Login] calling userStore.login...')
    const result = await userStore.login({
      username: loginForm.username,
      password: loginForm.password,
      remember_me: loginForm.remember_me
    })
    console.log('[DEBUG Login] login result:', result)
    console.log('[DEBUG Login] token:', userStore.token?.slice(0, 20) + '...')
    console.log('[DEBUG Login] userInfo:', userStore.userInfo)
    console.log('[DEBUG Login] isLoggedIn:', userStore.isLoggedIn)
    
    ElMessage.success('登录成功')
    router.push('/home').then(() => {
      console.log('[DEBUG Login] router push successful')
    }).catch(err => {
      console.error('[DEBUG Login] router push error:', err)
    })
  } catch (error) {
    console.error('[DEBUG Login] login error:', error)
    console.error('[DEBUG Login] error response:', error.response?.data)
    ElMessage.error(error.response?.data?.message || '登录失败')
  } finally {
    loading.value = false
  }
}

const goToRegister = () => {
  router.push('/register')
}
</script>

<style scoped>
/* 🎨 登录容器 - 柔和渐变背景 */
.login-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #f0f4ff 0%, #faf0ff 50%, #f5f0ff 100%);
  padding: 20px;
}

/* 🎨 登录卡片 - 毛玻璃效果 */
.login-card {
  width: 420px;
  max-width: 100%;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
  overflow: hidden;
}

.login-card .el-card__header {
  background: linear-gradient(135deg, rgba(79, 70, 229, 0.05) 0%, rgba(124, 58, 237, 0.05) 100%);
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
  padding: 32px 24px;
}

.login-card .el-card__body {
  padding: 32px 24px;
}

/* 🎨 卡片头部 */
.card-header {
  text-align: center;
}

.card-header h2 {
  margin: 0 0 12px 0;
  color: #4F46E5;
  font-size: 28px;
  font-weight: 600;
  line-height: 1.5;
}

.card-header p {
  margin: 0;
  color: #6b7280;
  font-size: 16px;
  line-height: 1.6;
}

/* 🎨 表单样式 */
.el-form-item__label {
  color: #4a5568;
  font-weight: 500;
}

.el-input__wrapper {
  background: rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  transition: all 0.3s ease;
}

.el-input__wrapper:hover {
  background: rgba(255, 255, 255, 0.7);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.el-input__wrapper.is-focus {
  background: rgba(255, 255, 255, 0.8);
  border-color: rgba(79, 70, 229, 0.3);
  box-shadow: 0 4px 16px rgba(79, 70, 229, 0.15);
}

/* 🎨 登录按钮 - 渐变蓝紫色 */
.el-button--primary {
  background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
  border: none;
  border-radius: 12px;
  height: 48px;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 0.5px;
  box-shadow: 0 4px 16px rgba(79, 70, 229, 0.3);
  transition: all 0.3s ease;
}

.el-button--primary:hover {
  background: linear-gradient(135deg, #5B21B6 0%, #8B5CF6 100%);
  box-shadow: 0 6px 24px rgba(79, 70, 229, 0.4);
  transform: translateY(-2px);
}

.el-button--primary.is-loading {
  background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
}

/* 🎨 记住密码复选框 */
.el-checkbox__label {
  color: #6b7280;
  font-size: 14px;
}

.el-checkbox__inner {
  border-radius: 4px;
  border-color: #d1d5db;
}

.el-checkbox__input.is-checked .el-checkbox__inner {
  background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
  border-color: #4F46E5;
}

/* 🎨 底部链接 */
.form-footer {
  text-align: center;
  margin-top: 24px;
}

.el-link--primary {
  color: #4F46E5;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.el-link--primary:hover {
  color: #7C3AED;
}
</style>
