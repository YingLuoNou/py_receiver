# 配置指南
```
uv sync
notepad $PROFILE
```
添加函数
```
function receive {
    # 获取当前 PowerShell 所在的目录
    $currentDir = Get-Location
    # 使用 uv run 直接运行脚本，uv 会自动处理顶部声明的 flask 依赖
    uv run "C:你的目录\py_receiver\main.py" "$currentDir"
}
```