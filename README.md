# MyBlog
Myself Blog source code.
## Support Function
- Register: [authentication user's email] [avatar of Gravatar] 
- Login: [change password] [change email] [change email] [reset password]  
- Article: [view] [edit]
## Depends on
- pipenv
## Using
- Clone this repositories 
```git
git clone https://github.com/sonny-zhang/MyBlog 
```
- You need to add two files: .env and mysql.env  
> This is the file contents: .env file
```env
FLASK_APP=manage.py  # 启动文件
MAIL_USERNAME=xxx@qq.com  # 因为config.py用的是qq发送邮箱，这里需要配置qq邮箱，其他邮箱请自己修改config配置
MAIL_PASSWORD=xxx  # 这是授权码
MyBlog_CONFIG=product  # 使用生产环境
MyBlog_DATABASE_URL=mysql+pymysql://root:123456@xxx.xxx.xx.xx:3306/myblog  # 数据库myblog需要手动创建好
```
> This is the file contents: mysql.env file
```env
MYSQL_ROOT_PASSWORD=123456  # 设置root密码
MYSQL_USER=sonny.zhang    # 创建一个sonny.zhang用户(这个用户不具备访问myblog权限，需要添加权限)
MYSQL_PASSWORD=sonny123     # 设置用户密码
```
- Run application
```shell
pipenv install
pipenv shell
gunicorn -b :80 manage:app
```
you can visit http://localhost , you will see page. 

- You also can use docker
```shell
docker-compose up -d
```

