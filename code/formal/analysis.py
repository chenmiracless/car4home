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