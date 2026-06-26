# 本次更新 · 线上部署文档

> 适用范围：把本次「小红书发布日历（xhs_posts）+ 图片上传 + 模型列名兼容」这批改动部署到线上。
> 线上拓扑：**前端 Nuxt（容器） + 后端 Flask（容器） + 远程独立 MySQL（120.76.247.123）**。
> 服务器：`120.76.247.123`（阿里云 ECS，Ubuntu）。

---

## 0. 本次改动清单（先看这里）

| 模块 | 文件 | 改了什么 | 部署时是否需要额外动作 |
|------|------|----------|------------------------|
| 数据库 | `mysql-standalone/init.sql` | 新增 `xhs_posts` 表 + 幂等迁移存储过程 | ✅ **必须在远程 MySQL 执行迁移 SQL**（见第 2 步） |
| 后端 | `server/app/models/xhs_post.py` | 新增小红书内容模型 | 随后端镜像一起上线 |
| 后端 | `server/app/routes/xhs_posts.py` | 新增 `/api/xhs-posts` 接口 + 图片上传 | 随后端镜像一起上线 |
| 后端 | `server/app/__init__.py` | 注册新蓝图、创建 uploads 目录、暴露 `/uploads/<path>` 静态访问 | 需挂载 uploads 卷（compose 已含） |
| 后端 | `server/config/config.py` | 新增上传配置；默认 DB 指向远程 MySQL | 用 `.env` 覆盖密钥与 DB |
| 后端 | `server/app/models/home.py` / `user.py` | 模型列名映射到**线上已有列**（`image/link`、`password`） | ⚠️ 依赖线上表结构，见第 2.3 节 |
| 前端 | `web/app/pages/xiaohongshu-calendar.vue`、`web/app/pages/admin/xiaohongshu.vue` | 小红书日历前台页 + 后台管理页 | 随前端镜像一起上线 |
| 前端 | `web/app/middleware/admin.ts` | 后台路由权限中间件 | 随前端镜像一起上线 |
| 前端 | 多个 admin 页面、`login.vue`、`api.ts`、`nuxt.config.ts` | 配套调整 | 随前端镜像一起上线 |

> ⚠️ **新增数据库表是本次最关键的一步。** 因为线上连的是**远程独立 MySQL**（不是 compose 里那个 mysql 容器），所以 `init.sql` 不会自动跑，必须手动在远程库执行迁移。

---

## 1. 部署前检查

### 1.1 确认要部署的版本

在本地把改动提交并推送到远端仓库（服务器靠 `git pull` 拉取）：

```bash
git add -A
git commit -m "feat: 小红书发布日历 + 图片上传"
git push origin main
```

> 当前工作区还有未提交的改动（`docker-compose.yml`、`config.py`、`init.sql`、新增的 `xhs_post.py`/`xhs_posts.py`/前端页面等），**记得全部提交**，否则服务器拉不到。

### 1.2 关键端口约定（务必对齐）

| 服务 | 容器内端口 | 宿主机端口 | 说明 |
|------|-----------|-----------|------|
| 后端 Flask | 5000 | **见下方注意** | `run.py` 默认 5000 |
| 前端 Nuxt | 3000 | 3000 | |
| MySQL | 3306 | 远程库，自有端口 | 120.76.247.123:3306 |

> ⚠️ **端口不一致风险（必须处理）**：
> 前端镜像里写死了 API 地址为 `http://120.76.247.123:5001/api`（端口 **5001**），
> 但后端 `server/docker-compose.yml` 把 app 映射到了 **5000**。
> **两者必须一致**，否则前端调不通后端。二选一：
> - **方案 A（推荐，改后端映射）**：把 `server/docker-compose.yml` 里 app 的端口映射改成 `"5001:5000"`，对外就是 5001。
> - **方案 B（改前端）**：把 `web/Dockerfile` 和 `web/docker-compose.yml` 里的 `NUXT_PUBLIC_API_BASE` 改成 `:5000/api`，前端需重新构建。
>
> 下文按 **方案 A** 编写。

### 1.3 ECS 安全组放行端口

在阿里云控制台为该 ECS 放行入方向：

| 端口 | 协议 | 用途 |
|------|------|------|
| 22 | TCP | SSH |
| 3000 | TCP | 前端访问 |
| 5001 | TCP | 后端 API（方案 A） |
| 3306 | TCP | 仅当后端容器需从外网连 MySQL；同机内网则无需对公网开放 |

---

## 2. 数据库迁移（远程 MySQL，最关键）

> 目标库：`120.76.247.123` 上的 `xingshuzi` 库。本次要新增 `xhs_posts` 表。
> 迁移脚本是**幂等**的（重复执行安全），直接用 `init.sql` 里新增的那段即可。

### 2.1 准备迁移 SQL

`mysql-standalone/init.sql` 末尾已新增 `xhs_posts` 建表 + 兼容升级存储过程。把这段单独执行即可。可在服务器上把仓库里的 init.sql 直接喂给远程库（推荐，避免手抄出错）。

