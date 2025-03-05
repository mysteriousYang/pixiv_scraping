# -*- coding: utf-8 -*-
#from functools import total_ordering
from turtle import back
from tqdm import trange,tqdm
from bs4 import BeautifulSoup
#import MySQLdb
import random
import time
import requests
import csv
import json
import os
import re

#hand made 
from _Logger import *
from conf import *
from __header import *
from __url import *

def Buddhism_bless():
    '''
    佛祖保佑
    '''                    
    #                      _ooOoo_
    #                     o8888888o
    #                     88" . "88
    #                     (| -_- |)
    #                      O\ = /O
    #                   ____/`---'\____
    #                .   ' \\| |// `.
    #                 / \\||| : |||// \
    #                / _||||| -:- |||||- \
    #                 | | \\\ - /// | |
    #               | \_| ''\---/'' | |
    #                \ .-\__ `-` ___/-. /
    #            ___`. .' /--.--\ `. . __
    #          ."" '< `.___\_<|>_/___.' >'"".
    #         | | : `- \`.;`\ _ /`;.`/ - ` : | |
    #            \ \ `-. \_ __\ /__ _/ .-` / /
    #   ======`-.____`-.___\_____/___.-`____.-'======
    #                      `=---='  
    
    return 'GOD'

#用于生成proxies字典
def proxies():
    return { "http": "127.0.0.1:" + str(proxies_port), 
             "https": "127.0.0.1:" + str(proxies_port), }

# #用于获取收藏页数
# def pagenumber(total):
#     i=0
#     if total%48!=0:
#         i=1
#     return total/48+i

class pixiv():
    def __init__(self,header):
        self.bookmark_header = header
        self.discovery_header = header
        self.illustrator_header = header
        #do somrthing
        pass

    # @disk_log
    def Get_bookmark(self,bookmark_url)->list:
        self.bookmark_header['Cookie'] = Cookie
        res={}
        try:
            # bookmark_url = "https://www.pixiv.net/ajax/user/17404403/illusts/bookmarks?tag=&offset=0&limit=48&rest=show&lang=zh&version=91606f25804acf7d59580f8b6ddf40e55cf4b3de"
            res = requests.get(bookmark_url,headers=self.bookmark_header,proxies=proxies())
            # print(res.json())
            if(res.status_code == 200):
                res = json.loads(res.content)
                if res['error']=='True':
                    print("[Connection Error]:: Cannot Pull Data from site{},\n please check your cookie".format(bookmark_url))
                    return False
            else:
                print("[Connection Error]:: Status_code {} ".format(res.status_code))
                return False
            # print(res)
            print('[Success] Get bookmark in URl {}'.format(bookmark_url))
            return res
        except Exception as ex:
            print("[Connection Error]:: {}".format(ex))
            return False

    def Get_discovery(self,discovery_url)->list:
        self.discovery_header['Cookie'] = Cookie
        try:
            res = requests.get(discovery_url,headers=self.discovery_header,proxies=proxies())
            #检测是否连接成功
            if(res.status_code == 200):
                # print(res.content.decode(encoding=res.encoding,errors='ignore'))
                # res = json.loads(res.text)
                res = json.loads(res.content)
                if res['error']=='True':
                    print("[Connection Error]:: Cannot Pull Data from site{},\n please check your cookie".format(Bookmark_url()))
                    return False
            else:
                print("[Connection Error]:: Status_code {} ".format(res.status_code))
                return False
            # print(res)
            print('[Success] Get discovery in URl {}'.format(discovery_url))
            return res
        except Exception as ex:
            print("[Connection Error]:: {}".format(ex))
            return False
        
    def Get_illustrator(self,illustrator_url)->list:
        #self.discovery_header['Cookie'] = Discover_cookies['Cookie']
        self.discovery_header['Cookie'] = Cookie
        res={}
        try:
            res = requests.get(illustrator_url,headers=self.illustrator_header,proxies=proxies())
            #检测是否连接成功
            if(res.status_code == 200):
                res = json.loads(res.content)
                if res['error']=='True':
                    print("[Connection Error]:: Cannot Pull Data from site{},\n please check your cookie".format(Bookmark_url()))
                    return False
            else:
                print("[Connection Error]:: Status_code {} ".format(res.status_code))
                return False
            # print(res)
            print('[Success] Get discovery in URl {}'.format(illustrator_url))
            return res
        except Exception as ex:
            print("[Connection Error]:: {}".format(ex))
            return False

