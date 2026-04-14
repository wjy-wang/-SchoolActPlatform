<template>
  <el-container class="home-container">
    <el-header class="header">
      <div class="header-left">
        <h1>校园活动发布平台</h1>
      </div>
      <div class="header-right">
        <el-dropdown @command="handleCommand">
          <span class="user-info">
            {{ userStore.userInfo?.username }}
            <el-icon class="el-icon--right"><arrow-down /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile">个人信息</el-dropdown-item>
              <el-dropdown-item command="password">修改密码</el-dropdown-item>
              <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </el-header>
    
    <el-main class="main-content">
      <div class="welcome-section">
        <h2>欢迎使用校园活动发布平台</h2>
        <p>这是一个基于 Django + Vue.js 的校园活动管理系统</p>
        
        <el-row :gutter="20" class="feature-cards">
          <el-col :span="8">
            <el-card>
              <template #header>
                <div class="card-header">
                  <el-icon><Calendar /></el-icon>
                  <span>活动管理</span>
                </div>
              </template>
              <div>发布、编辑和管理校园活动</div>
            </el-card>
          </el-col>
          
          <el-col :span="8">
            <el-card>
              <template #header>
                <div class="card-header">
                  <el-icon><UserFilled /></el-icon>
                  <span>活动报名</span>
                </div>
              </template>
              <div>在线报名参加活动</div>
            </el-card>
          </el-col>
          
          <el-col :span="8">
            <el-card>
              <template #header>
                <div class="card-header">
                  <el-icon><Star /></el-icon>
                  <span>活动收藏</span>
                </div>
              </template>
              <div>收藏感兴趣的活动</div>
            </el-card>
          </el-col>
        </el-row>
        
        <div class="user-info-section" v-if="userStore.userInfo">
          <h3>当前登录用户信息</h3>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="用户名">{{ userStore.userInfo.username }}</el-descriptions-item>
            <el-descriptions-item label="学号">{{ userStore.userInfo.student_id }}</el-descriptions-item>
            <el-descriptions-item label="邮箱">{{ userStore.userInfo.email }}</el-descriptions-item>
            <el-descriptions-item label="手机号">{{ userStore.userInfo.phone }}</el-descriptions-item>
            <el-descriptions-item label="角色">
              <el-tag :type="userStore.userInfo.role === 1 ? 'danger' : 'success'">
                {{ userStore.userInfo.role === 1 ? '管理员' : '普通用户' }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="注册时间">{{ formatDate(userStore.userInfo.date_joined) }}</el-descriptions-item>
          </el-descriptions>
        </div>
      </div>
    </el-main>
  </el-container>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowDown, Calendar, UserFilled, Star } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

onMounted(() => {
  // 刷新用户信息
  userStore.fetchUserInfo().catch(() => {})
})

const handleCommand = (command) => {
  switch (command) {
    case 'profile':
      router.push('/profile')
      break
    case 'password':
      router.push('/password')
      break
    case 'logout':
      handleLogout()
      break
  }
}

const handleLogout = () => {
  ElMessageBox.confirm('确定要退出登录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    userStore.logout()
    ElMessage.success('已退出登录')
    router.push('/login')
  }).catch(() => {})
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN')
}
</script>

<style scoped>
.home-container {
  min-height: 100vh;
}

.header {
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left h1 {
  margin: 0;
  font-size: 20px;
  color: #303133;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  cursor: pointer;
  color: #606266;
  display: flex;
  align-items: center;
}

.main-content {
  background-color: #f5f7fa;
  padding: 20px;
}

.welcome-section {
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-section h2 {
  text-align: center;
  margin-bottom: 10px;
  color: #303133;
}

.welcome-section > p {
  text-align: center;
  color: #909399;
  margin-bottom: 30px;
}

.feature-cards {
  margin-bottom: 40px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: bold;
}

.user-info-section {
  background: #fff;
  padding: 20px;
  border-radius: 4px;
}

.user-info-section h3 {
  margin-bottom: 20px;
  color: #303133;
}
</style>
