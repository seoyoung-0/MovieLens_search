# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 22:04:38 2020

@author: kdy03
"""

#-*- coding: utf-8 -*-
import pymysql
import pandas as pd

u_users = pd.read_csv('u.user.tsv', sep='|',names=['id','age','gender','occupation','zip_code'])
u_item = pd.read_csv('u_item.tsv', sep='|',encoding='latin-1')
u_data = pd.read_csv('u_data.tsv', sep=',')
u_genre = pd.read_csv('u.genre.tsv', sep='|')


users_list=list(u_users.itertuples(index=False, name=None))
item_list=list(u_item.itertuples(index=False, name=None))
data_list=list(u_data.itertuples(index=False, name=None))
genre_list=list(u_genre.itertuples(index=False, name=None))

conn=pymysql.connect(host = '127.0.0.1',port=3307,user='201714164', 
                        password='db2020', db='db_201714164')
curs = conn.cursor(pymysql.cursors.DictCursor)


conn1=pymysql.connect(host = '127.0.0.1',port=3307,user='201714164', password='db2020',
                    db='db_201714164')
curs1 = conn1.cursor(pymysql.cursors.DictCursor)

'''
sql = "insert into u_data (user_id,id,rating,u_timestamp) values (%s,%s,%s,%s)"
curs.executemany(sql,data_list)
conn.commit()

sql = "insert into genre (genre_name,genre_id) values (%s,%s)"
curs.executemany(sql,genre_list)
conn.commit()

sql = "insert into users (user_id,age,gender,occupation,zip_code) values (%s,%s,%s,%s,%s)"
curs.executemany(sql,users_list)
conn.commit()

sql = "insert into items values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
curs.executemany(sql,item_list)
conn.commit()

'''
print("-----영화 검색 프로그램에 오신 것을 환영합니다.-----")
while 1:
    print("-----[ 1.직업 검색 2. 장르 검색 3. 평점 검색 0:exit]----- ")
    menu = int(input( "Your Choice(1-3) : "))
    
    if menu == 1:
        # 입력받은 직업군의 영화 평점 목록
        job = input("직업 을 입력하세요 :")
        sql1="""
        select d.id, avg(d.rating) as en_avg , i.movie_title
        from users u, u_data d, items i
        where u.user_id = d.user_id and d.id = i.id  and u.occupation= '%s'
        group by i.id
        order by avg(d.rating) desc, i.movie_title;
        """ %(job)
    
        job_based_search = pd.read_sql(sql1,conn)
        print(job_based_search)
        
    elif menu == 2:
        # 입력받은 장르에 대한 4.5 이상의 영화 
        genre_name_list=['Action','Adventure','Animation','Childrens','Comedy','Crime'
                         ,'Documentary','Drama','Fantasy','Film-Noir','Horror'
                         ,'Musical','Mystery','Romance','Sci-Fi','Thriller','War','Western']
        print("--- 영화 장르 리스트 ---" )
        for i in genre_name_list:
            print(i)
        selected_genre = input("장르를 입력하세요 : ")
        selected_rating = input(selected_genre
                        +"영화 중, 평점 몇 점 이상의 영화를 찾을까요? :")
        
        sql2="""
        select * from (
        select  i.movie_title,avg(d.rating) as g_avg
        from item_genre ig, items i, genre g, u_data d
        where ig.id = i.id and i.id = d.id and g.genre_name='%s'
        group by i.id)gs where g_avg >= %s order by g_avg desc;"""%(selected_genre,selected_rating)
        
        genre_search = pd.read_sql(sql2,conn)
        print(genre_search)
    elif menu == 3:
        under_rating = input("최소 평점(0.0~5.0) :")
        top_rating = input("최대 평(0.0~5.0):")
        #입력받은 평점 max, min 사이 영화 목록 
        sql = """
        select * from (
        select avg(d.rating) as m_avg, i.id , i.movie_title 
        from items i, u_data d
        where i.id = d.id 
        group by i.id
        order by avg(d.rating) desc) m
        where m_avg >= %s and m_avg <= %s""" %(under_rating,top_rating)
        
        df = pd.read_sql(sql,conn)
        print(df)
    else:
        print("안녕히 가세요, 또 봅시다.")
        break
    
curs.close()  
curs1.close()
conn.close()
conn1.close()
