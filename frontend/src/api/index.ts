import axios, { AxiosError } from 'axios'
import type { AxiosResponse } from 'axios'
import type { ApiResponse, ApiError } from '@/types'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('shushan_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error),
)

// eslint-disable-next-line @typescript-eslint/no-explicit-any
apiClient.interceptors.response.use(
  (response: AxiosResponse<any, any>) => {
    // API 直接返回数据，不需要包裹在 data 中
    return response.data
  },
  (error: AxiosError<ApiError>) => {
    const message = error.response?.data?.message || '网络请求失败'
    return Promise.reject({ success: false, message, code: error.response?.status || 0 })
  },
)

export default apiClient
