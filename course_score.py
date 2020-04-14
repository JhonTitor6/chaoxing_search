import requests
from bs4 import BeautifulSoup
username = "18320552318"
passwd = "000322yq"
classId = 14290926
courseId =  207127146
inputUrl = ""
cookies = {}
done = 0
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'}
openc = "a4eabe6f153e124a321cfb1a9905ec3c"

def login(username, passwd):  # 获取cookie
    url = 'https://passport2-api.chaoxing.com/v11/loginregister'
    data = {'uname': username, 'code': passwd, }
    session = requests.session()
    cookie_jar = session.post(url=url, data=data, headers=headers).cookies
    cookie_t = requests.utils.dict_from_cookiejar(cookie_jar)  # cookiejar转字典
    return cookie_t

def getpagescore(pagenum):
    url = "https://mooc1-1.chaoxing.com/moocAnalysis/analysisScoreData"
    data = {
        'Accept-Language': 'zh,zh-CN;q=0.9,zh-TW;q=0.8,en;q=0.7',
        "classId": classId,
        "courseId": courseId,
        #不知道这是啥，经测试去掉也行
        #"openc": openc,
        "pageNum": pagenum,
        #按什么排序，可选：学生姓名，学号/工号（好像默认是这个），综合成绩
        "sortType": "综合成绩",
        #1是降序
        "order": 1,
        #
        "pageSize": 60
    }
    session = requests.session()
    res = session.post(url, data=data, headers=headers, cookies=cookies)
    if res.text == "":
        global done
        done = 1
        print("获取完成")
    soup = BeautifulSoup(res.text,'lxml')
    all_tr = soup.find_all("tr")
    for col in all_tr:
        all_td = col.find_all("td")
        #打印结果
        if(len(all_td)>7):
            name = all_td[1].text
            #名字补空格，强迫症为了好看而已
            if len(name) == 2:
                name = name + "  "
            id = all_td[2].text
            video_score = all_td[3].text.replace("\t",'').replace("\n",'').replace("\r",'')
            ceyan_score = all_td[4].text.replace("\t",'').replace("\n",'').replace("\r",'')
            fangwen_score = all_td[5].text.replace("\t",'').replace("\n",'').replace("\r",'')
            zuoye_score = all_td[6].text.replace("\t",'').replace("\n",'').replace("\r",'')
            kaoshi_score = all_td[7].text.replace("\t",'').replace("\n",'').replace("\r",'')
            zonghe_score = col.find_all(class_="borRightNone")[0].text.replace("\t",'').replace("\n",'').replace("\r",'')
            print(name,id,video_score,ceyan_score,fangwen_score,zuoye_score,zonghe_score)

def main():
    global  cookies,inputUrl,courseId,classId,done
    done = 0
    #获取courseId,classId
    print("请输入课程网址（应包含courseId=xxxx&clazzid=xxxx&）:")
    inputUrl = input()
    courseId = inputUrl.split("courseId=")[1].split("&clazzid=")[0]
    classId = inputUrl.split("courseId=")[1].split("&clazzid=")[1].split("&")[0]
    #默认获取20页
    for pagenum in range(1,20):
        if done == 1:
            break

        getpagescore(pagenum)

    main()

if __name__ == '__main__':
    #输入帐号密码
    #print("请输入帐号密码:")
    #username = input()
    #passwd = input()
    # 获取cookies，似乎用谁的cookies都无所谓
    try:
        cookies = login(username, passwd)
    except:
        print("登录失败,获取cookie失败")
    main()