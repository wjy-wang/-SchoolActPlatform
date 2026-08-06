import request from '@/utils/request'

export function getActivityList(params) {
  return request({
    url: '/activities/',
    method: 'get',
    params
  })
}

export function getActivityDetail(id) {
  return request({
    url: `/activities/${id}/`,
    method: 'get'
  })
}

export function createActivity(data) {
  return request({
    url: '/activities/create/',
    method: 'post',
    data
  })
}

export function updateActivity(id, data) {
  return request({
    url: `/activities/${id}/update/`,
    method: 'put',
    data
  })
}

export function deleteActivity(id) {
  return request({
    url: `/activities/${id}/delete/`,
    method: 'delete'
  })
}

export function getMyActivities() {
  return request({
    url: '/activities/my/',
    method: 'get'
  })
}

export function enrollActivity(data) {
  return request({
    url: '/enrollments/create/',
    method: 'post',
    data
  })
}

export function cancelEnrollment(id) {
  return request({
    url: `/enrollments/${id}/`,
    method: 'delete'
  })
}

export function getMyEnrollments() {
  return request({
    url: '/enrollments/',
    method: 'get'
  })
}

export function favoriteActivity(data) {
  return request({
    url: '/favorites/create/',
    method: 'post',
    data
  })
}

export function cancelFavorite(id) {
  return request({
    url: `/favorites/${id}/`,
    method: 'delete'
  })
}

export function getMyFavorites() {
  return request({
    url: '/favorites/',
    method: 'get'
  })
}

export function getActivityComments(activityId) {
  return request({
    url: `/activities/${activityId}/comments/`,
    method: 'get'
  })
}

export function createComment(data) {
  return request({
    url: '/comments/create/',
    method: 'post',
    data
  })
}

export function deleteComment(id) {
  return request({
    url: `/comments/${id}/`,
    method: 'delete'
  })
}

export function getActivityEnrollments(activityId) {
  return request({
    url: `/activities/${activityId}/enrollments/`,
    method: 'get'
  })
}

export function getAllEnrollments() {
  return request({
    url: '/enrollments/all/',
    method: 'get'
  })
}

export function getAllFavorites() {
  return request({
    url: '/favorites/all/',
    method: 'get'
  })
}
