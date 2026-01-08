@echo off
echo 正在启动服务...
echo.

echo 启动后端服务 (Flask)...
start "后端服务" cmd /k "set MYSQL_HOST=127.0.0.1 && set MYSQL_PORT=3306 && set MYSQL_DB=xingshuzi && set MYSQL_USER=root && set MYSQL_PASSWORD=123456 && cd /d %~dp0server && python run.py"

timeout /t 3 /nobreak >nul

echo 启动前端服务 (Nuxt)...
start "前端服务" cmd /k "set NUXT_PUBLIC_API_BASE=http://127.0.0.1:5000/api && cd /d %~dp0web && npm run dev"

echo.
echo 服务已启动！
echo 后端服务: http://localhost:5000
echo 前端服务: http://localhost:3000
echo.
pause

