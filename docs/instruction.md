# 开发手册

## 运行方式

先在 `src\config.py` 中修改配置信息（mysql信息，api_key等等），然后

```sh
conda env create -f ChatOBE.yml  # 创建环境
conda activate ChatOBE  # 激活环境

python .\src\app.py  # 运行项目
```

应该看到输出：

```sh
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: xxx
```

有上述输出后，在浏览器中打开 http://127.0.0.1:5000 即可。

## 文件结构

```sh
ChatOBE
│  .gitignore  
│  ChatOBE.yml  # 环境配置文件
│  README.md  
│  
├─docs
│      instruction.md  # 本文件
│      requirements.md  # 大作业要求
│      TODOs.md  # 待办
│
├─images  # 图片
|
└─src  # 代码
    │  app.py  # 程序入口
    │  ChatOBE.py  # ChatOBE主体，各种功能写在这里（ChatOBE类中）
    │  config.py  # 配置信息
    │  utils.py  # 辅助方法写在这里面
    │
    ├─static  # 前端
    │      style.css
    │
    └─templates  # 前端
           index.html
```

## 相关资料

- [git、GitHub教程（基本操作+提交pr）](https://blog.csdn.net/qq_39350172/article/details/125322895)
- [MySQL 教程 | 菜鸟教程](https://www.runoob.com/mysql/mysql-tutorial.html)
- [Python中pymysql模块详解：安装、连接、执行SQL语句等常见操作-CSDN博客](https://blog.csdn.net/qq_43341612/article/details/132113053)