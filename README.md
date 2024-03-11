# 现场快递柜状态采集与控制系统

> 设计实现一个对现场快递柜状态数据采集、显示、参数设置、抽屉打开、保鲜控制等功能软件系统

## 实现功能

+ 对快递柜控制板状态数据的采集与显示，包括当前温度、控制温度、控制状态、10 个抽屉的开关状态；
+ 开关指定抽屉、启停温度控制（压缩机制冷控制）、设置控制温度、以及设置系统参数；
+ 依据控制温度和压缩机的启停控制，对快递柜控制板温度进行控制，控制精度为1度；
+ 以曲线方式显示1小时内的当前温度和设定温度的变化趋势。

## 实现方案

+ 与快递柜仿真软件通信
  + 安装python的pyserial库，调用其serial.Serial()函数，绑定COM2串口，发送命令进行连通性测试。
+ 状态采集
  + 依据文档，从上传的数据帧中去除固定的字节，提取功能号和数据的十六进制数字，进行对应的转化处理。
  + 其中采集锁状态时，由于2个字节对应的锁编号不一，因此采取将两个字节对应两个列表，分别判断对应位是否为1并加入到排序好的列表中。
  + 其他状态的采集按照文档的要求转化处理即可。
+ 功能设置
  + 可靠传输的实现分为两个部分。第一部分是将帧去头去尾去CRC校验位，利用函数计算并加入帧中。第二部分是发送完每一个命令之后立即进入校验阶段，提取到ack之后进入CRC校验。如果通过，则GUI提示已成功。如果3s内校验不通过，则再次发送之前的命令，直到回传的命令ack校验正确。
  + 抽屉控制是将需要控制的抽屉编号加入列表，传参到对应函数。函数经过提取，将列表中出现的抽屉对应位置1，以此类推转化为对应的二进制数字，再转化为十六进制，加入到对应命令帧的数据位，CRC填充完发送。
  + 启停压缩机时，根据之前的数据分析结果，利用数据位的00和01进行启停。启动压缩机需要考虑和温度偏差范围的配合。高于则停止，低于则运行。
+ 参数设置
  + 包括温度，温度偏差，设备地址，压缩机预启动时间等。处理方法类似。将输入的十进制数字转化为十六进制，加入到对应命令帧的数据位，CRC填充完发送。

## 结果展示

+ 主界面包括当前温度，设定温度，工作状态，抽屉，温度曲线图的显示和打开抽屉，启停温度控制，设置控制温度，设置系统参数的按钮。点击启停温度控制后，所有的数据都是通过后端回传并实时显示的。

![](https://raw.githubusercontent.com/zappen-cs/myBlogResource/etc/image图片1.png)

+ 如果未连接控制板，也会有对应的警告提示。

![](https://raw.githubusercontent.com/zappen-cs/myBlogResource/etc/image20240311111132.png)

+ 抽屉打开界面，通过遍历复选框得到一个列表，将列表传入后端对应的函数中。

![](https://raw.githubusercontent.com/zappen-cs/myBlogResource/etc/image20240311111309.png)

+ 设定控制温度通过滑块控制，这样就减少了手动输入的麻烦。系统参数设置可以手动输入也可以利用上下箭头控制。

![](https://raw.githubusercontent.com/zappen-cs/myBlogResource/etc/image20240311111341.png)

![](https://raw.githubusercontent.com/zappen-cs/myBlogResource/etc/image20240311111351.png)

+ 控制台会打印当前程序的运行状态，行为状态，ack帧，上传状态帧，crc校验结果和重发命令的提示，方便用户实时查看程序的运行状态。

![](https://raw.githubusercontent.com/zappen-cs/myBlogResource/etc/image20240311111423.png)