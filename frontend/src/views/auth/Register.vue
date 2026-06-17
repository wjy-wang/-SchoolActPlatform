<template>
  <div class="register-container">
    <el-card class="register-card">
      <template #header>
        <div class="card-header">
          <h2>校园活动发布平台</h2>
          <p>用户注册</p>
        </div>
      </template>
      
      <el-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="registerRules"
        label-position="top"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="registerForm.username"
            placeholder="请输入用户名"
            :prefix-icon="User"
            size="large"
          />
        </el-form-item>
        
        <el-form-item label="学号" prop="student_id">
          <el-input
            v-model="registerForm.student_id"
            placeholder="请输入学号"
            :prefix-icon="Document"
            size="large"
          />
        </el-form-item>
        
        <el-form-item label="邮箱" prop="email">
          <el-input
            v-model="registerForm.email"
            placeholder="请输入邮箱"
            :prefix-icon="Message"
            size="large"
          />
        </el-form-item>
        
        <el-form-item label="手机号" prop="phone">
          <el-input
            v-model="registerForm.phone"
            placeholder="请输入手机号"
            :prefix-icon="Phone"
            size="large"
          />
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="registerForm.password"
            type="password"
            placeholder="请输入密码"
            :prefix-icon="Lock"
            size="large"
            show-password
          />
        </el-form-item>
        
        <el-form-item label="确认密码" prop="password_confirm">
          <el-input
            v-model="registerForm.password_confirm"
            type="password"
            placeholder="请再次输入密码"
            :prefix-icon="Lock"
            size="large"
            show-password
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            :loading="loading"
            @click="handleRegister"
            style="width: 100%"
          >
            注册
          </el-button>
        </el-form-item>
        
        <div class="form-footer">
          <el-link type="primary" @click="goToLogin">已有账号？立即登录</el-link>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, Message, Phone, Document } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()
const registerFormRef = ref()
const loading = ref(false)

const registerForm = reactive({
  username: '',
  student_id: '',
  email: '',
  phone: '',
  password: '',
  password_confirm: ''
})

const validatePass2 = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== registerForm.password) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

const registerRules = {
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
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6位', trigger: 'blur' }
  ],
  password_confirm: [
    { required: true, validator: validatePass2, trigger: 'blur' }
  ]
}

const handleRegister = async () => {
  console.log('[DEBUG Register] handleRegister called')
  console.log('[DEBUG Register] form data:', JSON.stringify(registerForm))
  
  const valid = await registerFormRef.value.validate().catch(() => false)
  console.log('[DEBUG Register] form valid:', valid)
  if (!valid) return
  
  loading.value = true
  try {
    console.log('[DEBUG Register] calling userStore.register...')
    const result = await userStore.register(registerForm)
    console.log('[DEBUG Register] register result:', result)
    ElMessage.success('注册成功，请登录')
    router.push('/login')
  } catch (error) {
    console.error('[DEBUG Register] register error:', error)
    console.error('[DEBUG Register] error response:', error.response?.data)
    console.error('[DEBUG Register] error message:', error.message)
    
    // 显示更详细的错误信息
    const errors = error.response?.data
    if (errors && typeof errors === 'object') {
      let errorMsg = ''
      for (const field in errors) {
        if (Array.isArray(errors[field])) {
          errorMsg += `${field}: ${errors[field].join(', ')}\n`
        } else {
          errorMsg += `${field}: ${errors[field]}\n`
        }
      }
      ElMessage.error(errorMsg || '注册失败')
    } else {
      ElMessage.error(error.response?.data?.message || error.message || '注册失败')
    }
  } finally {
    loading.value = false
  }
}

const goToLogin = () => {
  router.push('/login')
}
</script>

<style scoped>
/* 🎨 注册容器 - 柔和渐变背景 */
.register-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #f0f4ff 0%, #faf0ff 50%, #f5f0ff 100%);
  padding: 20px;
}

/* 🎨 注册卡片 - 毛玻璃效果 */
.register-card {
  width: 480px;
  max-width: 100%;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
  overflow: hidden;
}

.register-card .el-card__header {
  background: linear-gradient(135deg, rgba(79, 70, 229, 0.05) 0%, rgba(124, 58, 237, 0.05) 100%);
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
  padding: 32px 24px;
}

.register-card .el-card__body {
  padding: 24px;
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

/* 🎨 注册按钮 - 渐变蓝紫色 */
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
