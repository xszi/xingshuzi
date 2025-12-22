@echo off
echo 🚀 启动本地生产服务器...
echo.
echo 📦 服务器路径: .output\server\index.mjs
echo 🌐 访问地址: http://localhost:3000
echo.
echo 按 Ctrl+C 停止服务器
echo.

cd /d "%~dp0"
node .output\server\index.mjs

