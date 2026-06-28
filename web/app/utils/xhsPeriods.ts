export type Period = 'morning' | 'noon' | 'evening' | 'night'

export const PERIOD_OPTIONS: {
  value: Period
  label: string
  time: string
}[] = [
  { value: 'morning', label: '早上', time: '7:30-8:30' },
  { value: 'noon', label: '中午', time: '11:30-12:30' },
  { value: 'evening', label: '傍晚', time: '18:30-19:30' },
  { value: 'night', label: '晚上', time: '21:00-22:00' }
]

export const periodLabel = (p: string) =>
  PERIOD_OPTIONS.find((x) => x.value === p)?.label || p

export const periodTime = (p: string) =>
  PERIOD_OPTIONS.find((x) => x.value === p)?.time || ''
