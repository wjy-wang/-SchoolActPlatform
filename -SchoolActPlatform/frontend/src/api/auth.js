import request from '@/utils/request'

// 用户注册
export const register = (data) => {
  return request({
    url: '/auth/register/',
    method: 'post',
    data
  })
}

// 用户登录
export const login = (data) => {
  return request({
    url: '/auth/login/',
    method: 'post',
    data
  })
}

// 用户登出
export const logout = (data) => {
  return request({
    url: '/auth/logout/',
    method: 'post',
    data
  })
}

// 刷新token
export const refreshToken = (data) => {
  return request({
    url: '/auth/refresh/',
    method: 'post',
    data
  })
}

// 获取用户信息
export const getProfile = () => {
  return request({
    url: '/auth/profile/',
    method: 'get'
  })
}

// 更新用户信息
export const updateProfile = (data) => {
  return request({
    url: '/auth/profile/',
    method: 'put',
    data
  })
}

// 修改密码
export const changePassword = (data) => {
  return request({
    url: '/auth/password/',
    method: 'put',
    data
  })
}
