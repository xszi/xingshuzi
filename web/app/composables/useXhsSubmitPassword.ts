const STORAGE_KEY = 'xhs_submit_password'

/** 小红书发布安排：提交密码（本地记住，免登录提交用） */
export function useXhsSubmitPassword() {
  const submitPassword = ref('')

  onMounted(() => {
    if (process.client) {
      submitPassword.value = localStorage.getItem(STORAGE_KEY) || ''
    }
  })

  const rememberPassword = () => {
    if (process.client) {
      localStorage.setItem(STORAGE_KEY, submitPassword.value)
    }
  }

  const clearRemembered = () => {
    submitPassword.value = ''
    if (process.client) {
      localStorage.removeItem(STORAGE_KEY)
    }
  }

  return {
    submitPassword,
    rememberPassword,
    clearRemembered
  }
}
