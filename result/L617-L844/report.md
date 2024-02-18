
# 数据分析报告

## 基础信息

![Table](imgs/table_run_info.png)

<div style="page-break-after: always;"></div>

## 上孔信息

### 20240117_Sync_Y0004_04_H01_Run0002 - 上孔信息

![Table](imgs/table_20240117_Sync_Y0004_04_H01_Run0002_pore_info.png)

### 20240117_Sync_Y0004_04_H01_Run0002 - 上孔信息

![Table](imgs/table_20240117_Sync_Y0004_04_H01_Run0002_pore_info.png)


## 单孔信号良率

<div style="page-break-after: always;"></div>

# 目录

1. [准确率相关统计](#准确率相关统计)  
   1.1 [准确率分布](#准确率分布)  
   1.2 [与读长关系](#与读长关系)  
   1.3 [错误类型统计](#错误类型统计)     
   1.4 [准确率差异分析](#准确率差异分析)
2. [读长相关统计](#读长相关统计)
3. [速度相关统计](#速度相关统计)
4. [AR相关统计](#AR相关统计)  
   4.1 [与Block Rate的关系](#与Block-Rate的关系)  
   4.2 [AR分布](#AR分布)
5. [DW相关统计](#DW相关统计)  
   5.1 [与Block Rate的关系](#与Block-Rate的关系)  
   5.2 [DW分布](#DW分布)  
6. [Capture Rate相关统计](#Capture-Rate相关统计)  
   6.1 [与Block Rate的关系](#与Block-Rate的关系-1)  
   6.2 [CR分布](#CR分布)
7. [Pore-LT与Basecall-LT相关统计](#Pore-LT与Basecall-LT相关统计)

<div style="page-break-after: always;"></div>

## 1. 准确率相关统计

### 1.1 准确率分布

<div style="text-align: center;">
Fig 1-1-1 准确率分布直方图
</div>

![Fig 1-1-1](imgs/proportion_identity.png)

### 1.2 与读长关系 

<div style="page-break-after: always;"></div>

<div style="text-align: center;">
L617 - Read len与Identity相关性散点图
</div>  

![Fig 1-2-1](imgs/correlation_read_len_and_identity_L617.png)

<div style="text-align: center;">
L844 - Read len与Identity相关性散点图
</div>  

![Fig 1-2-1](imgs/correlation_read_len_and_identity_L844.png)

### 1.3 错误类型统计


<div style="text-align: center;">
L617 - 错误类型统计汇总表
</div>

![Table 1-3-1](imgs/table_error_type_statistics_L617.png)


<div style="text-align: center;">
L844 - 错误类型统计汇总表
</div>

![Table 1-3-1](imgs/table_error_type_statistics_L844.png)

<div style="page-break-after: always;"></div>

<div style="text-align: center;">
L617 - 错误类型统计汇总图
</div>

![Fig 1-3-3](imgs/error_type_statistics_L617.png)


<div style="text-align: center;">
L844 - 错误类型统计汇总图
</div>

![Fig 1-3-3](imgs/error_type_statistics_L844.png)


<div style="text-align: center;">
Fig 1-3-1 总-错误类型统计
</div>

![Fig 1-3-1](imgs/total_error_type.png)

<div style="text-align: center;">
Fig 1-3-2 四种碱基-总错误统计
</div>

![Fig 1-3-2](imgs/4_base_error_type.png) 

### 1.4 准确率差异分析

#### 1.4.1 单因素方差分析

<div style="text-align: center;">
Table1-4-1 单因素方差分析统计表
</div>

![Fig 1-4-1](imgs/ANOVA.png)

#### 1.4.2 秩和检验

<div style="text-align: center;">
Table1-4-2秩和检验统计表
</div>

![Fig 1-4-2](imgs/rank-sum.png)

<div style="page-break-after: always;"></div>

## 2. 读长相关统计

<div style="text-align: center;">
Fig 2-1 信号LT>60min 读长分布占比图
</div>

![Fig 2-1](imgs/proportion_read_len.png)

<div style="page-break-after: always;"></div>

## 3. 速度相关统计

<div style="text-align: center;">
Fig 3-1 信号LT>60min 速度分布占比图
</div>

![Fig 2-1](imgs/proportion_speed.png)

<div style="page-break-after: always;"></div>

## 4. AR相关统计

### 4.1 与Block Rate的关系


<div style="text-align: center;">
L617 - AR与BR相关性散点图
</div>

![Fig 4-1-1](imgs/correlation_AR_and_BR_L617.png)


<div style="text-align: center;">
L844 - AR与BR相关性散点图
</div>

![Fig 4-1-1](imgs/correlation_AR_and_BR_L844.png)


### 4.2 AR分布

<div style="text-align: center;">
Fig 4-2-1 AR分布条形图
</div>

![Fig 4-2-1](imgs/AR_prop.png)

<div style="page-break-after: always;"></div>

<div style="text-align: center;">
L617 四种碱基AR占比图
</div>

![Fig 4-2-2](imgs/4_Base_AR_L617.png)


<div style="text-align: center;">
L844 四种碱基AR占比图
</div>

![Fig 4-2-2](imgs/4_Base_AR_L844.png)

<div style="page-break-after: always;"></div>

## 5. DW相关统计

### 5.1 与Block Rate的关系

<div style="text-align: center;">
L617 - DW与BR相关性散点图
</div>

![Fig 5-1-1](imgs/correlation_DW_and_BR_L617.png)


<div style="text-align: center;">
L844 - DW与BR相关性散点图
</div>

![Fig 5-1-1](imgs/correlation_DW_and_BR_L844.png)


### 5.2 DW分布

<div style="text-align: center;">
Fig 5-2-1 DW分布条形图
</div>

![Fig 5-2-1](imgs/DW_prop.png)

<div style="page-break-after: always;"></div>

<div style="text-align: center;">
L617 - 四种碱基DW占比图
</div>

![Fig 5-2-2](imgs/4_Base_DW_L617.png)


<div style="text-align: center;">
L844 - 四种碱基DW占比图
</div>

![Fig 5-2-2](imgs/4_Base_DW_L844.png)

<div style="page-break-after: always;"></div>

## 6. Capture Rate相关统计

### 6.1 与Block Rate的关系


<div style="text-align: center;">
L617 - CR与BR相关性散点图
</div>

![Fig 6-1-1](imgs/correlation_CR_and_BR_L617.png)


<div style="text-align: center;">
L844 - CR与BR相关性散点图
</div>

![Fig 6-1-1](imgs/correlation_CR_and_BR_L844.png)


### 6.2 CR分布

<div style="text-align: center;">
Fig 6-2-1 CR分布条形图
</div>

![Fig 6-2-1](imgs/CR_prop.png)

<div style="page-break-after: always;"></div>

<div style="text-align: center;">
L617 - 四种碱基CR占比图
</div>

![Fig 6-2-2](imgs/4_Base_CR_L617.png)


<div style="text-align: center;">
L844 - 四种碱基CR占比图
</div>

![Fig 6-2-2](imgs/4_Base_CR_L844.png)

<div style="page-break-after: always;"></div>

## 7. Pore-LT与Basecall-LT相关统计

<div style="text-align: center;">
L617 Pore-LT与Basecall-LT占比图
</div>

![Fig 7-1-1](imgs/Pore_LT-Basecall_LT_L617.png)
    
<div style="text-align: center;">
L844 Pore-LT与Basecall-LT占比图
</div>

![Fig 7-1-1](imgs/Pore_LT-Basecall_LT_L844.png)
    