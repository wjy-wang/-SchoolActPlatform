# 校园活动发布平台

## 项目简介
校园活动发布平台是一个用于统一管理校园活动信息、活动报名和用户互动的轻量型Web应用。

## 技术栈
- 后端: Django 4.2, Django REST Framework, JWT, Swagger
- 前端: Vue 3.x
- 数据库: MySQL 8.0
- 缓存: Redis 7.0+
- 部署: Nginx, Gunicorn

## 环境搭建

### 1. 安装Docker和Docker Compose
确保你的系统已安装Docker和Docker Compose。

### 2. 克隆项目
```bash
git clone https://github.com/wjy-wang/-SchoolActPlatform.git
cd -SchoolActPlatform
```

### 3. 启动服务
```bash
docker-compose up -d
```

### 4. 环境验证

#### 后端API验证
- Swagger文档: http://localhost:8000/swagger/
- ReDoc文档: http://localhost:8000/redoc/

#### 前端验证
- 前端页面: http://localhost/

#### 数据库验证
- MySQL数据库已在容器中运行，端口3306
- Redis缓存已在容器中运行，端口6379

### 5. 停止服务
```bash
docker-compose down
```

## 项目结构
```
school-activity-platform/
├── backend/
│   ├── manage.py
│   ├── school_activity/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── apps/
│   │   ├── users/
│   │   ├── activities/
│   │   ├── enrollments/
│   │   ├── comments/
│   │   └── favorites/
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   ├── router/
│   │   ├── store/
│   │   └── api/
│   ├── package.json
│   └── vite.config.js
├── docker-compose.yml
└── nginx.conf
```

## 安全说明
- 敏感信息通过环境变量配置，禁止硬编码
- 所有操作遵循沙箱隔离、权限最小化原则
- 用户密码采用加密存储
- 敏感数据传输加密
