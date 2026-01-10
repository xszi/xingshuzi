// 本地生产服务器启动脚本
import { spawn } from 'child_process'
import { fileURLToPath } from 'url'
import { dirname, join } from 'path'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

const serverPath = join(__dirname, '.output', 'server', 'index.mjs')

console.log('🚀 启动本地生产服务器...')
console.log('📦 服务器路径:', serverPath)
console.log('🌐 访问地址: http://localhost:3000')
console.log('')

const server = spawn('node', [serverPath], {
  stdio: 'inherit',
  shell: true
})

server.on('error', (error) => {
  console.error('❌ 启动服务器失败:', error)
  process.exit(1)
})

server.on('exit', (code) => {
  if (code !== 0) {
    console.error(`❌ 服务器退出，代码: ${code}`)
    process.exit(code)
  }
})

// 处理退出信号
process.on('SIGINT', () => {
  console.log('\n🛑 正在关闭服务器...')
  server.kill('SIGINT')
  process.exit(0)
})

process.on('SIGTERM', () => {
  console.log('\n🛑 正在关闭服务器...')
  server.kill('SIGTERM')
  process.exit(0)
})





