import os
import requests
import time
import random
import re


# 随机生成用户空间链接
def randomly_gen_uspace_url():
    url_list = []
    # 访问小黑屋用户空间不会获得积分、生成的随机数可能会重复，这里多生成两个链接用作冗余
    for i in range(12):
       # uid = random.randint(310000, 315000)
        uid = [51661,270644,21595,10196,317192,17365,317217,315706,210132,207016,133791,13815] 
        url = "https://ssdforum.org/space-uid-{}.html".format(str(uid[i]))
        url_list.append(url)
    return url_list

# 登录帐户
def login(username, password):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
    }
    login_url = "https://ssdforum.org/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1"
    login_data = {
        "fastloginfield": "username",
        "username": username,
        "password": password,
    }
    s = requests.Session()
    s.post(url=login_url, data=login_data, headers=headers)
    return s


# 通过抓取用户设置页面的标题检查是否登录成功
def check_login_status(s, number_c):
    test_url = "https://ssdforum.org/home.php?mod=spacecp"
    res = s.get(test_url)
    res.encoding = "gbk"
    test_title = re.findall("<title>.*?</title>", res.text)
    if test_title[0] != "<title>个人资料 -  SSDForum -  Powered by Discuz!</title>":
        print("第" + str(number_c) + "个帐户登录失败！")
        return False
    else:
        print("第" + str(number_c) + "个帐户登录成功！")
        return True


# 依次访问随机生成的用户空间链接获取积分
def get_points(s, number_c):
    if check_login_status(s, number_c):
        url_list = randomly_gen_uspace_url()
        # 使用for和try/except实现当前链接访问出错时不中断程序继续访问下一个链接
        for url in url_list:
            try:
                s.get(url)
                print("用户空间链接：" + url + " 访问成功")
                time.sleep(4)  # 每访问一个链接后休眠4秒，以避免触发论坛的防cc机制
            except Exception as e:
                print("链接访问异常：" + str(e))
            continue
    else:
        print("请检查你的帐户是否正确！")

# 依次留言随机生成的用户空间链接获取积分
def get_liuyan_points(s,number_c):
    if check_login_status(s, number_c):
        url = "https://ssdforum.org/home.php?mod=spacecp&ac=comment&inajax=1"
        uid = [306242, 316866, 10196, 250177, 78299, 315148, 58578, 18931]
        res = s.get("https://ssdforum.org/forum.php")
        matchObj = re.search(r'formhash=.*?"', str(res.content))
        str1 = str(matchObj.group())
        # 使用for和try/except实现当前链接访问出错时不中断程序继续访问下一个链接
        for i in range(len(uid)):
            try:
                data = {
                    "message": "[em:3:]",
                    "referer": "home.php%3Fmod%3Dspace%26uid%3D%26do%3Dwall",
                    "id": str(uid[i]),
                    "idtype": "uid",
                    "handlekey": "qcwall_" + str(uid[i]),
                    "commentsubmit": "true",
                    "quickcomment": "true",
                    "formhash": str1[9:17],
                }
                r = s.post(url, data=data)
                if re.search(r'\\xb2\\xd9\\xd7\\xf7\\xb3\\xc9\\xb9\\xa6', str(r.content)):
                    print("用户空间：" + "https://ssdforum.org/home.php?mod=space&uid=" + str(uid[i]) + "&do=wall " + " 留言成功")
                time.sleep(61)  # 每访问一个链接后休眠4秒，以避免触发论坛的防cc机制
            except Exception as e:
                print("链接访问异常：" + str(e))
                continue
    else:
        print("请检查你的帐户是否正确！")

# 依次留言随机生成的用户空间链接获取积分
def get_dazhaohu_points(s,number_c):
    uid = [110651,250177,715,311110,27929,5190]
    if check_login_status(s, number_c):
        # 使用for和try/except实现当前链接访问出错时不中断程序继续访问下一个链接
        for i in range(len(uid)):
            try:
                url = "https://ssdforum.org/home.php?mod=spacecp&ac=poke&op=send&uid=" + str(uid[i])+"&inajax=1"
                res = s.get("https://ssdforum.org/forum.php")
                matchObj = re.search(r'formhash=.*?"', str(res.content))
                str1 = str(matchObj.group())
                data = {
                    "referer": "https%3A%2F%2Fssdforum.org%2Fspace-uid-"+str(uid[i])+".html",
                    "pokesubmit": "true",
                    "formhash": str1[9:17],
                    "from": "",
                    "handlekey": "a_poke_"+str(uid[i]),
                    "iconid": "3",
                     "note" : "",
                }
                r = s.post(url, data=data)
                if re.search(r'succeedhandle_a_poke_', str(r.content)):
                    print("用户空间：" + "https://ssdforum.org/home.php?mod=space&uid=" + str(uid[i]) + " 打招呼成功")
                time.sleep(10)  # 每访问一个链接后休眠4秒，以避免触发论坛的防cc机制
            except Exception as e:
                print("链接访问异常：" + str(e))
                continue
    else:
        print("请检查你的帐户是否正确！")

if __name__ == "__main__":
    username = os.environ["HOSTLOC_USERNAME"]
    password = os.environ["HOSTLOC_PASSWORD"]
    # 分割用户名和密码为列表
    user_list = username.split(",")
    passwd_list = password.split(",")

    if len(user_list) != len(passwd_list):
        print("用户名与密码个数不匹配，请检查环境变量设置是否错漏！")
    else:
        print("共检测到" + str(len(user_list)) + "个帐户，开始获取积分")
        print("**************************************************")

        # 使用for和try/except实现当前用户获取积分出错时不中断程序继续尝试下一个用户
        for i in range(len(user_list)):
            try:
                s = login(user_list[i], passwd_list[i])
                get_points(s, i + 1)
                get_liuyan_points(s,i+1)
                get_dazhaohu_points(s,i+1)
                print("**************************************************")
            except Exception as e:
                print("获取积分异常：" + str(e))
            continue

        print("程序执行完毕，获取积分结束")
