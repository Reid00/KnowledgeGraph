# Nebula Graph Learning Notes

## 介绍
Nebula Graph是一款开源的、分布式的、易扩展的原生图数据库，能够承载数十亿个点和数万亿条边的超大规模数据集，并且提供毫秒级查询。
>official site: https://docs.nebula-graph.com.cn/2.0.1/

## 架构
Nebula Graph由三种服务构成：Graph服务、Meta服务和Storage服务。
每个服务都有可执行的二进制文件和对应进程，您可以使用这些二进制文件在一个或多个计算机上部署Nebula Graph集群。
下图展示了Nebula Graph集群的经典架构。
![Nebula架构](https://raw.githubusercontent.com/Reid00/image-host/main/20210507/nebula_architecture.png)

### Meta服务简介
在Nebula Graph架构中，Meta服务是由nebula-metad进程提供的，负责数据管理，例如Schema操作、集群管理和用户权限管理等。
### Graph服务和Storage服务简介
Nebula Graph采用计算存储分离架构。Graph服务负责处理计算请求，Storage服务负责存储数据。它们由不同的进程提供，Graph服务是由nebula-graphd进程提供，Storage服务是由nebula-storaged进程提供。计算存储分离架构的优势如下：
- 易扩展
   分布式架构保证了Graph服务和Storage服务的灵活性，方便扩容和缩容。
- 高可用
   如果提供Graph服务的服务器有一部分出现故障，其余服务器可以继续为客户端提供服务，而且Storage服务存储的数据不会丢失。服务恢复速度较快，甚至能做到用户无感知。
- 节约成本
   计算存储分离架构能够提高资源利用率，而且可根据业务需求灵活控制成本。如果使用Nebula Graph Cloud，可以进一步节约成本。
- 开放更多可能性
   基于分离架构的特性，Graph服务可以在多种存储引擎上单独运行，Storage服务也可以为多种计算引擎提供服务。
### Meta服务
<https://docs.nebula-graph.com.cn/2.0/1.introduction/3.nebula-graph-architecture/2.meta-service/>
### Graph服务
<https://nebula-graph.io/posts/nebula-query-engine-introduction/>
<https://docs.nebula-graph.com.cn/manual-CN/1.overview/3.design-and-architecture/3.query-engine/>
### Storage服务
<https://nebula-graph.io/posts/nebula-graph-storage-engine-overview/>
<https://docs.nebula-graph.com.cn/manual-CN/1.overview/3.design-and-architecture/2.storage-design/>

## 部署
Github download rpm
><https://github.com/vesoft-inc/nebula-graph/releases>
   
安装rpm 包
```shell
sudo rpm -ivh --prefix=<installation_path> <package_name>
# --prefix 制定安装路径，默认 /usr/local/nebula
```

## 图建模
### 以性能为目标进行建模
目前Nebula Graph没有完美的建模方法，如何建模取决于您想从数据中挖掘的内容。分析数据并根据业务模型创建方便直观的数据模型，测试模型并优化，逐渐适应业务。为了更好的性能，您可以多次更改或重新设计模型。
### 合理设置边属性
- 深度图遍历的性能较低，为了减少遍历深度，请使用点属性代替边。例如，模型a包括姓名、年龄、眼睛颜色三种属性，建议您创建一个标签person，然后为它添加姓名、年龄、眼睛颜色的属性。如果创建一个包含眼睛颜色的标签和一个边类型has，然后创建一个边用来表示人拥有的眼睛颜色，这种建模方法会降低遍历性能。
- 为边创建属性时请勿使用长字符串，Nebula Graph支持在边上存储长字符串属性，但是这些属性会同时保存在出边和入边，请小心写入放大(write amplification)
### 合理设置标签属性
图建模中，请将一组类似的平级属性放入同一个标签，即按不同概念进行分组。
### 正确使用索引
正确使用索引可以加速查询，但是索引会导致写性能下降90%甚至更多，只有在根据点或边的属性定位点或边时才使用索引。
> 注意：请不要随意在生产环境中使用索引，除非您很清楚使用索引对业务的影响。
## 语法
- leader 分布不平衡
   ```shell
   # 若发现机器都已在线 (online)，但 Leader distribution 分布不均(如上)，则可以通过命令 (BALANCE LEADER) 来触发 partition 重分布：
   balance leader
   ```
- create player tag
  ```shell
  create tag palyer(name string, age int)
  ```
- edge property
   ![edge properry](https://raw.githubusercontent.com/Reid00/image-host/main/20210507/Nebula_0.png)
   
