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
            <el-card class="clickable-card" @click="goToActivities">
              <template #header>
                <div class="card-header">
                  <el-icon><Calendar /></el-icon>
                  <span>浏览活动</span>
                </div>
              </template>
              <div>查看所有校园活动</div>
            </el-card>
          </el-col>

          <el-col :span="8">
            <el-card class="clickable-card" :class="{ 'admin-card': userStore.userInfo?.role === 1 }" @click="handleEnrollmentsClick">
              <template #header>
                <div class="card-header">
                  <el-icon><UserFilled /></el-icon>
                  <span>{{ userStore.userInfo?.role === 1 ? '报名名单' : '我的报名' }}</span>
                </div>
              </template>
              <div>{{ userStore.userInfo?.role === 1 ? '查看所有用户的报名情况' : '查看已报名的活动' }}</div>
            </el-card>
          </el-col>

          <el-col :span="8">
            <el-card class="clickable-card" :class="{ 'admin-card': userStore.userInfo?.role === 1 }" @click="handleFavoritesClick">
              <template #header>
                <div class="card-header">
                  <el-icon><Star /></el-icon>
                  <span>{{ userStore.userInfo?.role === 1 ? '收藏名单' : '我的收藏' }}</span>
                </div>
              </template>
              <div>{{ userStore.userInfo?.role === 1 ? '查看所有用户的收藏情况' : '查看已收藏的活动' }}</div>
            </el-card>
          </el-col>
        </el-row>

        <el-row :gutter="20" class="feature-cards" v-if="userStore.userInfo?.role === 1">
          <el-col :span="12">
            <el-card class="clickable-card admin-card" @click="goToCreateActivity">
              <template #header>
                <div class="card-header">
                  <el-icon><Plus /></el-icon>
                  <span>发布活动</span>
                </div>
              </template>
              <div>创建新的校园活动</div>
            </el-card>
          </el-col>

          <el-col :span="12">
            <el-card class="clickable-card admin-card" @click="goToMyActivities">
              <template #header>
                <div class="card-header">
                  <el-icon><Management /></el-icon>
                  <span>管理活动</span>
                </div>
              </template>
              <div>编辑或删除已创建的活动</div>
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
import { ArrowDown, Calendar, UserFilled, Star, Plus, Management } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

onMounted(() => {
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

const goToActivities = () => {
  router.push('/activities')
}

const handleEnrollmentsClick = () => {
  console.log('[DEBUG] handleEnrollmentsClick clicked')
  console.log('[DEBUG] userStore.isLoggedIn:', userStore.isLoggedIn)
  console.log('[DEBUG] userStore.token:', userStore.token?.slice(0, 20) + '...')
  console.log('[DEBUG] userStore.userInfo:', userStore.userInfo)
  console.log('[DEBUG] user role:', userStore.userInfo?.role)
  
  const targetRoute = userStore.userInfo?.role === 1 ? '/enrollment-list' : '/my-enrollments'
  console.log('[DEBUG] targetRoute:', targetRoute)
  
  try {
    router.push(targetRoute).then(() => {
      console.log('[DEBUG] Router push successful')
    }).catch(err => {
      console.error('[DEBUG] Router push error:', err)
    })
  } catch (err) {
    console.error('[DEBUG] Exception:', err)
  }
}

const handleFavoritesClick = () => {
  console.log('[DEBUG] handleFavoritesClick clicked')
  console.log('[DEBUG] userStore.isLoggedIn:', userStore.isLoggedIn)
  console.log('[DEBUG] userStore.token:', userStore.token?.slice(0, 20) + '...')
  console.log('[DEBUG] userStore.userInfo:', userStore.userInfo)
  console.log('[DEBUG] user role:', userStore.userInfo?.role)
  
  const targetRoute = userStore.userInfo?.role === 1 ? '/favorite-list' : '/my-favorites'
  console.log('[DEBUG] targetRoute:', targetRoute)
  
  try {
    router.push(targetRoute).then(() => {
      console.log('[DEBUG] Router push successful')
    }).catch(err => {
      console.error('[DEBUG] Router push error:', err)
    })
  } catch (err) {
    console.error('[DEBUG] Exception:', err)
  }
}

const goToCreateActivity = () => {
  router.push('/activities/form')
}

const goToMyActivities = () => {
  router.push('/my-activities')
}

const goToEnrollmentList = () => {
  router.push('/enrollment-list')
}

const goToFavoriteList = () => {
  router.push('/favorite-list')
}
</script>

<style scoped>
/* 🎨 整体布局 - 渐变背景 */
.home-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f0f4ff 0%, #faf0ff 50%, #f5f0ff 100%);
}

/* 🎨 Header - 毛玻璃效果 */
.header {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
}

.header-left h1 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #4F46E5;
  letter-spacing: 0.5px;
}

