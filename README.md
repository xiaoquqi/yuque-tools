# 语雀常用工具

本项目中主要存放用于将语雀迁移走的实用工具和方法。

## 语雀图片下载工具

### 使用场景

从语雀导出Markdown格式后，图片仍然存储于语雀的图床中，如果导入其他工具中无法直接使用，需要将图像下载到本地，方便导入其他软件时使用。

同时为了方便其他工具识别，自动为语雀Markdown添加必要的空行。

### 使用流程

#### 1. 语雀文档下载(无Token)

推荐使用 [ytool工具下载语雀文档](https://github.com/vannvan/yuque-tools/blob/main/packages/yuque-tools-cli/README.md#%E4%BD%BF%E7%94%A8%E6%96%B9%E5%BC%8F)

#### 2. 安装本工具

```
pip install https://github.com/xiaoquqi/yuque-tools
```

#### 3. 使用本工具自动下载图片到本地目录

```
usage: yuque-images-downloader [-h] [-d] [-v] [-p MARKDOWN_DIR] [-i IMAGE_DOWNLOAD_DIR] [-b]

Yuque images downlaoder.

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Enable debug message.
  -v, --verbose         Show message in standard output.
  -p MARKDOWN_DIR, --markdown-dir MARKDOWN_DIR
                        用于存放语雀Markdown的目录，默认情况下将会遍历所有子目录中的markdown文件进行替换
  -i IMAGE_DOWNLOAD_DIR, --image-download-dir IMAGE_DOWNLOAD_DIR
                        图像存放路径，默认为markdown文件同级目录下的_images，可以通过该参数指定
  -b, --backup          是否对文档目录进行备份
```

例如：

```
yuque-images-downloader -p docs -b
```

## Markdown格式化工具

### 使用场景

从语雀导出Markdown格式后，存在不换行问题，例如标题和段落、段落和段落之间没有空行的情况，所以提供了一个专门用于格式化的工具对导出的Markdown格式进行处理。目前处理的内容包括：

* 标题上下增加空行
* 段落上下增加空行
* Code开始前有空行，结束后有空行，Code中的内容不受影响
* 分割线上下增加空行
* List不增加换行


### 使用方法

下载方法见上，使用方法如下：

```
yuque-markdown-formatter -p docs -b
```
