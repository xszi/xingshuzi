# 安装 Node.js 20.19.0+ 的详细步骤

## 当前状态
- 当前 Node.js 版本: v20.6.0
- 项目要求: >= 20.19.0
- 错误: `Cannot redefine property: File` (由于版本过低)

## 方法 1: 使用 Homebrew 安装（推荐，最简单）

```bash
# 安装 Node.js 20 LTS
brew install node@20

# 如果已安装，升级到最新版本
brew upgrade node@20

# 验证安装
node -v
```

## 方法 2: 从官网下载安装（适合所有用户）

1. 访问 https://nodejs.org/
2. 下载 Node.js 20.x LTS 版本（当前最新是 20.19.x）
3. 运行安装程序
4. 验证安装：
   ```bash
   node -v
   npm -v
   ```

## 方法 3: 安装真正的 nvm（推荐用于开发）

### 步骤 1: 安装 nvm

在终端中运行：

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
```

如果遇到 SSL 证书问题，可以尝试：

```bash
curl -k -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
```

### 步骤 2: 重新加载 shell 配置

```bash
source ~/.zshrc
```

### 步骤 3: 安装 Node.js 20.19.0

```bash
nvm install 20.19.0
nvm use 20.19.0
nvm alias default 20.19.0  # 设置为默认版本
```

### 步骤 4: 验证

```bash
node -v  # 应该显示 v20.19.0 或更高
npm -v
```

## 方法 4: 手动下载并安装到 ~/.nvm/versions/node/

如果上述方法都不可用，可以手动下载：

1. 访问 https://nodejs.org/dist/v20.19.0/
2. 下载 macOS ARM64 版本: `node-v20.19.0-darwin-arm64.tar.gz`
3. 解压并移动到 nvm 目录：

```bash
cd ~/Downloads  # 假设下载到这里
tar -xzf node-v20.19.0-darwin-arm64.tar.gz
mkdir -p ~/.nvm/versions/node/
mv node-v20.19.0-darwin-arm64 ~/.nvm/versions/node/v20.19.0
```

4. 使用新版本：

```bash
nvm use 20.19.0
```

## 安装完成后的步骤

1. **验证版本**：
   ```bash
   node -v  # 应该 >= 20.19.0
   ```

2. **清理项目依赖**：
   ```bash
   cd /Users/jiuhua-pc/Desktop/xingshuzi/xingshuzi
   rm -rf node_modules .nuxt .output .cache
   ```

3. **重新安装依赖**：
   ```bash
   npm install
   # 或
   pnpm install
   ```

4. **启动开发服务器**：
   ```bash
   npm run dev
   ```

## 故障排除

### 如果 Homebrew 安装失败

检查 Homebrew 权限：
```bash
sudo chown -R $(whoami) /opt/homebrew/Cellar
```

### 如果 nvm 安装后无法使用

确保 `~/.zshrc` 中包含 nvm 初始化代码：
```bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
```

然后重新加载：
```bash
source ~/.zshrc
```

### 如果仍然遇到 "Cannot redefine property: File" 错误

1. 确保 Node.js 版本 >= 20.19.0
2. 完全清理并重新安装依赖
3. 检查是否有全局安装的冲突包