.header-right {
  display: flex;
  align-items: center;
}

/* 🎨 用户信息 - 圆形头像 */
.user-info {
  cursor: pointer;
  color: #4F46E5;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 12px;
  background: rgba(79, 70, 229, 0.1);
  transition: all 0.3s ease;
}

.user-info:hover {
  background: rgba(79, 70, 229, 0.2);
  transform: translateY(-2px);
}

/* 🎨 主内容区 - 最大宽度1400px */
.main-content {
  background: transparent;
  padding: 40px 20px;
}

.welcome-section {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
}

.welcome-section h2 {
  text-align: center;
  margin-bottom: 16px;
  color: #1a1a2e;
  font-size: 32px;
  font-weight: 600;
  line-height: 1.5;
}

.welcome-section > p {
  text-align: center;
  color: #6b7280;
  margin-bottom: 48px;
  font-size: 16px;
  line-height: 1.6;
}

/* 🎨 功能卡片 - Grid布局 + 毛玻璃 */
.feature-cards {
  margin-bottom: 48px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 600;
  font-size: 16px;
}

.card-header .el-icon {
  font-size: 20px;
  color: #4F46E5;
}

/* 🎨 卡片样式 - 毛玻璃 + 圆角 */
.clickable-card {
  cursor: pointer;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.clickable-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(79, 70, 229, 0.15);
  background: rgba(255, 255, 255, 0.85);
}

.clickable-card .el-card__header {
  background: linear-gradient(135deg, rgba(79, 70, 229, 0.05) 0%, rgba(124, 58, 237, 0.05) 100%);
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
}

.clickable-card .el-card__body {
  color: #6b7280;
  font-size: 14px;
}

/* 🎨 管理员卡片 - 渐变背景 */
.admin-card {
  background: linear-gradient(135deg, rgba(79, 70, 229, 0.08) 0%, rgba(124, 58, 237, 0.08) 100%);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.admin-card:hover {
  background: linear-gradient(135deg, rgba(79, 70, 229, 0.12) 0%, rgba(124, 58, 237, 0.12) 100%);
}

/* 🎨 用户信息区 - 毛玻璃卡片 */
.user-info-section {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  padding: 32px;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.user-info-section h3 {
  margin-bottom: 24px;
  color: #1a1a2e;
  font-size: 20px;
  font-weight: 600;
}

/* 🎨 Element Plus组件样式覆盖 */
.el-descriptions {
  background: transparent;
}

.el-descriptions__label {
  color: #6b7280;
  font-weight: 500;
}

.el-descriptions__content {
  color: #1a1a2e;
}

.el-tag--success {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 4px 12px;
}

.el-tag--danger {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 4px 12px;
}

/* 🎨 下拉菜单样式 */
.el-dropdown-menu {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
}

.el-dropdown-menu__item {
  color: #4a5568;
  padding: 12px 20px;
  transition: all 0.2s ease;
}

.el-dropdown-menu__item:hover {
  background: rgba(79, 70, 229, 0.1);
  color: #4F46E5;
}
</style>
