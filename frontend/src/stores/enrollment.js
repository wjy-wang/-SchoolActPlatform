import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import {
  getMyEnrollments,
  enrollActivity,
  cancelEnrollment
} from '@/api/activity'

export const useEnrollmentStore = defineStore('enrollment', () => {
  // State
  const enrollments = ref([])
  const loading = ref(false)
  const enrollmentMap = ref(new Map()) // 用于快速查询某活动是否已报名

  // Getters
  const enrollmentCount = computed(() => enrollments.value.length)
  
  const isEnrolled = computed(() => (activityId) => {
    return enrollmentMap.value.has(Number(activityId))
  })

  const getEnrollmentByActivityId = computed(() => (activityId) => {
    return enrollmentMap.value.get(Number(activityId)) || null
  })

  // 待确认的报名数量
  const pendingCount = computed(() => {
    return enrollments.value.filter(e => e.status === 0).length
  })

  // 已确认的报名数量
  const confirmedCount = computed(() => {
    return enrollments.value.filter(e => e.status === 1).length
  })

  // Actions
  const buildEnrollmentMap = () => {
    enrollmentMap.value.clear()
    enrollments.value.forEach(enrollment => {
      enrollmentMap.value.set(Number(enrollment.activity), enrollment)
    })
  }

  const fetchEnrollments = async () => {
    loading.value = true
    try {
      const response = await getMyEnrollments()
      enrollments.value = response.enrollments || []
      buildEnrollmentMap()
      return response
    } catch (error) {
      console.error('获取报名列表失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const enroll = async (activityId) => {
    try {
      const response = await enrollActivity({ activity: activityId })
      // 添加到本地列表
      if (response.enrollment) {
        enrollments.value.unshift(response.enrollment)
        enrollmentMap.value.set(Number(activityId), response.enrollment)
      }
      return response
    } catch (error) {
      console.error('报名失败:', error)
      throw error
    }
  }

  const cancel = async (enrollmentId, activityId) => {
    try {
      await cancelEnrollment(enrollmentId)
      // 从本地列表移除
      enrollments.value = enrollments.value.filter(e => e.id !== enrollmentId)
      if (activityId) {
        enrollmentMap.value.delete(Number(activityId))
      } else {
        // 如果没有提供activityId，重新构建map
        buildEnrollmentMap()
      }
    } catch (error) {
      console.error('取消报名失败:', error)
      throw error
    }
  }

  // 从活动详情页直接取消报名
  const cancelByActivityId = async (activityId) => {
    const enrollment = enrollmentMap.value.get(Number(activityId))
    if (enrollment) {
      await cancel(enrollment.id, activityId)
    }
  }

  const clearEnrollments = () => {
    enrollments.value = []
    enrollmentMap.value.clear()
  }

  return {
    // State
    enrollments,
    loading,
    // Getters
    enrollmentCount,
    isEnrolled,
    getEnrollmentByActivityId,
    pendingCount,
    confirmedCount,
    // Actions
    fetchEnrollments,
    enroll,
    cancel,
    cancelByActivityId,
    clearEnrollments
  }
})
