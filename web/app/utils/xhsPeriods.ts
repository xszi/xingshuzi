export type Period = 'morning' | 'noon' | 'evening' | 'night' | 'late_night'

export const PERIOD_OPTIONS: {
  value: Period
  label: string
  time: string
}[] = [
  { value: 'morning', label: '早上', time: '7:30-8:30' },
  { value: 'noon', label: '中午', time: '11:30-12:30' },
  { value: 'evening', label: '初晚', time: '19:30-21:00' },
  { value: 'night', label: '中晚', time: '21:30-22:30' },
  { value: 'late_night', label: '深晚', time: '22:30-23:30' }
]

export const periodLabel = (p: string) =>
  PERIOD_OPTIONS.find((x) => x.value === p)?.label || p

export const periodTime = (p: string) =>
  PERIOD_OPTIONS.find((x) => x.value === p)?.time || ''
