// 用户数据存储工具
// 注意：这是内存存储，生产环境应使用数据库

import { createHash } from 'node:crypto'

export interface User {
  username: string
  password: string // 加密后的密码
  role: 'admin' | 'user'
  createdAt: string
}

// 内存存储（生产环境应使用数据库）
const users: Map<string, User> = new Map()

// 初始化测试账号
export function initUsers() {
  // 初始化管理员账号
  if (!users.has('admin123')) {
    const adminPassword = hashPassword('admin123')
    users.set('admin123', {
      username: 'admin123',
      password: adminPassword,
      role: 'admin',
      createdAt: new Date().toISOString()
    })
  }

  // 初始化测试用户账号
  if (!users.has('user123')) {
    const userPassword = hashPassword('user123')
    users.set('user123', {
      username: 'user123',
      password: userPassword,
      role: 'user',
      createdAt: new Date().toISOString()
    })
  }
}

// 密码加密
export function hashPassword(password: string): string {
  return createHash('sha256').update(password).digest('hex')
}

// 验证密码
export function verifyPassword(password: string, hashedPassword: string): boolean {
  return hashPassword(password) === hashedPassword
}

// 根据用户名查找用户
export function findUserByUsername(username: string): User | undefined {
  return users.get(username)
}

// 检查用户名是否存在
export function userExists(username: string): boolean {
  return users.has(username)
}

// 创建用户
export function createUser(username: string, password: string, role: 'admin' | 'user' = 'user'): User {
  const hashedPassword = hashPassword(password)
  const newUser: User = {
    username,
    password: hashedPassword,
    role,
    createdAt: new Date().toISOString()
  }
  users.set(username, newUser)
  return newUser
}

// 获取所有用户（仅用于调试）
export function getAllUsers(): User[] {
  return Array.from(users.values())
}

// 初始化用户数据
initUsers()


