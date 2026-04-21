# 校园活动发布平台

## 项目简介

校园活动发布平台是一个用于统一管理校园活动信息、活动报名和用户互动的轻量型 Web 应用。该平台支持管理员发布和管理活动，普通用户浏览、报名和收藏活动，以及评论互动功能。

## 功能特性

### Sprint 1 - 基础架构与用户管理 ✅

- [x] 项目初始化与技术栈搭建（Django + Vue.js）
- [x] 用户注册功能（支持学号/邮箱/手机号）
- [x] 用户登录功能（含记住密码）
- [x] 个人信息管理（修改资料、密码）
- [x] 权限管理系统（管理员/普通用户角色）

### Sprint 2 - 活动管理核心功能

- [ ] 活动发布功能（标题、时间、类型、地点、描述、图片）
- [ ] 活动编辑和删除功能
- [ ] 活动列表页面（支持按时间、类型筛选）
- [ ] 活动详情页面（展示活动信息）

### Sprint 3 - 活动报名与收藏功能

- [ ] 活动报名功能（普通用户）
- [ ] 取消报名功能（普通用户）
- [ ] 报名信息查看（管理员）
- [ ] 个人报名记录（普通用户）
- [ ] 活动收藏功能（普通用户）
- [ ] 取消收藏功能（普通用户）
- [ ] 收藏列表（普通用户）

### Sprint 4 - 评论互动与系统优化

- [ ] 活动评论功能（普通用户）
- [ ] 评论管理功能（管理员）
- [ ] 评论展示（活动详情页）
- [ ] 系统性能优化（缓存、数据库查询）
- [ ] 响应式设计优化（PC端和移动端）
- [ ] 系统测试与bug修复

## 技术栈

### 后端

- **框架**: Django 4.2 + Django REST Framework
- **认证**: JWT (JSON Web Token)
- **文档**: Swagger / ReDoc
- **数据库**: MySQL 8.0
- **缓存**: Redis 7.0+
- **部署**: Nginx + Gunicorn

### 前端

- **框架**: Vue 3.x (Composition API)
- **UI组件库**: Element Plus
- **状态管理**: Pinia
- **HTTP客户端**: Axios
- **构建工具**: Vite
- **图标**: Element Plus Icons

## 快速开始

### 环境要求

- Docker 20.10+
- Docker Compose 2.0+
- Node.js 18+ (前端开发)
- Python 3.11+ (后端开发)

### 1. 克隆项目

```bash
git clone https://github.com/wjy-wang/-SchoolActPlatform.git
cd -SchoolActPlatform
```

### 2. Docker 部署（推荐）

#### 启动所有服务

```bash
docker-compose up -d
```

#### 执行数据库迁移

```bash
docker-compose exec backend python manage.py migrate
```

#### 创建超级管理员

```bash
docker-compose exec backend python manage.py createsuperuser
```

#### 停止服务

```bash
docker-compose down
```

### 3. 本地开发

#### 后端开发

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件配置数据库和Redis连接

# 执行迁移
python manage.py migrate

# 创建超级管理员
python manage.py createsuperuser

# 启动开发服务器
python manage.py runserver
```

#### 前端开发

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

## 访问地址

| 服务         | 地址                           | 说明            |
| ------------ | ------------------------------ | --------------- |
| 前端页面     | http://localhost/              | 用户界面        |
| 后端API      | http://localhost:8000/api/     | RESTful API     |
| Swagger文档  | http://localhost:8000/swagger/ | API文档         |
| ReDoc文档    | http://localhost:8000/redoc/   | API文档（替代） |
| Django Admin | http://localhost:8000/admin/   | 管理后台        |

## API 接口文档

### 认证相关

| 接口                  | 方法    | 描述              | 权限   |
| --------------------- | ------- | ----------------- | ------ |
| `/api/auth/register/` | POST    | 用户注册          | 公开   |
| `/api/auth/login/`    | POST    | 用户登录（JWT）   | 公开   |
| `/api/auth/logout/`   | POST    | 用户登出          | 需登录 |
| `/api/auth/refresh/`  | POST    | 刷新Token         | 需登录 |
| `/api/auth/profile/`  | GET/PUT | 查看/修改个人信息 | 需登录 |
| `/api/auth/password/` | PUT     | 修改密码          | 需登录 |

### 用户管理（管理员）

| 接口               | 方法           | 描述               | 权限         |
| ------------------ | -------------- | ------------------ | ------------ |
| `/api/users/`      | GET            | 用户列表           | 管理员       |
| `/api/users/<id>/` | GET/PUT/DELETE | 用户详情/修改/删除 | 管理员或本人 |

### 请求示例

#### 用户注册

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123",
    "password_confirm": "testpass123",
    "email": "test@example.com",
    "student_id": "2024001",
    "phone": "13800138000"
  }'
```

