import requests,json
from bs4 import BeautifulSoup
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'
}
openc = "a4eabe6f153e124a321cfb1a9905ec3c"


username = ""
passwd = ""
cookies = {}
courseId = ""
classId = ""
#fid 学校
fid = ""


def login(username, passwd):  # 获取cookie
    url = 'https://passport2-api.chaoxing.com/v11/loginregister'
    data = {'uname': username, 'code': passwd, }
    session = requests.session()
    cookie_jar = session.post(url=url, data=data, headers=headers).cookies
    cookie_t = requests.utils.dict_from_cookiejar(cookie_jar)  # cookiejar转字典
    return cookie_t

cookies = login(username,passwd)
#cookie_jar = json.loads(cookie)
cookies['k8s']='004486b6f3845f0bf20f4939fe9691fdfd56d3a8'
#cookies['route']='c010ccedb771f8b7c7793c67ee1d2aae'
cookies['thirdRegist']='0'
cookies['tl']='1'
cookies['uname']='1'
cookies['videojs_id']='1712380'

def writein(msg):
    with open("teacher_info.txt","r+",encoding="utf-8") as f:
        f.read()
        f.write(str(msg))
        if ('\n' not in msg):
            f.write("\n")

for pagenum in range(1,200):
        #department:学院,major:专业,class:班级
        url = "http://mooc1-1.chaoxing.com/teachingClassManage/newSearch?school=-1&department=-1&major=-1&class=-1&sw=&typeFlag=2&fid=" + fid + "&pageNum=" + str(
            pagenum) + "&pageSize=50&courseId=" + courseId + "&clazzId=" + classId
        url = "http://mooc1-1.chaoxing.com/teachingClassManage/searchTeacherNew?courseId="+courseId+"&name=&groupid=0&pages="+str(pagenum)+"&fid="+fid
        res = requests.get(url,headers=headers,cookies=cookies)
        res.encoding = 'utf-8'
        if(res.text == ""):
            print("获取完毕,共",pagenum+"页")
        #print(res.text)
        soup = BeautifulSoup(res.text,"lxml")
        all_tr = soup.find_all("tr")
        for col in all_tr:
            if "序号" in col.text:
                continue
            info = col.text[1:].replace('\n','\t')
            writein(info)
            print(info)
