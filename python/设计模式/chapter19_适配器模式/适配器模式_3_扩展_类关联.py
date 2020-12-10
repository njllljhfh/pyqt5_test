# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》--- 适配器模式_3_扩展_类关联 --- P-241"
"""
"""


# TODO:目标角色
# 员工信息接口
class IUserInfo(object):

    def get_user_name(self):
        """获取用户名"""
        pass

    def get_home_address(self):
        """获得家庭地址"""
        pass

    def get_mobile_number(self):
        """手机号码，这个太重要，手机泛滥呀"""
        pass

    def get_office_tel_number(self):
        """办公电话，一般是座机"""
        pass

    def get_job_position(self):
        """这个人的职位是什么"""
        pass

    def get_home_tel_number(self):
        """获得家庭电话，这有点不好，我不喜欢打家庭电话讨论工作"""
        pass


""" - - - """


# 实现类
class UserInfo(IUserInfo):

    def get_home_address(self):
        print(f"这里是员工的家庭地址...")

    def get_home_tel_number(self):
        print(f"员工的家庭电话是...")

    def get_job_position(self):
        print(f"这个人的职位是BOSS...")

    def get_mobile_number(self):
        print(f"这个人的手机号码是0000...")

    def get_office_tel_number(self):
        print(f"办公室电话是...")

    def get_user_name(self):
        print(f"姓名叫做...")


"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """


# 用户基本信息接口
class IOuterUserBaseInfo(object):

    def get_user_base_info(self) -> dict:
        """基本信息，比如名称、性别、手机号码等"""
        pass


# 用户家庭信息接口
class IOuterUserHomeInfo(object):

    def get_user_home_info(self) -> dict:
        """用户的家庭信息"""
        pass


# 用户工作信息接口
class IOuterUserOfficeInfo(object):

    def get_user_office_info(self) -> dict:
        """工作区域信息"""
        pass


""" - - - """


# TODO: 源角色
# 用户基本信息实现类
class OuterUserBaseInfo(IOuterUserBaseInfo):

    def get_user_base_info(self) -> dict:
        base_info = dict()
        base_info["user_name"] = "这个员工叫混世魔王...."
        base_info["mobile_number"] = "这个员工的额电话是...."
        return base_info


# 用户家庭信息实现类
class OuterUserHomeInfo(IOuterUserHomeInfo):

    def get_user_home_info(self):
        home_info = dict()
        home_info["home_tel_number"] = "员工的家庭电话是...."
        home_info["home_address"] = "员工的家庭地址是...."
        return home_info


# 用户工作信息实现类
class OuterUserOfficeInfo(IOuterUserOfficeInfo):

    def get_user_office_info(self):
        office_info = dict()
        office_info["job_position"] = "这个人的职位是BOSS...."
        office_info["office_tel_number"] = "员工的办公电话是...."
        return office_info


"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """


# TODO:【对象适配器】
# 适配器角色
class OuterUserInfo(IUserInfo):
    def __init__(self, base_info: IOuterUserBaseInfo, home_info: IOuterUserHomeInfo,
                 office_info: IOuterUserOfficeInfo):
        # 源角色的对象
        # TODO: 类关联
        self._base_info = base_info
        self._home_info = home_info
        self._office_info = office_info

        # 数据处理
        # TODO: OuterUserInfo 变成了委托服务，把 IUserInfo 接口需要的所有操作都委托给其他三个接口下的实现类，
        #       它的委托是通过对象层次的关联关系进行委托的，而不是继承关系。这就是【对象适配器】。
        #       我们之前讲的通过继承进行的适配器，叫做【类适配器】。
        self._base_map = self._base_info.get_user_base_info()
        self._home_map = self._home_info.get_user_home_info()
        self._office_map = self._office_info.get_user_office_info()

    def get_home_address(self):
        home_address = self._home_map["home_address"]
        print(f"{home_address}")
        return home_address

    def get_home_tel_number(self):
        home_tel_number = self._home_map["home_tel_number"]
        print(f"{home_tel_number}")
        return home_tel_number

    def get_job_position(self):
        job_position = self._office_map["job_position"]
        print(f"{job_position}")
        return job_position

    def get_mobile_number(self):
        mobile_number = self._base_map["mobile_number"]
        print(f"{mobile_number}")
        return mobile_number

    def get_office_tel_number(self):
        office_tel_number = self._office_map["office_tel_number"]
        print(f"{office_tel_number}")
        return office_tel_number

    def get_user_name(self):
        user_name = self._base_map["user_name"]
        print(f"{user_name}")
        return user_name


"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """


# 场景类
class Client(object):

    @staticmethod
    def main():
        # 外系统的人员信息
        baseInfo = OuterUserBaseInfo()
        homeInfo = OuterUserHomeInfo()
        officeInfo = OuterUserOfficeInfo()
        # 传递三个对象
        youngGirl = OuterUserInfo(baseInfo, homeInfo, officeInfo)
        # 从数据库中查到3个
        for i in range(3):
            youngGirl.get_mobile_number()


if __name__ == '__main__':
    client = Client()
    client.main()
