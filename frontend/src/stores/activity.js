import { defineStore } from 'pinia'
import { getActivityList, getActivityDetail } from '@/api/activity'

export const useActivityStore = defineStore('activity', {
  state: () => ({
    activities: [],
    currentActivity: null,
    loading: false,
    filters: {
      type: null,
      status: null
    }
  }),

  getters: {
    filteredActivities(state) {
      let result = state.activities
      if (state.filters.type !== null) {
        result = result.filter(a => a.type === state.filters.type)
      }
      if (state.filters.status !== null) {
        result = result.filter(a => a.status === state.filters.status)
      }
      return result
    }
  },

  actions: {
    async fetchActivities(params = {}) {
      this.loading = true
      try {
        const response = await getActivityList(params)
        this.activities = response.data.activities || []
        return response.data
      } finally {
        this.loading = false
      }
    },

    async fetchActivityDetail(id) {
      this.loading = true
      try {
        const response = await getActivityDetail(id)
        this.currentActivity = response.data.activity
        return response.data
      } finally {
        this.loading = false
      }
    },

    setFilters(filters) {
      this.filters = { ...this.filters, ...filters }
    },

    clearFilters() {
      this.filters = {
        type: null,
        status: null
      }
    }
  }
})