### 2.2 执行迁移

**方式一：用 mysql 客户端直接连远程库执行（推荐）**

```bash
# 在任意能连到 120.76.247.123 的机器上（建议就在 ECS 上）
mysql -h 120.76.247.123 -P 3306 -u jhadmin -p xingshuzi < /opt/xingshuzi/server-repo/mysql-standalone/init.sql
# 输入密码：Ww@204417
```

> `init.sql` 里建表用的是 `CREATE TABLE IF NOT EXISTS`，存储过程也做了「列/索引存在性判断」，对**已有数据无破坏**，可安全重复执行。

**方式二：只执行 xhs_posts 这一段**（如果不想跑整个 init.sql）

把 `init.sql` 中从 `-- 小红书发布内容表` 到 `DROP PROCEDURE IF EXISTS migrate_xhs_posts_student;` 之间的内容复制出来，存为 `migrate_xhs.sql`，再：

```bash
mysql -h 120.76.247.123 -P 3306 -u jhadmin -p xingshuzi < migrate_xhs.sql
```

### 2.3 校验迁移结果

```bash
mysql -h 120.76.247.123 -P 3306 -u jhadmin -p xingshuzi -e "
  SHOW CREATE TABLE xhs_posts\G
  SHOW INDEX FROM xhs_posts;
"
```

应能看到：
- 表 `xhs_posts` 存在；
- 含 `student` 列、`product` 为 `text` 类型；
- 唯一键为 `uq_date_student_period (post_date, student, period)`。

### 2.4 关于 home.py / user.py 的列名映射（重要前置条件）

本次后端把模型列名映射到了**线上已有列名**：
- `home_banners`：`image_url → image`、`link_url → link`
- `users`：`password_hash → password`，并新增读取 `status`、`updated_at`

➡️ **部署前确认线上这两张表的实际列名/字段确实如此**（否则后端启动后查询会报「Unknown column」）。校验：

```bash
mysql -h 120.76.247.123 -u jhadmin -p xingshuzi -e "
  DESC home_banners;
  DESC users;
"
```

- 若 `home_banners` 有 `image`/`link` 列、`users` 有 `password`/`status`/`updated_at` 列 → 直接部署。
- 若线上列名不同 → 需要先补列或调整模型映射后再上线。

---

## 3. 部署后端（Flask）

### 3.1 拉取代码

```bash
ssh root@120.76.247.123
cd /opt/xingshuzi-back        # 若不存在：mkdir -p 并 git clone <repo> .
git pull origin main
cd server                     # docker-compose.yml 在 server 目录
```

### 3.2 准备 `.env`（覆盖远程 MySQL 与密钥）

> 后端 `docker-compose.yml` 自带的 `mysql` 容器与本次**不使用**（线上连远程库）。
> 用 `.env` 把 `MYSQL_HOST` 等覆盖为远程库即可。

```bash
cat > .env << 'EOF'
# 远程独立 MySQL
MYSQL_USER=jhadmin
MYSQL_PASSWORD=Ww@204417
MYSQL_HOST=120.76.247.123
MYSQL_PORT=3306
MYSQL_DB=xingshuzi

# 生产密钥（请用下方命令重新生成后替换）
SECRET_KEY=请替换为随机值
JWT_SECRET_KEY=请替换为随机值
EOF
```

生成随机密钥：

```bash
python3 -c "import secrets; print('SECRET_KEY='+secrets.token_hex(32))"
python3 -c "import secrets; print('JWT_SECRET_KEY='+secrets.token_hex(32))"
```

### 3.3 调整端口映射与环境（方案 A）

编辑 `server/docker-compose.yml` 的 `app` 服务：

1. 端口映射改为对外 **5001**：
   ```yaml
       ports:
         - "5001:5000"
   ```
2. 把 `environment` 里写死的 MySQL 改为读 `.env`（或直接删掉这几行让 `.env` 生效）。当前 compose 里 app 的 env 写死了 `MYSQL_HOST=mysql` 等，**会覆盖 `.env`**，需改成：
   ```yaml
       environment:
         - MYSQL_USER=${MYSQL_USER}
         - MYSQL_PASSWORD=${MYSQL_PASSWORD}
         - MYSQL_HOST=${MYSQL_HOST}
         - MYSQL_PORT=${MYSQL_PORT}
         - MYSQL_DB=${MYSQL_DB}
         - SECRET_KEY=${SECRET_KEY}
         - JWT_SECRET_KEY=${JWT_SECRET_KEY}
   ```
3. 既然连远程库，可以**不启动本地 mysql 容器**：把 app 的 `depends_on` 那段删掉，并只启动 app 服务（见 3.4）。

> compose 里已挂载 `./uploads:/app/uploads`，上传的图片会持久化到宿主机 `server/uploads/`，重建容器不丢。确保该目录存在：`mkdir -p uploads`。

### 3.4 构建并启动

```bash
mkdir -p uploads

# 只启动后端 app（不起本地 mysql）
docker compose build app
docker compose up -d app

# 看日志确认启动无报错
docker compose logs -f app
```

