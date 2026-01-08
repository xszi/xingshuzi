// 用户注册接口
// POST /api/auth/register

import { userExists, createUser } from '~/server/utils/users'

export default defineEventHandler(async (event) => {
  try {
    // 读取请求体
    const body = await readBody(event)
    const { username, password } = body

    // 验证输入
    if (!username || !password) {
      return {
        code: 400,
        msg: '用户名和密码不能为空',
        data: null
      }
    }

    // 验证用户名格式（3-20个字符，只能包含字母、数字、下划线）
    const usernameRegex = /^[a-zA-Z0-9_]{3,20}$/
    if (!usernameRegex.test(username)) {
      return {
        code: 400,
        msg: '用户名格式不正确，只能包含字母、数字和下划线，长度3-20个字符',
        data: null
      }
    }

    // 验证密码长度（至少6个字符）
    if (password.length < 6) {
      return {
        code: 400,
        msg: '密码长度至少为6个字符',
        data: null
      }
    }

    // 检查用户名是否已存在
    if (userExists(username)) {
      return {
        code: 409,
        msg: '用户名已存在',
        data: null
      }
    }

    // 创建用户（默认角色为普通用户）
    const newUser = createUser(username, password, 'user')

    // 返回成功响应（不返回密码）
    return {
      code: 200,
      msg: '注册成功',
      data: {
        username: newUser.username,
        role: newUser.role,
        createdAt: newUser.createdAt
      }
    }
  } catch (error: any) {
    console.error('注册接口错误:', error)
    return {
      code: 500,
      msg: '服务器内部错误',
      data: null
    }
  }
})

