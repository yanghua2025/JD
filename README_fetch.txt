
### 使用指南

1. 将本压缩包解压并把所有文件整体上传到 GitHub 私有仓库根目录。
2. 进入 GitHub -> Actions 标签页，首次需点击 'I understand my workflows' 启用。
3. 在工作流列表找到 **Fetch HKEX OHLC once** -> 点击 **Run workflow** 测试。
   日志中会输出 latest_price.json 内容，同目录亦会生成工件(Artifact)可下载。
4. 若要每天自动抓取，把 workflow_dispatch 改成:
     on:
       schedule:
         - cron: '10 10 * * *'   # UTC 10:10 = 北京 18:10
   并提交即可。
