import os


def generate_single_run_md_file(label, PN, run_name):
    single_run_markdown_content = f''' 

# 数据分析报告

## 基础信息

![Table 0-1](imgs/table_{run_name}_run_info.png)

<div style="page-break-after: always;"></div>

## 上孔信息

![Table 0-2](imgs/table_{run_name}_pore_info.png)

## 单孔信号良率

<div style="page-break-after: always;"></div>

# 目录

1. [准确率相关统计](#准确率相关统计)  
   1.1 [准确率分布](#准确率分布)  
   1.2 [与读长关系](#与读长关系)  
   1.3 [错误类型统计](#错误类型统计)  
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

![Fig 1-1-1](imgs/proportion_identity_{PN}.png)

### 1.2 与读长关系 

<div style="text-align: center;">
Fig 1-2-1 Read len与Identity相关性散点图
</div>

![Fig 1-2-1](imgs/correlation_read_len_and_identity_{PN}.png)

### 1.3 错误类型统计

<div style="text-align: center;">
Table 1-3-1 错误类型统计汇总表
</div>

![Table 1-3-1](imgs/table_error_type_statistics_{PN}.png)

<div style="text-align: center;">
Fig 1-3-3 错误类型统计汇总图
</div>

![Fig 1-3-3](imgs/error_type_statistics_{PN}.png)

<div style="text-align: center;">
Fig 1-3-1 总-错误类型统计
</div>

![Fig 1-3-1](imgs/total_error_type_{PN}.png)
 
<div style="text-align: center;">
Fig 1-3-2 四种碱基-总错误统计
</div>

![Fig 1-3-2](imgs/4_base_error_type_{PN}.png)

## 2. 读长相关统计

<div style="text-align: center;">
Fig 2-1 信号LT>60min 读长分布占比图
</div>

![Fig 2-1](imgs/proportion_read_len_{PN}.png)

## 3. 速度相关统计

<div style="text-align: center;">
Fig 3-1 信号LT>60min 速度分布占比图
</div>

![Fig 2-1](imgs/proportion_speed_{PN}.png)


## 4. AR相关统计

### 4.1 与Block Rate的关系

<div style="text-align: center;">
Fig 4-1-1 AR与BR相关性散点图
</div>

![Fig 4-1-1](imgs/correlation_AR_and_BR_{PN}.png)

### 4.2 AR分布

<div style="text-align: center;">
Fig 4-2-1 AR分布条形图
</div>

![Fig 4-2-1](imgs/AR_prop_{PN}.png)

<div style="text-align: center;">
Fig 4-2-2 四种碱基AR占比图
</div>

![Fig 4-2-2](imgs/4_Base_AR_{PN}.png)

## 5. DW相关统计

### 5.1 与Block Rate的关系

<div style="text-align: center;">
Fig 5-1-1 DW与BR相关性散点图
</div>

![Fig 5-1-1](imgs/correlation_DW_and_BR_{PN}.png)

### 5.2 DW分布

<div style="text-align: center;">
Fig 5-2-1 DW分布条形图
</div>

![Fig 5-2-1](imgs/DW_prop_{PN}.png)

<div style="text-align: center;">
Fig 5-2-2 四种碱基DW占比图
</div>

![Fig 5-2-2](imgs/4_Base_DW_{PN}.png)

## 6. Capture Rate相关统计

### 6.1 与Block Rate的关系

<div style="text-align: center;">
Fig 6-1-1 CR与BR相关性散点图
</div>

![Fig 6-1-1](imgs/correlation_CR_and_BR_{PN}.png)

### 6.2 CR分布

<div style="text-align: center;">
Fig 6-2-1 CR分布条形图
</div>

![Fig 6-2-1](imgs/CR_prop_{PN}.png)

<div style="text-align: center;">
Fig 6-2-2 四种碱基CR占比图
</div>

![Fig 6-2-2](imgs/4_Base_CR_{PN}.png)

## 7. Pore-LT与Basecall-LT相关统计

<div style="text-align: center;">
Fig 7-1 Pore-LT与Basecall-LT占比图
</div>

![Fig 7-1-1](imgs/Pore_LT-Basecall_LT_{PN}.png)
    '''

    file_path = f'result/{label}/report_{PN}.md'
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(single_run_markdown_content)


