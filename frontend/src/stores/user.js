import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as loginApi, getProfile, register as registerApi } from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  // State
  const token = ref(localStorage.getItem('token') || '')
  const refreshToken = ref(localStorage.getItem('refreshToken') || '')
  const userInfo = ref(JSON.parse(localStorage.getItem('userInfo') || '{}'))

  // Getters
  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => userInfo.value?.role === 1)

  // Actions
  const setToken = (accessToken, refresh) => {
    token.value = accessToken
    refreshToken.value = refresh
    localStorage.setItem('token', accessToken)
    localStorage.setItem('refreshToken', refresh)
  }

  const setUserInfo = (info) => {
    userInfo.value = info
    localStorage.setItem('userInfo', JSON.stringify(info))
  }

  const login = async (credentials) => {
    const res = await loginApi(credentials)
    if (res.access) {
      setToken(res.access, res.refresh)
      setUserInfo(res.user)
      return res
    }
    throw new Error(res.message || '登录失败')
  }

  const register = async (data) => {
    const res = await registerApi(data)
    return res
  }

  const fetchUserInfo = async () => {
    const res = await getProfile()
    if (res.user) {
      setUserInfo(res.user)
      return res.user
    }
    throw new Error(res.message || '获取用户信息失败')
  }

  const logout = () => {
    token.value = ''
    refreshToken.value = ''
    userInfo.value = {}
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
    localStorage.removeItem('userInfo')
  }

  const updateUserInfo = (info) => {
    userInfo.value = { ...userInfo.value, ...info }
    localStorage.setItem('userInfo', JSON.stringify(userInfo.value))
  }

  return {
    token,
    refreshToken,
    userInfo,
    isLoggedIn,
    isAdmin,
    login,
    register,
    logout,
    fetchUserInfo,
    setToken,
    setUserInfo,
    updateUserInfo
  }
})
