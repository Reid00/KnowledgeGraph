from py2neo import Node,Relationship,Graph
import re

class CypherExercise():
    graph=None
    def __init__(self):
        print(r'start ...')
    def connectionDB(self):
        self.graph=Graph('http://localhost:7474',username='neo4j',password='Neo4j@123')
        print(r'connect neo4j sucess!')

    def cql_exercise(self):
        # 删除所有数据
        # self.graph.delete_all()
        # print(r'delete all nodes')

        # 创建节点
        node1=Node('Person',name='张三')
        node2=Node('Person',name='李四')
        node3=Node('Person',name='王五')
        self.graph.create(node1)
        self.graph.create(node2)
        self.graph.create(node3)
        print(r'node create successfully')
        # 查询cql
        query= 'match (p:Person) return p limit 25'
        res=self.graph.run(query).data
        print(res)

        #带有关系的查询
        q='match (p:Person)-[h:Has_Phone]->(p1:Phone) return p,p1 limit 10'
        # 带有where 条件的查询
        q='match (p:Person)-[h:Has_Phone]->(p1:Phone) where p.name=="张三" return p,p1 limit 10'

        # 二度关系的查询
        q='match (p:Person)-[h:Has_Phone]->(p1:Phone)-[:Call]->(p2:Phone) where p.name=="张三" return p,p1,p2'

        #利用call关系去查询
        q='match p=()-[c:Call]-() return p limit 10'

        #利用正则~查询
        q='match (n:Users) where n.name=~"Jack.*" return n limit 10'

        # 包含查询
        q='match (n:Users) where n.name contains "J" return n limit 10'

        # 创建关系
        q='Create (p:Person)-[l:Love]->(d:Dog)'

        # 创建带有属性的实体，关系
        q='Create (p:Person{name:"力气"})-[:Fear{Level:1}]->(t:Tiger{type: "东北话"})'

        # 给没有关系的实体，创建的关系
        q='match (p:Person{name:"力气"}),(p1:Person{name:"张三"}) Create(p)-[k:Know]->(p1)'

        #merge 有则返回，没有则创建
        q='match (p:Person{name:"力气"}),(p1:Person{name:"张三"}) Merge(p)-[k:Know]->(p1)'

        # 删除实体关系
        q='match (p:Person{name:"力气"})-[f:Fear]->(t:Tiger) delete f'
        q='match (p:Person{name:"力气"})-[f:Fear]->(t:Tiger) delete p'
        #同时删除
        q='match (p:Person)-[l:Love]->(d:Dog) delete p,l,d'

        #更新实体
        q='match (t:Tiger) where id(t)==1837 set t:Animal return Animal'

        #给实体增加属性
        q='match (a:Animal) where id(a)==1837 set a.age==10'

        # 给关系增加属性
        q='match (p:Person)-[l:Love]->(:Person) set l.dae="1990"' 

        # 查询姓名十二 三度关系内的朋友有哪些
        q='match (p:Person)-[:Friend_OF]-(p1:Person)-[:Friend_OF]-(p2:Person) where p.name="张三" return p,p1,p2'

        # 查询姓名十二 三度关系内的有关系的人有哪些
        q='match (p:Person)-[:]-(p1:Person)-[:]-(p2:Person) where p.name="张三" retrun p,p1,p2'

        # 姓名张三的通话记录有哪些
        q='match (p:Person)-[h:Has_Phone]->(ph:Phone)-[:Call]-(ph2:Phone) where p.name="张三" return p,h,ph,ph2'

        # 查询姓名2 和 姓名10 的最短路径
        #  APOC  [*..10] 十度关系内
        q='match (p1:Person{name:"姓名2"}), (p2:Person{name:"姓名10"}) p=shortestpath((p1)-[*..10]-(p2)) return p'
        # 查询姓名2 和 姓名10 的所有的最短路径
        q='match (p1:Person{name:"姓名2"}), (p2:Person{name:"姓名10"}) p=allshortestpaths((p1)-[*..10]-(p2)) return p'


        # 将hudong_pedia.csv 导入
        load='LOAD CSV WITH HEADERS  FROM "file:///hudong_pedia.csv" AS line CREATE (p:HudongItem{title:line.title,image:line.image,detail:line.detail,url:line.url,openTypeList:line.openTypeList,baseInfoKeyList:line.baseInfoKeyList,baseInfoValueList:line.baseInfoValueList})'

        # 创建索引
        create_index='CREATE CONSTRAINT ON (c:HudongItem) ASSERT c.title IS UNIQUE'
        
        # 删除索引
        drop_index='DROP CONSTRAINT ON (c:HudongItem) ASSERT c.title IS UNIQUE'


if __name__ == "__main__":
    cypher= CypherExercise()
    cypher.connectionDB()
    cypher.cql_exercise()