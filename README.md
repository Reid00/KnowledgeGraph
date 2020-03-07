# KnowledgeGraph
KowledgeGraph test



### 1. 使用load csv导入数据

1. 导入CSV 节点 （detail see the code）
2. 创建索引并删除重复节点
3. 导入关系csv文件

### 2. 使用neo4j-admin导入数据

通过neo4j-admin方式导入的话，需要暂停服务，并且需要清除graph.db,这样才能导入进去数据。而且，只能在初始化数据时，导入一次之后，就不能再次导入了。所以这种方式，可以在初次建库的时候，导入大批量数据，等以后如果还需要导入数据时，可以采用上边的方法。

1. #### 数据导入前的准备工作

   对于大规模的数据集，使用语句插入和load csv的时候往往非常缓慢，当需要插入大量三元组时，可以考虑使用Neo4j-import的方式。这种方式有许多**注意点**：

   1、传入文件名的时候务必使用绝对路径。
   2、在执行指令之前务必保证Neo4j处于关闭状态，如果不确定可以在Neo4j根目录下运行./bin/neo4j status 查看当前状态。
   3、使用neo4j-admin import指令导入之前先将原数据库从neo4j_home/data/databases/graph.db／中移除。
   4、写CSV文件的时候务必确保所有的节点的CSV文件的ID fileds的值都唯一、不重复。并且确保所有的边的CSV文件的START_ID 和 END_ID都包含在节点CSV文件中。

2. #### 数据预处理

   neo4j-import官方要求的数据格式为csv文件，主要就是分成两个文件entity.csv 和relationship.csv。

   其中entity.csv中包含了实体的id，实体的name，以及标签LABEL，具体格式如下：

   ```
   entity:ID,name,:LABEL
   e0,GDP,my_entity
   e1,PHP,my_entity
   e2,李冲,my_entity
   e3,perimenopausal syndrome,my_entity
   e4,雁荡山景区分散，东起羊角洞，西至锯板岭；南起筋竹溪，北至六坪山。,my_entity
   e5,词条（拼音：cí tiáo）也叫词目，是辞书学用语，指收列的词语及其释文。,my_entity
   e6,芦苇茂密，结草为荡,my_entity
   e7,面粉，水，酵母，苏打,my_entity
   e8,先注册先得的原则,my_entity
   e9,解压缩软件,my_entity
   e10,华硕电脑股份有限公司,my_entity
   ```

   relationship.csv文件包含了起始节点id，结束节点id，关系的name，以及标签LABEL，具体格式如下：

   ```
   :START_ID,:END_ID,name,:TYPE
   e48,e799,属性,属性
   e191,e479,描述,描述
   e641,e5,描述,描述
   e641,e182,标签,标签
   e237,e575,描述,描述
   e237,e237,中文名,中文名
   e237,e533,是否含防腐剂,是否含防腐剂
   e237,e264,主要食用功效,主要食用功效
   e237,e405,适宜人群,适宜人群
   ```

   需要将导入的数据转换成这样的两个格式的csv文件，才能够导入Neo4j中。

3. #### 数据导入

   csv数据文件准备好后，可以通过执行以下脚本来实现数据导入：

   ```#导入命令
   
   #导入命令
   # 停止neo4j服务
   neo4j stop 
   # 如果是Linux可以进入到databases目录下删除数据库，windows直接删除即可
   cd /usr/local/Cellar/neo4j/3.5.0/libexec/data/databases
   rm -rf graph.db
   # 执行数据导入命令neo4j-admin
   neo4j-admin import \
   --database=graph.db
   --nodes:phone="../phone_header.csv,phones.csv \
   --ignore-duplicate-nodes=true \
   --ignore-missing-nodes=true \
   --relationships:call="../call_header.csv,call.csv"
   # 重启neo4j服务
   neo4j start
   ```