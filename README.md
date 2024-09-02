# WebsocketSSH
提供webSSH服务，可以实现，内网穿透的SSH，通过web前端界面，可以ssh访问内网的主机


* 运行步骤：
   1. 后端python文件，python3可运行：注意修改监听端口：默认 9900 （0.0.0.0 ip为可访问ip不改）；注意修改后端的User和pwd，不然ssh连不上机器。
   2. 前端html文件，浏览器打开，注意修改html文件端口和IP地址：默认 localhost:9900
   3. ①点击前端运行websocket，第二部在输入框中输入"[first-start-connection#@1]10.0.21.52"，后面的ip地址为你需要连接ssh主机ip，账号密码，后端设置
   4. ②在第一次输入"[first-start-connection#@1]10.0.21.52"之后，就可以直接ls，cd，等命令了
