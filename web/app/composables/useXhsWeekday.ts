import {
  type Weekday,
  getTodayWeekday
} from '~/utils/xhsWeekday'
import { fetchXhsMarkedWeekdays } from '~/utils/xhsPostsApi'

/** 小红书发布安排：按星期（周一至周日）选择，无具体日期 */
export function useXhsWeekday(initial?: Weekday) {
  const selectedWeekday = ref<Weekday>(initial || getTodayWeekday())
  const markedWeekdays = ref<Set<Weekday>>(new Set())

  const loadMarkedWeekdays = async () => {
    try {
      markedWeekdays.value = await fetchXhsMarkedWeekdays()
    } catch (error) {
      console.error('加载星期标记失败', error)
    }
  }

  const selectToday = () => {
    selectedWeekday.value = getTodayWeekday()
  }

  return {
    selectedWeekday,
    markedWeekdays,
    loadMarkedWeekdays,
    selectToday
  }
}
