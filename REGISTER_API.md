# 用户注册接口实现说明

## 接口信息

- **路径**: `/api/auth/register`
- **方法**: `POST`
- **文件位置**: `server/api/auth/register.post.ts`

## 请求格式

```json
{
  "username": "testuser",
  "password": "password123"
}
```

## 响应格式

### 成功响应 (200)

```json
{
  "code": 200,
  "msg": "注册成功",
  "data": {
    "username": "testuser",
    "role": "user",
    "createdAt": "2025-01-15T10:30:00.000Z"
  }
}
```

### 错误响应

#### 用户名或密码为空 (400)
```json
{
  "code": 400,
  "msg": "用户名和密码不能为空",
  "data": null
}
```

#### 用户名格式不正确 (400)
```json
{
  "code": 400,
  "msg": "用户名格式不正确，只能包含字母、数字和下划线，长度3-20个字符",
  "data": null
}
```

#### 密码长度不足 (400)
```json
{
  "code": 400,
  "msg": "密码长度至少为6个字符",
  "data": null
}
```

#### 用户名已存在 (409)
```json
{
  "code": 409,
  "msg": "用户名已存在",
  "data": null
}
```

#### 服务器错误 (500)
```json
{
  "code": 500,
  "msg": "服务器内部错误",
  "data": null
}
```

## 验证规则

1. **用户名**:
   - 长度: 3-20 个字符
   - 格式: 只能包含字母（a-z, A-Z）、数字（0-9）和下划线（_）
   - 正则表达式: `/^[a-zA-Z0-9_]{3,20}$/`

2. **密码**:
   - 长度: 至少 6 个字符

## 实现细节

### 密码加密

使用 SHA-256 哈希算法加密密码（生产环境建议使用 bcrypt）：

```typescript
import { hashPassword } from '~/server/utils/users'
const hashedPassword = hashPassword(password)
```

### 用户存储

当前使用内存存储（`Map`），生产环境应替换为数据库：

- 文件: `server/utils/users.ts`
- 函数: `createUser(username, password, role)`

### 默认角色

新注册用户默认角色为 `user`（普通用户），管理员角色需要手动设置。

## 前端调用示例

```typescript
// 使用 useAuth composable
const { register } = useAuth()

const handleRegister = async () => {
  const result = await register('testuser', 'password123')
  if (result.success) {
    console.log('注册成功')
  } else {
    console.error('注册失败:', result.message)
  }
}
```

## 配置说明

### 使用 Nuxt API 路由（当前实现）

如果前端配置的 `apiBase` 指向外部服务（如 `http://127.0.0.1:5001/api`），需要修改配置以使用 Nuxt 的 API 路由：

**方法 1: 修改环境变量**

在 `.env` 文件中设置：
```bash
NUXT_PUBLIC_API_BASE=
```

或者在 `nuxt.config.ts` 中：
```typescript
runtimeConfig: {
  public: {
    apiBase: '' // 使用相对路径，调用 Nuxt API 路由
  }
}
```

**方法 2: 使用代理**

如果后端是独立服务，可以在 Nuxt 中创建代理路由。

## 测试

### 使用 curl 测试

```bash
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'
```

### 使用浏览器测试

1. 访问 `http://localhost:3000/login`
2. 点击"立即注册"
3. 输入用户名和密码
4. 点击"注册"按钮

## 注意事项

1. **数据持久化**: 当前使用内存存储，服务器重启后数据会丢失。生产环境必须使用数据库。

2. **密码安全**: SHA-256 不是最安全的密码加密方式，生产环境应使用 bcrypt 或 argon2。

3. **API 地址配置**: 确保前端配置的 `apiBase` 正确指向 Nuxt API 路由或后端服务。

4. **CORS**: 如果前后端分离部署，需要配置 CORS。

## 后续改进建议

1. ✅ 添加邮箱验证
2. ✅ 添加手机号验证
3. ✅ 实现密码强度检查
4. ✅ 添加验证码（防止机器人注册）
5. ✅ 实现数据库持久化
6. ✅ 使用更安全的密码加密算法（bcrypt）
7. ✅ 添加注册日志记录

