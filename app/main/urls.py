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
main.add_url_rule('/follow/<username>', view_func=Follow.as_view('follow'))
main.add_url_rule('/unfollow/<username>', view_func=UnFollow.as_view('unfollow'))
main.add_url_rule('/followers/<username>', view_func=Followers.as_view('followers'))
main.add_url_rule('/followed_by/<username>', view_func=FollowedBy.as_view('followed_by'))
main.add_url_rule('/show_all', view_func=ShowAll.as_view('show_all'))
main.add_url_rule('/show_followed', view_func=ShowFollowed.as_view('show_followed'))
main.add_url_rule('/moderate', view_func=Moderate.as_view('moderate'))
main.add_url_rule('/moderate/enable/<int:id>', view_func=ModerateEnable.as_view('moderate_enable'))
main.add_url_rule('/moderate/disable/<int:id>', view_func=ModerateDisable.as_view('moderate_disable'))


