import { type Student, STUDENT_ORDER } from '~/data/xhsStudents'
import {
  type Weekday,
  WEEKDAY_ORDER,
  getTodayWeekday
} from '~/utils/xhsWeekday'
import {
  type Period,
  PERIOD_OPTIONS
} from '~/utils/xhsPeriods'
import { fetchXhsMarkedWeekdays } from '~/utils/xhsPostsApi'

const PERIOD_VALUES = PERIOD_OPTIONS.map((p) => p.value)

export const parseXhsWeekday = (value: unknown): Weekday | null => {
  const s = String(value || '').toLowerCase()
  return WEEKDAY_ORDER.includes(s as Weekday) ? (s as Weekday) : null
}

export const parseXhsStudent = (value: unknown): Student | null => {
  const s = String(value || '').toLowerCase()
  return STUDENT_ORDER.includes(s as Student) ? (s as Student) : null
}

export const parseXhsPeriod = (value: unknown): Period | null => {
  const s = String(value || '').toLowerCase()
  return PERIOD_VALUES.includes(s as Period) ? (s as Period) : null
}

/** 发布安排页筛选（周几 / 号几 / 时段），与 URL query 同步，刷新可保留 */
export function useXhsScheduleFilters() {
  const route = useRoute()
  const router = useRouter()

  const readFromQuery = () => ({
    weekday: parseXhsWeekday(route.query.weekday) || getTodayWeekday(),
    student: parseXhsStudent(route.query.student) || ('a' as Student),
    period: parseXhsPeriod(route.query.period) || ('morning' as Period)
  })

  const initial = readFromQuery()
  const weekday = ref<Weekday>(initial.weekday)
  const student = ref<Student>(initial.student)
  const period = ref<Period>(initial.period)
  const markedWeekdays = ref<Set<Weekday>>(new Set())

  let syncingFromRoute = false

  const filterQuery = computed(() => ({
    weekday: weekday.value,
    student: student.value,
    period: period.value
  }))

  const scheduleLink = (path: string) => ({
    path,
    query: { ...filterQuery.value }
  })

  const syncToRoute = () => {
    if (syncingFromRoute) return
    const next = filterQuery.value
    const q = route.query
    if (
      q.weekday === next.weekday &&
      q.student === next.student &&
      q.period === next.period
    ) {
      return
    }
    router.replace({ path: route.path, query: next })
  }

  watch([weekday, student, period], syncToRoute)

  watch(
    () => [route.query.weekday, route.query.student, route.query.period],
    () => {
      const parsed = readFromQuery()
      if (
        parsed.weekday === weekday.value &&
        parsed.student === student.value &&
        parsed.period === period.value
      ) {
        return
      }
      syncingFromRoute = true
      weekday.value = parsed.weekday
      student.value = parsed.student
      period.value = parsed.period
      nextTick(() => {
        syncingFromRoute = false
      })
    }
  )

  const loadMarkedWeekdays = async () => {
    try {
      markedWeekdays.value = await fetchXhsMarkedWeekdays()
    } catch (error) {
      console.error('加载星期标记失败', error)
    }
  }

  return {
    weekday,
    student,
    period,
    markedWeekdays,
    filterQuery,
    scheduleLink,
    loadMarkedWeekdays
  }
}
