<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-box">
        <h1 class="login-title">{{ isLogin ? '用户登录' : '用户注册' }}</h1>
        
        <form @submit.prevent="handleSubmit" class="login-form">
          <div class="form-group">
            <label for="username">用户名</label>
            <input
              id="username"
              v-model="formData.username"
              type="text"
              placeholder="请输入用户名"
              required
            />
          </div>

          <div class="form-group">
            <label for="password">密码</label>
            <input
              id="password"
              v-model="formData.password"
              type="password"
              placeholder="请输入密码"
              required
            />
          </div>

          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>

          <button type="submit" class="submit-btn" :disabled="loading">
            {{ loading ? '处理中...' : (isLogin ? '登录' : '注册') }}
          </button>
        </form>

        <div class="switch-mode">
          <span v-if="isLogin">
            还没有账号？
            <a href="#" @click.prevent="isLogin = false">立即注册</a>
          </span>
          <span v-else>
            已有账号？
            <a href="#" @click.prevent="isLogin = true">立即登录</a>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const { login, register } = useAuth()
const router = useRouter()

const isLogin = ref(true)
const loading = ref(false)
const errorMessage = ref('')

const formData = ref({
  username: '',
  password: ''
})

const handleSubmit = async () => {
  errorMessage.value = ''
  loading.value = true

  try {
    if (isLogin.value) {
      // 登录
      const result = await login(formData.value.username, formData.value.password)
      if (result.success) {
        // 登录成功，跳转到首页
        router.push('/')
      } else {
        errorMessage.value = result.message || '登录失败'
      }
    } else {
      // 注册
      const result = await register(formData.value.username, formData.value.password)
      if (result.success) {
        // 注册成功，切换到登录
        isLogin.value = true
        formData.value.password = ''
        errorMessage.value = ''
        alert('注册成功，请登录')
      } else {
        errorMessage.value = result.message || '注册失败'
      }
    }
  } finally {
    loading.value = false
  }
}

// SEO
useHead({
  title: '用户登录 - 行书子',
  meta: [
    { name: 'description', content: '行书子用户登录' }
  ]
})
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
}

.login-container {
  width: 100%;
  max-width: 400px;
}

.login-box {
  background: white;
  padding: 3rem 2.5rem;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.login-title {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
  text-align: center;
  margin: 0 0 2rem 0;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-size: 0.9rem;
  font-weight: 500;
  color: #555;
}

.form-group input {
  padding: 0.75rem 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
}

.error-message {
  padding: 0.75rem;
  background: #fee;
  color: #c33;
  border-radius: 8px;
  font-size: 0.9rem;
  text-align: center;
}

.submit-btn {
  padding: 0.875rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.switch-mode {
  margin-top: 1.5rem;
  text-align: center;
  font-size: 0.9rem;
  color: #666;
}

.switch-mode a {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
}

.switch-mode a:hover {
  text-decoration: underline;
}
</style>




