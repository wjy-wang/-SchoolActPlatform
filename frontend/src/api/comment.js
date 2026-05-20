import request from '@/utils/request'

/**
 * 获取活动评论列表
 * @param {number} activityId - 活动ID
 * @param {object} params - 查询参数 { page, page_size }
 * @returns {Promise}
 */
export const getActivityComments = (activityId, params = {}) => {
  return request({
    url: `/activities/${activityId}/comments/`,
    method: 'get',
    params
  })
}

/**
 * 发布评论
 * @param {number} activityId - 活动ID
 * @param {object} data - 评论数据 { content }
 * @returns {Promise}
 */
export const createComment = (activityId, data) => {
  return request({
    url: `/activities/${activityId}/comments/`,
    method: 'post',
    data
  })
}

/**
 * 删除评论
 * @param {number} commentId - 评论ID
 * @returns {Promise}
 */
export const deleteComment = (commentId) => {
  return request({
    url: `/comments/${commentId}/`,
    method: 'delete'
  })
}
