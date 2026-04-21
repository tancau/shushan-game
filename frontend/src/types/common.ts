export interface ApiResponse<T = unknown> {
  success: boolean
  data?: T
  message?: string
  code?: number
}

export interface ApiError {
  success: false
  message: string
  code: number
}

export interface PaginationParams {
  page: number
  pageSize: number
}

export interface PaginationResult<T> {
  list: T[]
  total: number
  page: number
  pageSize: number
}
