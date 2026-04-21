/**
 * API 响应的基础类型定义
 */

/**
 * 通用 API 响应格式
 * 注意：API 直接在根对象返回数据，而不是包裹在 data 字段中
 */
export interface ApiResponse<T = unknown> {
  success: boolean
  message?: string
  code?: number
  // API 有时直接在根对象返回数据，有时通过泛型 T 提供额外字段
}

/**
 * 玩家状态 API 响应
 * 准确反映后端返回的数据格式（snake_case）
 */
export interface PlayerStatusApiResponse {
  success: boolean
  name: string
  realm: string
  cultivation: string  // API 返回字符串
  hp: string          // 格式: "100/100"
  mp: string          // 格式: "95/100"
  location: string
  sect: string | null
  spirit_stones: string  // snake_case
  equipped_artifact: string | null  // snake_case
}

/**
 * 修炼 API 响应
 */
export interface CultivateApiResponse {
  success: boolean
  cultivation: string
  message: string
}

/**
 * 突破 API 响应
 */
export interface AdvanceApiResponse {
  success: boolean
  message: string
  new_realm?: string
}

/**
 * API 错误响应
 */
export interface ApiError {
  success: false
  message: string
  code: number
}

/**
 * 分页参数
 */
export interface PaginationParams {
  page: number
  pageSize: number
}

/**
 * 分页结果
 */
export interface PaginationResult<T> {
  list: T[]
  total: number
  page: number
  pageSize: number
}
