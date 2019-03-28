# @Time     : 2019/3/6 23:17
# @Author   : sonny-zhang
# @FileName : urls.py
# @Blog     : http://www.cnblogs.com/1fengchen1/
from . import main
from .views import *

main.add_url_rule('/', view_func=Index.as_view('index'))
main.add_url_rule('/user/<username>', view_func=Users.as_view('user'))
main.add_url_rule('/edit-profile', view_func=EditProfile.as_view('edit_profile'))
main.add_url_rule('/edit-profile/<int:id>', view_func=EditProfileAdmin.as_view('edit_profile_admin'))
main.add_url_rule('/article/<int:id>', view_func=ArticleView.as_view('article'))
main.add_url_rule('/edit/<int:id>', view_func=ArticleEdit.as_view('edit'))

