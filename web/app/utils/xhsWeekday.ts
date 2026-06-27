/** 星期维度（与后端 WEEKDAYS 一致） */
export type Weekday = 'mon' | 'tue' | 'wed' | 'thu' | 'fri' | 'sat' | 'sun'

export const WEEKDAY_ORDER: Weekday[] = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

export const WEEKDAY_LABELS: Record<Weekday, string> = {
  mon: '周一',
  tue: '周二',
  wed: '周三',
  thu: '周四',
  fri: '周五',
  sat: '周六',
  sun: '周日'
}

export const weekdayLabel = (w: string) =>
  WEEKDAY_LABELS[w as Weekday] || w

/** 浏览器本地时区下的今天对应 weekday */
export const getTodayWeekday = (): Weekday => {
  const map: Weekday[] = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
  return map[new Date().getDay()]
}

export const WEEKDAY_OPTIONS = WEEKDAY_ORDER.map((value) => ({
  value,
  label: WEEKDAY_LABELS[value]
}))
