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
        
        #查找属性相同并且值相同的节点
        q= 'match (n:references),(p:references) with n,p unwind keys(n) as keyn unwind keys(p) as keyp with n,p,keyn,keyp where keyp=keyn and n[keyn]<>"" return keyn,n[keyn],keyp,n[keyp] limit 2'
        
        #删除重复节点，可用id 不同其他相同

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
        # 创建多维复杂关系
        q='match (p:Person{name:"李四"}),(p1:Person{name:"赵四"}),(p2:Person{name:"王五"}) CREATE (p)-[h:Hate]->(p1)<-[l:Love]-(p2) return p,p1,p2,h,l'
        # 创建带有属性的实体，关系
        q='Create (p:Person{name:"力气"})-[:Fear{Level:1}]->(t:Tiger{type: "东北话"})'

        # 给没有关系的实体，创建的关系
        q='match (p:Person{name:"力气"}),(p1:Person{name:"张三"}) Create(p)-[k:Know]->(p1)'

        #merge 有则返回，没有则创建
        q='Merge (p:Person{name:"力气"}),(p1:Person{name:"张三"}) Merge(p)-[k:Know]->(p1)'


        # 删除所有的节点和关系
        q='match (p:Person) delete p'
        # 删除所有孤立的点
        q='MATCH (n) WHERE NOT (n)--() DELETE n'
        # 同时删除关系；这个查询适用于删除少量的数据，不适用于删除巨量的数据
        q='match (p:Person) detach delete p'
        # 删除一个节点及其所有的关系
        q='match (p:Person{name:"力气"}) detach delete p'
        # 只删除实体
        q='match (p:Person{name:"力气"})-[f:Fear]->(t:Tiger) delete p'
        #同时删除
        q='match (p:Person)-[l:Love]->(d:Dog) delete p,l,d'
        # 删除实体关系
        q='match (p:Person{name:"力气"})-[f:Fear]->(t:Tiger) delete f'

        # 删除一个属性;neo4j不允许属性存储空值null。如果属性的值不存在，那么节点或者关系中的属性将被删除。这也可以通过remove来删除。
        q='match (p:Person{name :"Andres"}) remove p.age return p'
        # 删除节点的一个标签
        q='match (p:Person{name: "张三"}) remove p:Chinese return p'
        # 删除节点的多个标签
        q='mathc (p:Person{name:"张三"}) remove p:Chinise:Student return p'


        #更新实体，添加标签animal
        q='match (t:Tiger) where id(t)==1837 set t:Animal return Animal'
        # 给实体添加更多标签
        q='match (p:Person{name:"李四"}) set p:Chinese:Student return p'

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
        #  APOC  [*..10] 十度关系内,[:KNOWS*1..2] 认识的一度或者两度关系
        # Cypher语言支持变长路径的模式，变长路径的表示方式是：[*N..M]，N和M表示路径长度的最小值和最大值。
        # (a)-[*2]->(b)：表示路径长度为2，起始节点是a，终止节点是b；
        # (a)-[*3..5]->(b)：表示路径长度的最小值是3，最大值是5，起始节点是a，终止节点是b；
        # (a)-[*..5]->(b)：表示路径长度的最大值是5，起始节点是a，终止节点是b；
        # (a)-[*3..]->(b)：表示路径长度的最小值是3，起始节点是a，终止节点是b；
        # (a)-[*]->(b)：表示不限制路径长度，起始节点是a，终止节点是b；
        q='match (p1:Person{name:"姓名2"}), (p2:Person{name:"姓名10"}) p=shortestpath((p1)-[*..10]-(p2)) return p'
        # 查询姓名2 和 姓名10 的所有的最短路径
        q='match (p1:Person{name:"姓名2"}), (p2:Person{name:"姓名10"}) p=allshortestpaths((p1)-[*..10]-(p2)) return p'

        # with从句可以连接多个查询的结果，即将上一个查询的结果用作下一个查询的开始。with的每一个结果，必须使用别名标识
        #两种用法：
        #1、通过使用oder by 和limit，with可以限制传入下一个match子查询语句的实体数目。
        #2、对聚合值过滤。
        # 3. collect 返回一个list
        # sample: 
        q='MATCH (n) WITH n ORDER BY n.name DESC LIMIT 3 RETURN collect(n.name)'

        # 利用with n.name 把传给了后面, 用collect 对名字重复的过滤
        q='MATCH (p:Person) with p.name AS Name, collect(p) AS nodes where size(nodes)>1 return nodes'
        q='MATCH (p:Person) with p.name AS Name, collect(p) AS nodes where size(nodes)>1 FOREACH(i in tail(nodes)|DETACH DELETE i) return i'

        # http://www.tastones.com/stackoverflow/neo4j/cypher/deletion/
        #分页排序
        q='Match (n:Person) RETURN n  ORDER BY n.name ASC Skip 1 limit 3'
        # 以T 开头的电影
        q='MATCH (actor:Person)-[:ACTED_IN]->(movie:Movie) WHERE movie.title STARTS WITH "T" RETURN movie.title AS title, collect(actor.name) AS cast ORDER BY title ASC LIMIT 10'

    def load_data_csv(self):
        #load node csv 
        command='USING PERIODIC COMMIT 1000 LOAD CSV WITH HEADERS FROM "file:///nodes.csv" AS csvLine CREATE (c:Contact { mobile:csvLine.mobile, name:csvLine.name, updateTime:csvLine.updateTime, createTime:csvLine.createTime })'
        # USING PERIODIC COMMIT 1000,是满足1000条之后，提交一个事务，这样能够提高效率。
        # 导入节点之后，我们必然会导入关系。这里就有个坑，如果你在node节点的库里，没有创建index，那么导入关系的时候，将会慢的要死。
        # 创建索引之前，我们插入的节点数据有可能会有重复的情况，我们需要先清除一下重复数据。
        command='MATCH (n:Contact) WITH　n.mobile AS mobile , collect (n) AS nodes WHERE size(nodes)>1 FOREACH (n in tail(nodes)|DETACH DELETE n)'

        #创建索引
        index1= 'CREATE CONSTRAINT ON (c:Contact) ASSERT c.mobile IS UNIQUE'
        index2= 'CREATE INDEX ON :Contact(mobile)'
        # 删除索引
        drop_index='DROP CONSTRAINT ON (c:HudongItem) ASSERT c.title IS UNIQUE'
        #导入关系csv文件
        rel='USING PERIODIC COMMIT 1000 LOAD CSV WITH HEADERS FROM "file:/rels.csv" AS csvLine MATCH (c:Contact {mobile:csvLine.mobile1}),(c1:Contact {mobile:csvLine.mobile2}) CREATE (c)-[:hasContact]->(c1)'
        
         # 将hudong_pedia.csv 导入
        load='LOAD CSV WITH HEADERS  FROM "file:///hudong_pedia.csv" AS line CREATE (p:HudongItem{title:line.title,image:line.image,detail:line.detail,url:line.url,openTypeList:line.openTypeList,baseInfoKeyList:line.baseInfoKeyList,baseInfoValueList:line.baseInfoValueList})'
        # 创建索引
        create_index='CREATE CONSTRAINT ON (c:HudongItem) ASSERT c.title IS UNIQUE'     
        # 导入hudongItem和新加入节点之间的关系
        q='LOAD CSV  WITH HEADERS FROM "file:///wikidata_relation2.csv" AS line MATCH (entity1:HudongItem{title:line.HudongItem}),(entity2:NewNode{title:line.NewNode}) CREATE (entity1)-[:RELATION {type: line.relation}]->(entity2)'
        
    def py_cql(self,Person,name,age,title,update_time):
        # 创建name唯一性，name是profile_id
        command = f'CREATE CONSTRAINT ON (n:{Person}) ASSERT n.name IS UNIQUE'
        self.graph.run(command)

        # 删除一个项目的全部节点和边
        command= f'MATCH (n:{Person}) DETACH DELETE n'
        # 建节点，原节点没有就会建，属性和属性的值完全一样才会保留原数据
        command = f'MERGE (node:{Person}{name:{name},age:{age},title:{title}}) return node'
        # 删除节点和关联的边
        command= f'MATCH (node:{Person}) WHERE node.update_time< {update_time} DETACH DELETE node'
        return None

    def create_rules(self):
        # 一度关系内有多少个触碰黑名单的
        q='match (p:Person)-[]-(p1:Person)-[h:Has_Phone]-(b:Black) where p.name=="张三" return count(b)'
        # 申请人的二度关系中有多少触碰黑名单
        q='match (p:Person)-[]-(p1:Person)-[]-(p2:Person)-[h:Has_Phone]-(b:Black) where p.name=="张三" return count(b)'

    def find_subgraph_by_entity(self,name):
        #根据实体名称进行查询，考虑方向,返回关系
        command=f'MATCH (p:Person{name:{name}})-[rel]->(p2:Person) return p,k,p2'
        ans=self.graph.run(command).data()
        if (len(ans)==0):
            #查询实体，不考虑其方向
            command=f'MTACH (p:Person)-[rel]-(p2:Person) where p.name={name} return p,rel,p2'
            ans=self.graph.run(command).data()
        return ans

    def find_subgraph_by_entity2(self,name):
        command=f'MATCH　(p:Person)-[rel]-(p1:Person{name:{name}}) return p,rel,p1'
        ans=self.run(command).data()
        if (len(ans)==0):
            command=f'MATCH (p:Student)-[rel]-(p1:Person{name:{name}} return p,rel,p1)'
            ans=self.run(command).data()
        return ans
    
    def find_subgraph_by_rel_entity(self,rel,name):
        command=f'MATCH (p:Person{name:{name}})-[rel:{rel}]-(p1:Person) return p,rel,p1'
        ans=self.run(command).data()
        return ans

    


    
if __name__ == "__main__":
    cypher= CypherExercise()
    cypher.connectionDB()
    cypher.cql_exercise()
