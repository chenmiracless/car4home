https://hexo-1253211031.cos.ap-chengdu.myqcloud.com/img/0184e15544d2a40000019ae9936cc4.jpg
那么今天我们主要是讲关于手机app抓包，来获取某个app的一些数据。道理其实很简单，就是通过抓包工具来截获发送到手机的数据。
## 1、准备工作
   准备抓包工具（fiddler),一步可以连接WiFi的手机。
   
   在这里，我以‘汽车之家’app为例，抓取2020年1月汽车销售量排行
   
   ![](https://hexo-1253211031.cos.ap-chengdu.myqcloud.com/img/5178a7ca7f6d7f2716ececc132e5a9b.png)
   
   准备工作完成后，我们开始抓包，至于fiddler的配置以及用法，可以自行百度，很简单
   打开我们的fiddler

## 2、抓包及数据分析
### 1)数据抓取
开始抓包后，我们可以看到如下

![fiddler界面](https://hexo-1253211031.cos.ap-chengdu.myqcloud.com/img/clipboard_20200317100352.png)

由于一般app数据包都是以json文件格式的文档发送过来的，所以，我首先想到了看一下json里面的内容，我们可以左击选择copy--> just URL
我们在把url粘贴到浏览器，查看一下，可以看到都是字符串，无法分辨，我们再用在线json解析查看一下

![json源文件](https://hexo-1253211031.cos.ap-chengdu.myqcloud.com/img/clipboard_20200317100854.png)

解析之后，我们可以看到，正式我们想要的数据

![解析后的数据](https://hexo-1253211031.cos.ap-chengdu.myqcloud.com/img/clipboard_20200317101136.png)

接着，直接写出获取源文件的代码
```
    f = open(file_json,'w',encoding = 'utf-8')
    r = urllib.request.urlopen(url)
    j = r.read().decode('utf-8')
    print(type(j))
    f.write(j)
    f.close()
``` 
### 2)数据解析与转换
在得到我们想要的数据之后，我们开始将json中我们需要的数据提取出来，在提取数据过程中，我碰到了点问题，本来想通过python的第三方json库直接解析，答案是你hi发现没那么简单，我们可以来看一下数据结构

![](https://hexo-1253211031.cos.ap-chengdu.myqcloud.com/img/clipboard_20200317103218.png)

我们可以看到，json的目录很清晰，我们需要的内容在键为"list"里面，它所对应的是一个值是一个列表,而每款车又对应一个字典，所以很是头疼。我是这样解决的：

```
	namelist = []
    numlist = []
    with open(json_file,'r',encoding='utf-8') as f:
        jsons = json.loads(f.read())
        List = jsons["result"]['list']
        #print(type(List))
        #print(List)
        fs = open(txt_file,'w',encoding = 'utf-8')
        for i in List:
            namelist.append(i['seriesname'])
            numlist.append(i['righttitle'])
        for r,s in zip(namelist,numlist):
            pat = r.replace(' ', '') + ' ' + s + '\n'
            fs.write(pat)
        fs.close()
```

首先先建立两个列表，分别存储汽车名和汽车销量`r.replace(' ', '') `这句意思是，将有些汽车名里面的空格删去，因为接下来我们将数据写入excle时，会根据txt文件中的空格来区分不同的列，完成后的txt文档如下格式

![](https://hexo-1253211031.cos.ap-chengdu.myqcloud.com/img/clipboard_20200317012006.png)


### 数据存储
我们最终要的时excle文档，所以我们还需将data.txt中的数据写入excle文件，你可以用pandas也可以用其他的包。我这里使用的是openpyxl，如下：

```
def readTxt(file):
    ls = list()
    with open(file, 'r', encoding='utf-8-sig') as f:
        for line in f.readlines():
            # 异常处理机制
            try:
                index1 = line.index(' ')
                index2 = line.index('\n')
                car_name = line[:index1]
                sale = line[index1 + 1:index2]

                ls.append((car_name, sale))  # 以元组的形式追加进空列表
            except:
                print('wrong format!')
    # 返回一个列表
    return ls

# 数据写入函数（写入excle表格)
def write_excel_xlsx1(path, sheet_name, value):
    index = len(value)  # 列表中所含元组的个数，从而确定写入Excel的行数
    # 打开Excel
    wb = load_workbook(path)
    # 创建工作簿
    sheet = wb.create_sheet(sheet_name)
    # 设置格式(列宽)
    sheet.column_dimensions['A'].width = 15
    sheet.column_dimensions['B'].width = 15
    # 按行加入
    for i in range(index):
        sheet.append(value[i])
    # 保存文件
    wb.save(path)
    print("**********数据写入成功**********")
```

![](https://hexo-1253211031.cos.ap-chengdu.myqcloud.com/img/clipboard_20200317012646.png)

*记得将第二列的数据转换成数字格式，因为之前写入的都是字符串格式，接下来做数据分析需要数字格式*


### 数据分析
使用第三方包pyecharts来制作bar图，至于pyecharts导包错误的可以看我之前的教程 <a href="http://chenpengfei.club/pyecharts.html" target="_blank" rel="noopener">关于 pyecharts.charts import Bar 报错解决方案（最新）</a>

```
import xlrd
from pyecharts.charts.bar import Bar
#读取表格
data=xlrd.open_workbook("data.xlsx")
#获取表格的sheets
table=data.sheets()[0]
#输出行数量
print(table.nrows)#8
#输出列数量
print(table.ncols)#4
#获取第一行数据
row1data=table.row_values(0)
print(row1data)#['列1', '列2', '列3', '列4']
print(row1data[0])#列1
xdata=[]
ydata=[]
for i in range(1,table.nrows):
    print(table.row_values(i))
    xdata.append(table.row_values(i)[0])
    ydata.append(table.row_values(i)[1])
print(xdata)
print(ydata)
bar=Bar()
bar.add("销量",xdata,ydata)
bar.render("show.html")
```
*记得将data.xlsx中的空sheet删掉，只要Sales这个sheet，不然会报错*

![](https://hexo-1253211031.cos.ap-chengdu.myqcloud.com/img/clipboard_20200317013422.png)
