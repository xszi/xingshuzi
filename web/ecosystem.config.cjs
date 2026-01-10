// PM2 进程管理器配置文件
// 使用方式: pm2 start ecosystem.config.cjs

module.exports = {
  apps: [
    {
      name: 'xingshuzi',
      script: '.output/server/index.mjs',
      instances: 2, // 或者使用 'max' 来使用所有 CPU 核心
      exec_mode: 'cluster', // 集群模式，充分利用多核 CPU
      env: {
        NODE_ENV: 'production',
        PORT: 3000,
        HOST: '0.0.0.0' // 监听所有网络接口
      },
      // 日志配置
      error_file: './logs/err.log',
      out_file: './logs/out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,
      // 自动重启配置
      autorestart: true,
      watch: false, // 生产环境建议关闭
      max_memory_restart: '1G', // 内存超过 1G 自动重启
      // 其他配置
      min_uptime: '10s', // 最小运行时间
      max_restarts: 10, // 最大重启次数
      restart_delay: 4000 // 重启延迟
    }
  ]
}





