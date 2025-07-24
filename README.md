# -CSDN-
前端bootstrap模板，后端django，数据库mysql，前后端不分离

本地启动项目
python manage.py runserver

将模型 (models.py) 的更改同步到数据库
python manage.py makemigrations 
python manage.py migrate

2025.7.24注
若重装python需要重新安装库

pip install django

若出现：django.core.exceptions.ImproperlyConfigured: Error loading MySQLdb module.
Did you install mysqlclient?
解决：
pip install mysqlclient
