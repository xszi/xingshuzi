/** 小红书发布账号（与后端 STUDENTS 一致） */
export type Student = 'a' | 'b' | 'c' | 'd'

export const STUDENT_ORDER: Student[] = ['a', 'b', 'c', 'd']

export const STUDENT_LABELS: Record<Student, string> = {
  a: '号1',
  b: '号2',
  c: '号3',
  d: '号4'
}

export const studentLabel = (s: string) =>
  STUDENT_LABELS[s as Student] || s

export const STUDENT_TABS = STUDENT_ORDER.map((name) => ({
  name,
  label: STUDENT_LABELS[name]
}))
