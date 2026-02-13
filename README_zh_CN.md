<div align="center">

<img src="./image/ic.png" width="15%">

# IXGenerator

[![IXGenerator](https://img.shields.io/badge/IX-Generator-blue?style=for-the-badge)](#)
[![License](https://img.shields.io/badge/LICENSE-MIT-brightgreen?style=for-the-badge)](#)

用于生成特定项目所需的 XML 文件的实用程序

[English](README.md) | **&gt; 简体中文 &lt;**
</div>

## 功能说明

该项目用于管理特定的图标包项目的应用图标映射并生成所需的XML配置文件。

### 添加新应用到数据库

**使用方法：**
```bash
python main.py -a
```
该命令从`input`文件夹读取CSV文件，将新应用信息添加到`map/data.csv`中。

### 生成输出文件

**使用方法：**
```bash
python main.py -g
```
该命令从`map/data.csv`读取完整的应用映射数据，生成5个XML配置文件。

`templates`文件夹下的`icon_pack_template.xml`和`theme_resources_template.xml`分别定义了生成的`icon_pack.xml`与`theme_resources.xml`的前半部分内容，您可以根据实际情况自由更改。

### 复制输出文件

**使用方法：**
```bash
python main.py -c
```
或者
```bash
python main.py -c [<目标目录>]
```
该命令将`map/output`下已经生成的5个XML配置文件复制到您的图标包项目目录下，您可以将项目目录写入`config/config.json`的`target_dir`中，这样就无需每次在命令中配置项目目录。

## 格式说明

### 输入CSV格式（input文件夹）
3列，包含表头：
```csv
AppName,PackageName,LauncherActivity
应用名称,包名,启动Activity
```

示例：
```csv
AppName,PackageName,LauncherActivity
Foo,com.app.foo,com.app.foo.MainActivity
Bar,com.app.bar,com.app.bar.BaseActivity
Foobar,com.foobar.app,com.foobar.app.ExmplActivity
```

### 数据CSV格式（map文件夹）
4列，包含表头：
```csv
AppName,PackageName,LauncherActivity,IconName
应用名称,包名,启动Activity,图标名称
```

## 系统需求
Python 3.6+