> 若你保留了本地 mysql 容器定义但不想用它，`up -d app` 只会拉起 app；若 compose 仍因 `depends_on` 拉起 mysql，按 3.3 第 3 点删掉依赖即可。

### 3.5 验证后端

```bash
# 健康检查（首页接口）
curl http://localhost:5001/api/home/banners

# 小红书接口（新功能，按月查询打点）
curl "http://localhost:5001/api/xhs-posts/month?month=2026-06"
# 预期返回 {"code":200,...,"data":{"dates":[]}}（无数据时为空数组，不报错即正常）
```

返回正常 JSON 即后端 + 新表打通。

---

## 4. 部署前端（Nuxt）

### 4.1 确认 API 地址与后端端口一致

`web/Dockerfile` 与 `web/docker-compose.yml` 里 `NUXT_PUBLIC_API_BASE=http://120.76.247.123:5001/api`。
按方案 A 后端对外就是 5001，**无需改动**，直接部署即可。
（若你选了方案 B，把这两处的 `5001` 改成 `5000` 后再构建。）

### 4.2 构建并启动

```bash
cd /opt/xingshuzi-back        # 仓库根
git pull origin main          # 若已在 3.1 拉过可跳过
cd web

# 一键脚本（已含 down→build→up→健康检查）
chmod +x deploy.sh
./deploy.sh
```

或手动：

```bash
docker compose build --no-cache
docker compose up -d
docker compose logs -f
```

> 前端构建较慢（约 5–10 分钟）。`NUXT_PUBLIC_API_BASE` 是**构建期**注入的，改了它必须 `--no-cache` 重新 build 才生效。

### 4.3 验证前端

```bash
curl -I http://localhost:3000
```

浏览器访问：

- 前台首页：`http://120.76.247.123:3000`
- 小红书日历前台：`http://120.76.247.123:3000/xiaohongshu-calendar`
- 后台管理（需管理员登录）：`http://120.76.247.123:3000/admin/xiaohongshu`

---

## 5. 端到端验收（新功能）

1. 用管理员账号登录后台 `http://120.76.247.123:3000/login`。
2. 进入 `/admin/xiaohongshu`，选一个日期、同学（A/B/C）、时段（早/中/傍晚/晚）。
3. **上传一张配图** → 应返回图片 URL，且能在 `http://120.76.247.123:5001/uploads/xhs/xxx.jpg` 打开。
4. 填标题/文案，勾选「所挂商品」（至少一个），保存 → 返回 `保存成功`。
5. 打开前台 `/xiaohongshu-calendar`，对应日期应出现打点，点开能看到刚保存的内容。
6. 校验落库：
   ```bash
   mysql -h 120.76.247.123 -u jhadmin -p xingshuzi -e "SELECT id,post_date,student,period,title FROM xhs_posts ORDER BY id DESC LIMIT 5;"
   ```

---

## 6. 回滚

```bash
# 代码回滚到上一个可用提交
cd /opt/xingshuzi-back
git log --oneline -5           # 找到上一个稳定 commit
git checkout <上一个稳定commit>

# 后端
cd server && docker compose up -d --build app

# 前端
cd ../web && docker compose up -d --build
```

> **数据库回滚说明**：本次迁移只是「新增 `xhs_posts` 表 / 加列」，对旧表无破坏，回滚代码时**无需回滚数据库**。如确需移除，可 `DROP TABLE xhs_posts;`（会丢失小红书数据，谨慎）。

---

## 7. 常用运维命令

```bash
# 后端
cd /opt/xingshuzi-back/server
docker compose ps
docker compose logs -f app
docker compose restart app

# 前端
cd /opt/xingshuzi-back/web
docker compose ps
docker compose logs -f
docker compose restart

# 远程 MySQL 备份（建议上线前先备一次）
mysqldump -h 120.76.247.123 -u jhadmin -p xingshuzi > /opt/backups/xingshuzi_$(date +%Y%m%d_%H%M%S).sql
```

---

## 8. 上线 Checklist

- [ ] 本地改动已 commit 并 push 到 main
- [ ] **上线前已备份远程 MySQL**
- [ ] 远程 MySQL 已执行 `init.sql` 迁移，`xhs_posts` 表 + 唯一键存在（第 2 步）
- [ ] 已确认 `home_banners` / `users` 线上列名与模型映射一致（第 2.4 节）
- [ ] 端口已对齐：后端对外 5001 ＝ 前端 `NUXT_PUBLIC_API_BASE` 的 5001（第 1.2 节）
- [ ] ECS 安全组已放行 3000 / 5001
- [ ] 后端 `.env` 已填远程库 + 新随机密钥
- [ ] `server/uploads/` 目录已创建并挂载
- [ ] 后端验证：`/api/home/banners`、`/api/xhs-posts/month` 正常
- [ ] 前端验证：首页、`/xiaohongshu-calendar`、`/admin/xiaohongshu` 可访问
- [ ] 端到端：上传图片 + 保存内容 + 前台日历打点全通