#### 用户登录

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123",
    "remember_me": true
  }'
```

## 项目结构

```
school-activity-platform/
├── backend/                    # 后端项目
│   ├── apps/                   # 应用模块
│   │   ├── users/              # 用户模块
│   │   │   ├── models.py       # 用户模型
│   │   │   ├── views.py        # 视图/接口
│   │   │   ├── serializers.py  # 序列化器
│   │   │   ├── urls.py         # 路由配置
│   │   │   └── permissions.py  # 权限控制
│   │   ├── activities/         # 活动模块
│   │   ├── enrollments/        # 报名模块
│   │   ├── comments/           # 评论模块
│   │   └── favorites/          # 收藏模块
│   ├── school_activity/        # 项目配置
│   │   ├── settings.py         # 全局设置
│   │   ├── urls.py             # 根路由
│   │   └── wsgi.py             # WSGI配置
│   ├── manage.py               # Django管理脚本
│   ├── requirements.txt        # Python依赖
│   └── Dockerfile              # 后端Docker配置
├── frontend/                   # 前端项目
│   ├── src/
│   │   ├── api/                # API接口封装
│   │   │   └── auth.js         # 认证相关接口
│   │   ├── components/         # 公共组件
│   │   ├── router/             # 路由配置
│   │   │   └── index.js        # 路由定义
│   │   ├── stores/             # Pinia状态管理
│   │   │   └── user.js         # 用户状态
│   │   ├── utils/              # 工具函数
│   │   │   └── request.js      # Axios封装
│   │   ├── views/              # 页面视图
│   │   │   ├── auth/           # 认证页面
│   │   │   │   ├── Login.vue   # 登录页
│   │   │   │   └── Register.vue # 注册页
│   │   │   ├── home/           # 首页
│   │   │   └── profile/        # 个人中心
│   │   ├── App.vue             # 根组件
│   │   └── main.js             # 入口文件
│   ├── index.html              # HTML模板
│   ├── package.json            # 依赖配置
│   ├── vite.config.js          # Vite配置
│   └── Dockerfile              # 前端Docker配置
├── docker-compose.yml          # Docker编排配置
├── nginx.conf                  # Nginx配置
└── README.md                   # 项目说明
```

## 开发规范

### 后端开发

- 遵循 PEP 8 代码规范
- 使用类型注解提高代码可读性
- 编写 API 文档注释
- 单元测试覆盖率不低于 80%

### 前端开发

- 使用 Composition API 风格
- 组件名使用大驼峰命名
- 使用 `<script setup>` 语法糖
- 遵循 ESLint 代码规范

## 数据库设计

### 用户表 (users_user)

| 字段        | 类型         | 说明                         |
| ----------- | ------------ | ---------------------------- |
| id          | INT          | 主键                         |
| username    | VARCHAR(150) | 用户名                       |
| email       | VARCHAR(254) | 邮箱                         |
| student_id  | VARCHAR(20)  | 学号（唯一）                 |
| phone       | VARCHAR(11)  | 手机号（唯一）               |
| role        | INT          | 角色（0=普通用户, 1=管理员） |
| password    | VARCHAR(128) | 加密密码                     |
| date_joined | DATETIME     | 注册时间                     |

### 活动表 (activities_activity)

| 字段        | 类型         | 说明                                 |
| ----------- | ------------ | ------------------------------------ |
| id          | INT          | 主键                                 |
| title       | VARCHAR(100) | 活动标题                             |
| description | TEXT         | 活动描述                             |
| start_time  | DATETIME     | 开始时间                             |
| end_time    | DATETIME     | 结束时间                             |
| type        | INT          | 类型（0=讲座, 1=比赛, 2=晚会）       |
| location    | VARCHAR(100) | 活动地点                             |
| poster      | VARCHAR(200) | 海报URL                              |
| organizer   | VARCHAR(50)  | 组织者                               |
| status      | INT          | 状态（0=未开始, 1=进行中, 2=已结束） |
| created_by  | FK           | 创建者（外键）                       |
| created_at  | DATETIME     | 创建时间                             |

## 安全说明

- 敏感信息通过环境变量配置，禁止硬编码
- 所有操作遵循沙箱隔离、权限最小化原则
- 用户密码采用 Django 默认的 PBKDF2 算法加密存储
- JWT Token 设置合理的过期时间
- 敏感数据传输使用 HTTPS 加密
- 接口权限验证，防止未授权访问

## 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 联系方式

- 项目地址: https://github.com/wjy-wang/-SchoolActPlatform
- 问题反馈: https://github.com/wjy-wang/-SchoolActPlatform/issues

---

**注意**: 本项目为学习和演示用途，生产环境使用前请进行充分的安全测试和性能优化。
