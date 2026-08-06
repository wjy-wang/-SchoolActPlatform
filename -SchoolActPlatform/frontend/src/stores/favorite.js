import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import {
  getMyFavorites,
  favoriteActivity,
  cancelFavorite
} from '@/api/activity'

export const useFavoriteStore = defineStore('favorite', () => {
  // State
  const favorites = ref([])
  const loading = ref(false)
  const favoriteMap = ref(new Map()) // 用于快速查询某活动是否已收藏

  // Getters
  const favoriteCount = computed(() => favorites.value.length)
  
  const isFavorited = computed(() => (activityId) => {
    return favoriteMap.value.has(Number(activityId))
  })

  const getFavoriteByActivityId = computed(() => (activityId) => {
    return favoriteMap.value.get(Number(activityId)) || null
  })

  // 获取收藏ID（用于取消收藏）
  const getFavoriteId = computed(() => (activityId) => {
    const favorite = favoriteMap.value.get(Number(activityId))
    return favorite ? favorite.id : null
  })

  // Actions
  const buildFavoriteMap = () => {
    favoriteMap.value.clear()
    favorites.value.forEach(favorite => {
      favoriteMap.value.set(Number(favorite.activity), favorite)
    })
  }

  const fetchFavorites = async () => {
    loading.value = true
    try {
      const response = await getMyFavorites()
      favorites.value = response.favorites || []
      buildFavoriteMap()
      return response
    } catch (error) {
      console.error('获取收藏列表失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const addFavorite = async (activityId) => {
    try {
      const response = await favoriteActivity({ activity: activityId })
      // 添加到本地列表
      if (response.favorite) {
        favorites.value.unshift(response.favorite)
        favoriteMap.value.set(Number(activityId), response.favorite)
      }
      return response
    } catch (error) {
      console.error('收藏失败:', error)
      throw error
    }
  }

  const removeFavorite = async (favoriteId, activityId) => {
    try {
      await cancelFavorite(favoriteId)
      // 从本地列表移除
      favorites.value = favorites.value.filter(f => f.id !== favoriteId)
      if (activityId) {
        favoriteMap.value.delete(Number(activityId))
      } else {
        // 如果没有提供activityId，重新构建map
        buildFavoriteMap()
      }
    } catch (error) {
      console.error('取消收藏失败:', error)
      throw error
    }
  }

  // 从活动详情页直接取消收藏
  const removeByActivityId = async (activityId) => {
    const favorite = favoriteMap.value.get(Number(activityId))
    if (favorite) {
      await removeFavorite(favorite.id, activityId)
    }
  }

  const clearFavorites = () => {
    favorites.value = []
    favoriteMap.value.clear()
  }

  return {
    // State
    favorites,
    loading,
    // Getters
    favoriteCount,
    isFavorited,
    getFavoriteByActivityId,
    getFavoriteId,
    // Actions
    fetchFavorites,
    addFavorite,
    removeFavorite,
    removeByActivityId,
    clearFavorites
  }
})
