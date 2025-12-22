# 本地生产服务器启动脚本 (PowerShell)
Write-Host "🚀 启动本地生产服务器..." -ForegroundColor Green
Write-Host ""
Write-Host "📦 服务器路径: .output\server\index.mjs" -ForegroundColor Cyan
Write-Host "🌐 访问地址: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "按 Ctrl+C 停止服务器" -ForegroundColor Yellow
Write-Host ""

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

$serverPath = Join-Path $scriptPath ".output\server\index.mjs"

if (-not (Test-Path $serverPath)) {
    Write-Host "❌ 错误: 找不到服务器文件。请先运行 'npm run build' 构建项目。" -ForegroundColor Red
    exit 1
}

node $serverPath