class pa():
    #用于生成图片名
    def img_name(self,id,page,form):
        return '{}_p{}.{}'.format(id,page,form)

    #用于保存图片
    def img_save(self,dir,group,name,img_url,header)->None:
        save=r'{}\{}\{}'.format(dir,group,name)
        try:
            html=requests.get(img_url,headers=header,proxies=proxies())
        except:
            time.sleep(10)
            html=requests.get(img_url,headers=header,proxies=proxies())

        if(html.status_code<400):
            try:
                with open(save,'wb') as f:
                    f.write(html.content)
            except FileNotFoundError:
                os.mkdir(r'{}\{}'.format(dir,group))
                with open(save,'wb') as f:
                    f.write(html.content)
            except OSError:
                try:
                    save=r'{}\unclassify\{}'.format(dir,name)
                except:
                    os.mkdir(r'{}\unclassify'.format(dir))
                with open(save,'wb') as f:
                    f.write(html.content)
            print("Saved successed")
        else:
            print("Download Failed!")
                

    def load_history(history_path)->list:
        '''
        Load download history from disk
            history_path: Where hold *.history
            return: list obj[id ,pagedown]'''        
        img_history = []
        hs = r"{}\{}.history".format(history_path,userid)
        if os.path.exists(hs):
            with open(hs,'r') as csvf:
                reader = csv.reader(csvf)
                for row in reader:
                    img_history.append(row)
        return img_history
    @disk_log
    def convert_history(history_path,img_obj)->None:
        '''
        convert data to *.history on disk
            history_path: Where hold *.history
            if: id of the art works
            count: download count of img downloaded
        '''
        if not os.path.exists(history_path):
            os.mkdir(history_path)
        with open(r"{}\{}.history".format(history_path,userid),'a+') as csvf:
            writer = csv.writer(csvf)
            try:
                writer.writerow([img_obj['id'],img_obj['title'],img_obj['tags'],img_obj['userName'],img_obj['userId'],img_obj['updateDate'],img_obj['pageCount'],datetime.datetime.now()])
            except UnicodeEncodeError:
                writer.writerow([img_obj['id'],'?','?','?',img_obj['userId'],img_obj['updateDate'],img_obj['pageCount'],datetime.datetime.now()])
        return "{} has been saved to history".format(img_obj['id'])

    class likes():
        def __init__(self,) -> None:
            pass
        
        def run(self,response_data):
            temp = {}
            #db = MySQLdb.connect("localhost","root","2003%!$ZXY","PIXIV",charset='utf8')
            temp_list = []
            #其实也可以分类但我懒得写
            #把那个抄一遍就行
            #illusts_list = list(response_data['body']['works'])
            #final = 8

            for img_obj in response_data['body']['works']:
            #for img_obj in illusts_list[final:]:
                temp['id'] = img_obj['id']
                temp['title'] = img_obj['title']
                temp['time'] = re.sub(r'\D',re.escape("/"),img_obj['updateDate'][:19])
                temp['page_count'] = img_obj['pageCount']
                temp['tags'] = img_obj['tags']
                print('\n',temp)

                #time.sleep(random.randint(1,10))

                for i in range(0,temp['page_count']):
                    # time.sleep(random.randint(3,10))
                    
                    img_url='https://i.pximg.net/img-original/img/{}/{}'.format( temp['time'], pa.img_name(super(),temp['id'],i,'jpg'))
                    # print(img_url)
                    try:
                        html=requests.get(img_url,headers=Bookmark_header,proxies=proxies())
                    except:
                        with open(r'./fail.txt',"a") as fp:
                            fp.write(pa.img_name(super(),temp['id'],i,'jpg')+'\n')
                        print(pa.img_name(super(),temp['id'],i,'jpg'),"get failed")
                        continue

                    if(html.status_code<400):
                        pa.img_save(super(),save_path,'fav',pa.img_name(super(),temp['id'],i,'jpg'),img_url,Bookmark_header)
                    else:
                        #不是jpg就是png
                        img_url='https://i.pximg.net/img-original/img/{}/{}'.format(temp['time'],pa.img_name(super(),temp['id'],i,'png'))
                        try:
                            html=requests.get(img_url,headers=Bookmark_header,proxies=proxies())
                        except:
                            with open(r'./fail.txt',"a") as fp:
                                fp.write(pa.img_name(super(),temp['id'],i,'jpg')+'\n')
                            print(pa.img_name(super(),temp['id'],i,'jpg'),"get failed")
                            continue
                        if(html.status_code<400):
                            pa.img_save(super(),save_path,'fav',pa.img_name(super(),temp['id'],i,'png'),img_url,Bookmark_header)
                        else:
                            print(html.status_code)
                            print(html.text)
                pa.convert_history(save_path+'\history',img_obj)
                temp_list.append(temp)    
            return temp_list

    class discovery():
        def __init__(self,) -> None:
            pass
        
        def run(self,response_data):
            temp = {}
            #count=0
            temp_list = []
            #db = MySQLdb.connect("localhost","root","2003%!$ZXY","PIXIV",charset='utf8')
            #cursor = db.cursor()
            #读取分类用的json
            #嗯,很C风格的Python代码
            fp = open('tab.json','r')
            jsonFile = fp.read()
            rankData = json.loads(jsonFile)
            fp.close()
            
            for img_obj in response_data['body']['thumbnails']['illust']:
                temp['id'] = img_obj['id']
                temp['title'] = img_obj['title']
                temp['time'] = re.sub(r'\D',re.escape("/"),img_obj['updateDate'][:19])
                temp['page_count'] = img_obj['pageCount']
                temp['tags'] = img_obj['tags']
                temp['userName']=img_obj['userName']
                temp['userID']=img_obj['userId']
                
                # imgTagStr = ','.join(str(i) for i in img_obj["tags"])
                # sql = '''INSERT INTO discovery_pics VALUES ({},'{}','{}','{}',{},'{}',{},NOW(),NULL)
                # '''.format(img_obj["id"],img_obj["title"],imgTagStr,
                # img_obj["userName"],img_obj["userId"],img_obj["updateDate"],
                # img_obj["pageCount"])
                #try:
                #    cursor.execute(sql)
                #    db.commit()
                #except:
                #    print("DataBase Write Failed")
                #    db.rollback()
                    
                print('\n',temp)
                #初始化用第一个标签存储
                save_as = temp['tags'][0]
                rank = '0'
                #尝试获取rank,如果没有该tag就新增一个
                try:
                    rank = rankData[save_as]
                except KeyError:
                    rankData[save_as]='0'
                    jsonTemp = json.dumps(rankData)
                    fp = open('tab.json','w')
                    fp.write(jsonTemp)
                    fp.close()
                    print("Tag added:",(temp['tags'][0]))
                
                for tag_iterator in temp['tags']:
                    #尝试获取rank，如果没有该tag就新增一个
                    rank_temp='0'
                    try:
                        rank_temp = rankData[tag_iterator]
                    except KeyError:
                        rankData[tag_iterator]='0'
                        jsonTemp = json.dumps(rankData)
                        fp = open('tab.json','w')
                        fp.write(jsonTemp)
                        fp.close()
                        print("Tag added:",tag_iterator)
                    #这条用于打印图片tag的rank
                    #print("tag:",tag_interator,", rank =",rank_temp,end='\n')

                    #选择rank高的tag存储
                    if(rank_temp > rank):
                        rank = rank_temp
                        save_as = tag_iterator
                
                #随机时间,一定程度反爬(?)
                time.sleep(random.randint(1,10))
                print("Will be saved as {}".format(save_as))

                for i in range(0,temp['page_count']):
                    img_url='https://i.pximg.net/img-original/img/{}/{}'.format(temp['time'],pa.img_name(super(),temp['id'],i,'jpg'))
                    html=requests.get(img_url,headers=Discovery_header,proxies=proxies())

                    if(html.status_code<=400):
                        pa.img_save(super(),save_path,save_as,pa.img_name(super(),temp['id'],i,'jpg'),img_url,Discovery_header)
                    else:
                        #不是jpg就是png
                        img_url='https://i.pximg.net/img-original/img/{}/{}'.format(temp['time'],pa.img_name(super(),temp['id'],i,'png'))
                        html=requests.get(img_url,headers=Discovery_header,proxies=proxies())
                        if(html.status_code<=400):
                            pa.img_save(super(),save_path,save_as,pa.img_name(super(),temp['id'],i,'png'),img_url,Discovery_header)
                pa.convert_history(save_path+r'\history',img_obj)
                temp_list.append(temp)
            return temp_list
        
    class discovery_with_like():
        def __init__(self,depth=3,bookmark_count=1000) -> None:
            self.depth = depth
            self.bookmark_count=bookmark_count
            pass
        
        def get_pictures(self,response,recommend_lim):
            self.temp_list = []
            #self.db = MySQLdb.connect("localhost","root","2003%!$ZXY","PIXIV",charset='utf8')
            # self.cursor = self.db.cursor()
            #读取分类用的json
            #嗯,很C风格的Python代码
            fp = open('tab.json','r')
            jsonFile = fp.read()
            self.rankData = json.loads(jsonFile)
            fp.close()
            self.run(response_data=response,now_depth=1,recommend_lim=recommend_lim)

        def run(self,response_data,now_depth=1,recommend_lim=30):
            temp = {}
            if(now_depth >= self.depth):
                return

            elif(now_depth==1):

                self.temp_list = []
                fp = open('tab.json','r')
                jsonFile = fp.read()
                self.rankData = json.loads(jsonFile)
                fp.close()

                # print(response_data)

                for img_obj in response_data['body']['thumbnails']['illust']:
                    temp['id'] = img_obj['id']
                    temp['title'] = img_obj['title']
                    temp['time'] = re.sub(r'\D',re.escape("/"),img_obj['updateDate'][:19])
                    temp['page_count'] = img_obj['pageCount']
                    temp['tags'] = img_obj['tags']
                    temp['userName']=img_obj['userName']
                    temp['userID']=img_obj['userId']

                    bookmark_count_response = requests.get(url=BookmarkCount_url(temp['id']),headers=Discovery_header,proxies=proxies())
                    var1 = json.loads(bookmark_count_response.content)
                    temp['bookmarkCount']=var1['body']['bookmarkCount']
                    if(var1['body']['bookmarkCount']>=self.bookmark_count):
                    
                        # imgTagStr = ','.join(str(i) for i in img_obj["tags"])
                        # sql = '''INSERT INTO discovery_pics VALUES ({},'{}','{}','{}',{},'{}',{},NOW(),NULL)
                        # '''.format(img_obj["id"],img_obj["title"],imgTagStr,
                        # img_obj["userName"],img_obj["userId"],img_obj["updateDate"],
                        # img_obj["pageCount"])
                        # try:
                        #     self.cursor.execute(sql)
                        #     self.db.commit()
                        # except:
                        #     print("DataBase Write Failed")
                        #     self.db.rollback()
                            
                        print('\n',temp)
                        #初始化用第一个标签存储
                        save_as = temp['tags'][0]
                        rank = '0'
                        #尝试获取rank,如果没有该tag就新增一个
                        try:
                            rank = self.rankData[save_as]
                        except KeyError:
                            self.rankData[save_as]='0'
                            jsonTemp = json.dumps(self.rankData)
                            fp = open('tab.json','w')
                            fp.write(jsonTemp)
                            fp.close()
                            print("Tag added:",(temp['tags'][0]))
                        
                        for tag_iterator in temp['tags']:
                            #尝试获取rank，如果没有该tag就新增一个
                            rank_temp='0'
                            try:
                                rank_temp = self.rankData[tag_iterator]
                            except KeyError:
                                self.rankData[tag_iterator]='0'
                                jsonTemp = json.dumps(self.rankData)
                                fp = open('tab.json','w')
                                fp.write(jsonTemp)
                                fp.close()
                                print("Tag added:",tag_iterator)
                            #这条用于打印图片tag的rank
                            #print("tag:",tag_interator,", rank =",rank_temp,end='\n')

                            #选择rank高的tag存储
                            if(rank_temp > rank):
                                rank = rank_temp
                                save_as = tag_iterator
                        
                        #随机时间,一定程度反爬(?)
                        
                        time.sleep(random.randint(1,10))
                        print("Will be saved as {}".format(save_as))

                        for i in range(0,temp['page_count']):
                            
                            img_url='https://i.pximg.net/img-original/img/{}/{}'.format(temp['time'],pa.img_name(super(),temp['id'],i,'jpg'))
                            html=requests.get(img_url,headers=Discovery_header,proxies=proxies())
                            if(html.status_code<=400):
                                pa.img_save(super(),save_path,save_as,pa.img_name(super(),temp['id'],i,'jpg'),img_url,Discovery_header)
                            else:
                                #不是jpg就是png
                                img_url='https://i.pximg.net/img-original/img/{}/{}'.format(temp['time'],pa.img_name(super(),temp['id'],i,'png'))
                                html=requests.get(img_url,headers=Discovery_header,proxies=proxies())
                                if(html.status_code<400):
                                    pa.img_save(super(),save_path,save_as,pa.img_name(super(),temp['id'],i,'png'),img_url,Discovery_header)
                        
                        pa.convert_history(save_path+r'\history',img_obj)
                        self.temp_list.append(temp)

                        recommend_response = requests.get(url=Recommend_url(temp['id'],recommend_lim),headers=Discovery_header,proxies=proxies())
                        #print(recommend_response)
                        recommend_response = json.loads(recommend_response.content)
                        self.run(response_data=recommend_response, now_depth= now_depth+1,recommend_lim=recommend_lim)
                        
                    else:
                        pass

            elif(now_depth>1):

                for img_obj in response_data['body']['illusts']:
                    #这个try确实有点大了
                    try:
                        temp['id'] = img_obj['id']
                        temp['title'] = img_obj['title']
                        temp['time'] = re.sub(r'\D',re.escape("/"),img_obj['updateDate'][:19])
                        temp['page_count'] = img_obj['pageCount']
                        temp['tags'] = img_obj['tags']
                        temp['userName']=img_obj['userName']
                        temp['userID']=img_obj['userId']

                        bookmark_count_response = requests.get(url=BookmarkCount_url(temp['id']),headers=Discovery_header,proxies=proxies())
                        var1 = json.loads(bookmark_count_response.content)
                        temp['bookmarkCount']=var1['body']['bookmarkCount']
                        if(var1['body']['bookmarkCount']>=self.bookmark_count):
                        
                            # imgTagStr = ','.join(str(i) for i in img_obj["tags"])
                            # sql = '''INSERT INTO discovery_pics VALUES ({},'{}','{}','{}',{},'{}',{},NOW(),NULL)
                            # '''.format(img_obj["id"],img_obj["title"],imgTagStr,
                            # img_obj["userName"],img_obj["userId"],img_obj["updateDate"],
                            # img_obj["pageCount"])
                            # try:
                            #     self.cursor.execute(sql)
                            #     self.db.commit()
                            # except:
                            #     print("DataBase Write Failed")
                            #     self.db.rollback()
                                
                            print('\n',temp)
                            #初始化用第一个标签存储
                            save_as = temp['tags'][0]
                            rank = '0'
                            #尝试获取rank,如果没有该tag就新增一个
                            try:
                                rank = self.rankData[save_as]
                            except KeyError:
                                self.rankData[save_as]='0'
                                jsonTemp = json.dumps(self.rankData)
                                fp = open('tab.json','w')
                                fp.write(jsonTemp)
                                fp.close()
                                print("Tag added:",(temp['tags'][0]))
                            
                            for tag_interator in temp['tags']:
                                #尝试获取rank，如果没有该tag就新增一个
                                rank_temp='0'
                                try:
                                    rank_temp = self.rankData[tag_interator]
                                except KeyError:
                                    self.rankData[tag_interator]='0'
                                    jsonTemp = json.dumps(self.rankData)
                                    fp = open('tab.json','w')
                                    fp.write(jsonTemp)
                                    fp.close()
                                    print("Tag added:",tag_interator)
                                #这条用于打印图片tag的rank
                                #print("tag:",tag_interator,", rank =",rank_temp,end='\n')

                                #选择rank高的tag存储
                                if(rank_temp > rank):
                                    rank = rank_temp
                                    save_as = tag_interator
                            
                            #随机时间,一定程度反爬(?)
                            time.sleep(random.randint(1,10))
                            print("Will be saved as {}".format(save_as))

                            for i in range(0,temp['page_count']):
                                
                                img_url='https://i.pximg.net/img-original/img/{}/{}'.format(temp['time'],pa.img_name(super(),temp['id'],i,'jpg'))
                                html=requests.get(img_url,headers=Discovery_header,proxies=proxies())
                                if(html.status_code<400):
                                    pa.img_save(super(),save_path,save_as,pa.img_name(super(),temp['id'],str(i),'jpg'),img_url,Discovery_header)
                                else:
                                    #不是jpg就是png
                                    img_url='https://i.pximg.net/img-original/img/{}/{}'.format(temp['time'],pa.img_name(super(),temp['id'],i,'png'))
                                    html=requests.get(img_url,headers=Discovery_header,proxies=proxies())
                                    if(html.status_code<=400):
                                        pa.img_save(super(),save_path,save_as,pa.img_name(super(),temp['id'],str(i),'png'),img_url,Discovery_header)
                            pa.convert_history(save_path+r'\history',img_obj)
                            self.temp_list.append(temp)

                            recommend_response = requests.get(url=Recommend_url(temp['id'],recommend_lim),headers=Discovery_header,proxies=proxies())
                            self.run(response_data=recommend_response, now_depth=now_depth+1,recommend_lim=recommend_lim)
                            
                        else:
                            pass    
                    except:
                        continue
            return self.temp_list

    class illustrator():
        def __init__(self,) -> None:
            pass

        # def init_Imglist(self,response_data):
        #     total = response_data['body']['total']
        #     return [int(total),]
        
        def run(self,response_data):
            temp = {}
            #db = MySQLdb.connect("localhost","root","2003%!$ZXY","PIXIV",charset='utf8')
            temp_list = []
            #其实也可以分类但我懒得写
            #把那个抄一遍就行
            illusts_id_list = list(response_data['body']['illusts'].keys())
            #illusts_list = []

            #print(illusts_id_list)
            # final = illusts_id_list.index('114177782')
            for id in illusts_id_list:
            # for id in illusts_id_list[final:]:
                try:
                    response = requests.get(url=BookmarkCount_url(id),headers=Illustrator_header,proxies=proxies())
                except:
                    print(id," failed")
                    continue
                
                img_obj = response.json()['body']
                #print(id," successed")
                
                temp['id'] = img_obj['id']
                temp['title'] = img_obj['title']
                temp['time'] = re.sub(r'\D',re.escape("/"),img_obj['uploadDate'][:19])
                temp['page_count'] = img_obj['pageCount']
                temp['tags'] = []

                temp['userName'] = img_obj['userName']
                temp['userId'] = img_obj['userId']

                print('\n',temp)

                

                img_url = img_obj['urls']['original']
                for i in range(0,temp['page_count']):
                    suffix = img_url[-4:]
                    if(i<=10):
                        img_url = img_url[:-5] + str(i) + suffix
                    elif(i>10):
                        img_url = img_url[:-6] + str(i) + suffix
                    # print(img_url)
                    time.sleep(random.randint(0,5))
                    try:
                        html=requests.get(img_url,headers=Illustrator_header,proxies=proxies())
                    except:
                        print("Cannot connect to Proxy!")
                        time.sleep(30)
                        #html=requests.get(img_url,headers=Illustrator_header,proxies=proxies())
                        continue
                    #print(html)
                    if(html.status_code<400):
                        try:
                            pa.img_save(super(),save_path, temp['userName'], pa.img_name(super(),temp['id'],i,suffix[1:]),img_url,Illustrator_header )
                        except:
                            #如果名字含有非法字符就用id保存
                            print("Illegal author name!")
                            pa.img_save(super(),save_path, temp['id'], pa.img_name(super(),temp['id'],i,suffix[:1]),img_url,Illustrator_header )
                    else:
                        print("Invalid picture url!")
                        
                #pa.convert_history(save_path+'\history',temp)
                temp_list.append(temp) 

            return temp_list

def operate(pge,mode = "discovery"):
    if(mode == "discovery"):
        Pixiv = pixiv(Discovery_header)
        # reptile = pa().discovery()
        reptile = pa().discovery_with_like(depth=3,bookmark_count=3000)
        res = Pixiv.Get_discovery(Discovery_url(50,mode='all'))

    elif(mode == "illustrator"):
        Pixiv = pixiv(Illustrator_header)
        reptile = pa().illustrator()
        res = Pixiv.Get_illustrator(Illustrator_url(target_userid))

    elif(mode == "likes"):
        Pixiv = pixiv(Bookmark_header)
        reptile = pa().likes()
        res = Pixiv.Get_bookmark(Bookmark_url(userid,pge,hide='show'))
        # res = Pixiv.Get_bookmark(Bookmark_url(userid,pge,hide='hide'))

    else:
        print("Unknown mode!")
        return

    # print(res)

    reptile.run(res)



if __name__ == '__main__':
    for i in range(0,20):
        operate(i,mode='likes')
        # operate(i, mode='discovery')
        # operate(i,'illustrator')