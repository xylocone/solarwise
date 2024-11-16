export interface APIResponse<T> {
  code: number
  msg: string
  payload: T
  raw_msg: string
}

export interface EnergyEstimation {
  months: {
    energy: number
    month: string
    order: number
  }[]
  total: number
}
