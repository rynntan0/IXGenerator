<div align="center">

<img src="./image/ic.png" width="15%">

# IXGenerator

[![IXGenerator](https://img.shields.io/badge/IX-Generator-blue?style=for-the-badge)](#)
[![License](https://img.shields.io/badge/LICENSE-MIT-brightgreen?style=for-the-badge)](#)

A utility for generating XML files required by specific projects.

**&gt; English &lt;** | [简体中文](README_zh_CN.md)
</div>

## Features

This project is used to manage app icon mappings for specific icon pack projects and generate the required XML configuration files.

### Add New Apps to Database

**Usage:**
```bash
python main.py -a
```
This command reads a CSV file from the `input` folder and appends new app information to `map/data.csv`.

### Generate Output Files

**Usage:**
```bash
python main.py -g
```
This command reads the complete app mapping data from `map/data.csv` and generates 5 XML configuration files.

The `icon_pack_template.xml` and `theme_resources_template.xml` files in the templates folder define the first half of the generated `icon_pack.xml` and `theme_resources.xml` respectively. You can modify them as needed.

### Copy Output Files

**Usage:**
```bash
python main.py -c
```
or
```bash
python main.py -c [<target directory>]
```
This command copies the 5 generated XML files from `map/output` to your icon pack project directory. You can specify the project directory in `target_dir` inside `config/config.json` to avoid entering it every time.

## Format Specifications

### Input CSV Format (input folder)
3 columns, with headers:
```csv
AppName,PackageName,LauncherActivity
Application Name,Package Name,Launcher Activity
```

Example:
```csv
AppName,PackageName,LauncherActivity
Foo,com.app.foo,com.app.foo.MainActivity
Bar,com.app.bar,com.app.bar.BaseActivity
Foobar,com.foobar.app,com.foobar.app.ExmplActivity
```

### Data CSV Format (map folder)
4 columns, with headers:
```csv
AppName,PackageName,LauncherActivity,IconName
Application Name,Package Name,Launcher Activity,Icon Name
```

## System Requirements
Python 3.6+