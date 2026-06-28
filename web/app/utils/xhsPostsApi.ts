import { api } from '~/utils/api'
import { type Weekday, WEEKDAY_ORDER } from '~/utils/xhsWeekday'

const weekdayFromDate = (dateStr: string): Weekday => {
  const map: Weekday[] = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
  const d = new Date(`${dateStr}T12:00:00`)
  return map[d.getDay()]
}

const postKey = (item: { student?: string; period?: string }) =>
  `${item.student || 'a'}:${item.period}`

/** 按星期拉取发布内容（新接口优先，旧 date 接口自动兼容） */
export async function fetchXhsPostsByWeekday(weekday: Weekday): Promise<any[]> {
  try {
    const res = await api.get<any>(`/xhs-posts?weekday=${weekday}`)
    if (res.code === 200 && Array.isArray(res.data)) return res.data
  } catch (e: any) {
    if (!isLegacyApiError(e)) throw e
  }

  const merged = new Map<string, any>()
  const now = new Date()
  for (let monthOffset = -18; monthOffset <= 1; monthOffset++) {
    const anchor = new Date(now.getFullYear(), now.getMonth() + monthOffset, 1)
    const month = `${anchor.getFullYear()}-${String(anchor.getMonth() + 1).padStart(2, '0')}`
    try {
      const monthRes = await api.get<any>(`/xhs-posts/month?month=${month}`)
      const dates: string[] = monthRes.data?.dates || []
      for (const dateStr of dates) {
        if (weekdayFromDate(dateStr) !== weekday) continue
        const dayRes = await api.get<any>(`/xhs-posts?date=${dateStr}`)
        const list = Array.isArray(dayRes.data) ? dayRes.data : []
        for (const item of list) {
          merged.set(postKey(item), item)
        }
      }
    } catch {
      // 忽略单个月份查询失败
    }
  }
  return Array.from(merged.values())
}

/** 拉取已有内容的星期（用于红点） */
export async function fetchXhsMarkedWeekdays(): Promise<Set<Weekday>> {
  try {
    const res = await api.get<any>('/xhs-posts/weekdays')
    const list: string[] = res.data?.weekdays || []
    if (list.length) {
      return new Set(
        list.filter((w): w is Weekday => WEEKDAY_ORDER.includes(w as Weekday))
      )
    }
  } catch (e: any) {
    if (!isLegacyApiError(e)) throw e
  }

  const weekdays = new Set<Weekday>()
  const now = new Date()
  for (let monthOffset = -18; monthOffset <= 1; monthOffset++) {
    const anchor = new Date(now.getFullYear(), now.getMonth() + monthOffset, 1)
    const month = `${anchor.getFullYear()}-${String(anchor.getMonth() + 1).padStart(2, '0')}`
    try {
      const monthRes = await api.get<any>(`/xhs-posts/month?month=${month}`)
      const dates: string[] = monthRes.data?.dates || []
      for (const dateStr of dates) {
        weekdays.add(weekdayFromDate(dateStr))
      }
    } catch {
      // 忽略单个月份查询失败
    }
  }
  return weekdays
}

/** 保存发布内容（新 weekday 接口优先，旧 date 接口自动兼容） */
export async function saveXhsPost(
  body: {
    weekday: Weekday
    student: string
    period: string
    poster_text: string
    title: string
    images: string[]
    content: string
    products: string[]
  },
  submitPassword?: string
) {
  const payload = {
    ...body,
    ...(submitPassword !== undefined ? { submit_password: submitPassword } : {})
  }
  try {
    const res = await api.post<any>('/xhs-posts', payload)
    if (res.code === 200) return res
  } catch (e: any) {
    if (!isLegacyApiError(e)) throw e
  }

  const { weekday, ...rest } = payload
  return api.post<any>('/xhs-posts', {
    ...rest,
    date: nextDateForWeekday(weekday)
  })
}

/** 修改小红书提交密码（仅管理员） */
export async function changeXhsSubmitPassword(newPassword: string) {
  return api.put<any>('/xhs-posts/submit-password', {
    new_password: newPassword
  })
}

/** 判断该星期是否还有内容（删除后刷新红点） */
export async function hasXhsPostsForWeekday(weekday: Weekday): Promise<boolean> {
  const list = await fetchXhsPostsByWeekday(weekday)
  return list.length > 0
}

function nextDateForWeekday(weekday: Weekday): string {
  const now = new Date()
  for (let i = 0; i < 7; i++) {
    const d = new Date(now.getFullYear(), now.getMonth(), now.getDate() + i)
    const dateStr = formatDate(d)
    if (weekdayFromDate(dateStr) === weekday) return dateStr
  }
  return formatDate(now)
}

function formatDate(d: Date): string {
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}-${m}-${day}`
}

function isLegacyApiError(e: any): boolean {
  const status = e?.status ?? e?.response?.status
  return status === 400 || status === 404
}
