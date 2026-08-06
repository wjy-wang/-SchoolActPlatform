#!/usr/bin/env python
"""
数据迁移脚本：将原有的 role=1 管理员转换为 Django is_staff 用户

使用方法：
1. 进入 Docker 容器：docker exec -it <container_name> /bin/bash
2. 切换到项目目录：cd /app/backend
3. 运行脚本：python migrate_admin_users.py

注意：此脚本仅需执行一次，用于迁移已有的自定义管理员用户。
如果数据库中不存在 role 字段，则无需执行此迁移。
"""

import os
import sys
import django

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_activity.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from apps.users.models import User

def migrate_admin_users():
    """迁移 role=1 的用户到 is_staff=True"""
    print("开始迁移管理员用户...")
    
    # 检查 role 字段是否存在
    if hasattr(User, 'role'):
        try:
            admin_users = User.objects.filter(role=1)
            count = admin_users.count()
            
            if count > 0:
                print(f"找到 {count} 个需要迁移的管理员用户")
                
                # 更新 is_staff 字段
                updated = admin_users.update(is_staff=True)
                print(f"成功将 {updated} 个用户标记为 staff")
                
                # 显示迁移的用户名
                for user in admin_users:
                    print(f" - {user.username} ({user.email})")
            else:
                print("没有找到需要迁移的管理员用户")
                
        except Exception as e:
            print(f"迁移过程中出现错误: {e}")
    else:
        print("User 模型中不存在 role 字段，无需执行迁移")

if __name__ == '__main__':
    migrate_admin_users()
    print("\n迁移完成！")
