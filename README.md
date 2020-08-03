 movielens dataset 데이터를 이용한 검색 프로그램 
-------------

##### movielens data
> [movielens site](https://grouplens.org/datasets/movielens/100k/)

Development Environment
-------------
* mysql @
* python @3.7
* Spyder

Code
------------
###### tsv 내의 '|' 또는 ',' 로 데이터 분리하여 dataframe 가져와서, 튜플 형태로 바꿔 리스트에 저장 
```
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
```
###### pymysql 사용, Connection과 Cursor 사용,리스트 형태 데이터로 여러 개의 row 한 번에 insert 가능 
```
sql = "insert into u_data (user_id,id,rating,u_timestamp) values (%s,%s,%s,%s)"
curs.executemany(sql,data_list)
conn.commit()
```
###### 검색 sql 예시 
  > 사용자로부터 입력받은 직업군이 본 영화들에 대해 평점순으로 검색 
```
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
```
  > 선택한 영화 장르 중, 원하는 평점 이상의 영화 검색 
```
        # 입력받은 장르에 대한 원하는 평점 이상의 영화 검색
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
```
실행 예시 [콘솔 프로그램]
------------
![1](https://user-images.githubusercontent.com/52600701/89152602-70120680-d59e-11ea-8c31-67206547a0ed.PNG)
![2](https://user-images.githubusercontent.com/52600701/89152604-70aa9d00-d59e-11ea-8dff-3aa6cb53d435.PNG)

