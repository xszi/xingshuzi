# 启动所有服务的脚本
Write-Host "正在启动服务..." -ForegroundColor Green

# 启动后端服务
Write-Host "`n启动后端服务 (Flask)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "$env:MYSQL_HOST='127.0.0.1'; $env:MYSQL_PORT='3306'; $env:MYSQL_DB='xingshuzi'; $env:MYSQL_USER='root'; $env:MYSQL_PASSWORD='123456'; cd '$PSScriptRoot\server'; python run.py" -WindowStyle Normal

# 等待后端启动
Start-Sleep -Seconds 3

# 启动前端服务
Write-Host "启动前端服务 (Nuxt)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "$env:NUXT_PUBLIC_API_BASE='http://127.0.0.1:5000/api'; cd '$PSScriptRoot\web'; npm run dev" -WindowStyle Normal

Write-Host "`n服务已启动！" -ForegroundColor Green
Write-Host "后端服务: http://localhost:5000" -ForegroundColor Cyan
Write-Host "前端服务: http://localhost:3000" -ForegroundColor Cyan
Write-Host "`n按任意键退出..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