def generate_multiple_run_md_file(run_name_list, PN_list, label):
    markdown_content = f'''
# 数据分析报告

## 基础信息

![Table](imgs/table_run_info.png)

<div style="page-break-after: always;"></div>

## 上孔信息

'''
    for run_name in run_name_list:
        markdown_content += f'''
### {run_name} - 上孔信息

![Table](imgs/table_{run_name}_pore_info.png)

'''

    markdown_content += f'''
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

'''
    for PN in PN_list:
        markdown_content += f'''
<div style="text-align: center;">
{PN} - Read len与Identity相关性散点图
</div>  

![Fig 1-2-1](imgs/correlation_read_len_and_identity_{PN}.png)
'''

    markdown_content += f'''
### 1.3 错误类型统计

'''
    for PN in PN_list:
        markdown_content += f'''
<div style="text-align: center;">
{PN} - 错误类型统计汇总表
</div>

![Table 1-3-1](imgs/table_error_type_statistics_{PN}.png)

'''
    for PN in PN_list:
        markdown_content += f'''
<div style="text-align: center;">
{PN} - 错误类型统计汇总图
</div>

![Fig 1-3-3](imgs/error_type_statistics_{PN}.png)

'''
    markdown_content += f'''
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

## 2. 读长相关统计

<div style="text-align: center;">
Fig 2-1 信号LT>60min 读长分布占比图
</div>

![Fig 2-1](imgs/proportion_read_len.png)

## 3. 速度相关统计

<div style="text-align: center;">
Fig 3-1 信号LT>60min 速度分布占比图
</div>

![Fig 2-1](imgs/proportion_speed.png)

## 4. AR相关统计

### 4.1 与Block Rate的关系

'''
    for PN in PN_list:
        markdown_content += f'''
<div style="text-align: center;">
{PN} - AR与BR相关性散点图
</div>

![Fig 4-1-1](imgs/correlation_AR_and_BR_{PN}.png)

'''
    markdown_content += f'''
### 4.2 AR分布

<div style="text-align: center;">
Fig 4-2-1 AR分布条形图
</div>

![Fig 4-2-1](imgs/AR_prop.png)

'''
    for PN in PN_list:
        markdown_content += f'''
<div style="text-align: center;">
{PN} 四种碱基AR占比图
</div>

![Fig 4-2-2](imgs/4_Base_AR_{PN}.png)

'''
    markdown_content += f'''
## 5. DW相关统计

### 5.1 与Block Rate的关系
'''
    for PN in PN_list:
        markdown_content += f'''
<div style="text-align: center;">
{PN} - DW与BR相关性散点图
</div>

![Fig 5-1-1](imgs/correlation_DW_and_BR_{PN}.png)

'''
    markdown_content += f'''
### 5.2 DW分布

<div style="text-align: center;">
Fig 5-2-1 DW分布条形图
</div>

![Fig 5-2-1](imgs/DW_prop.png)

'''
    for PN in PN_list:
        markdown_content += f'''
<div style="text-align: center;">
{PN} - 四种碱基DW占比图
</div>

![Fig 5-2-2](imgs/4_Base_DW_{PN}.png)

'''
    markdown_content += f'''
## 6. Capture Rate相关统计

### 6.1 与Block Rate的关系

'''
    for PN in PN_list:
        markdown_content += f'''
<div style="text-align: center;">
{PN} - CR与BR相关性散点图
</div>

![Fig 6-1-1](imgs/correlation_CR_and_BR_{PN}.png)

'''
    markdown_content += f'''
### 6.2 CR分布

<div style="text-align: center;">
Fig 6-2-1 CR分布条形图
</div>

![Fig 6-2-1](imgs/CR_prop.png)

'''
    for PN in PN_list:
        markdown_content += f'''
<div style="text-align: center;">
{PN} - 四种碱基CR占比图
</div>

![Fig 6-2-2](imgs/4_Base_CR_{PN}.png)

'''
    markdown_content += f'''
## 7. Pore-LT与Basecall-LT相关统计

'''
    for PN in PN_list:
        markdown_content += f'''
<div style="text-align: center;">
{PN} Pore-LT与Basecall-LT占比图
</div>

![Fig 7-1-1](imgs/Pore_LT-Basecall_LT_{PN}.png)
    '''

    file_path = f'result/{label}/report.md'
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(markdown_content)



