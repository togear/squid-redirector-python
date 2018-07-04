# squid-redirector-python
python squid redirector
# Squid Url Rewriter
## 说明
这是一个python 版本的squid url rewritor的例子程序
以后这种防盗链都可以按照这种形式去做

## 用法
更改执行程序的属组
chown squid:squid redirector.py
chmod +x redirector.py
chown squid:squid config.json

在squid.conf里面配置

```
acl redirect_host url_regex -i http://mooc.test/.*
url_rewrite_program /usr/local/squid/bin/redirector.py /usr/local/squid/etc/config.json
url_rewrite_children 300
url_rewrite_host_header on
url_rewrite_concurrency 0
redirector_bypass off
url_rewrite_access allow redirect_host
url_rewrite_access deny all
```


## 测试
两种方法
### 命令行方式
可以直接在命令行的方式下执行这个命令
./redirector.py config.json 
然后标准输入
http://mooc.test/course/1.flv?k=ff6da47d&t=1528252675 1.1.1.1/- ddd

### 集成方式
在squid里面运行这个程序：
配置：
```
url_rewrite_program /usr/local/squid/bin/squid_redirector.py /usr/local/squid/etc/config.json
url_rewrite_children 200
url_rewrite_host_header on
redirector_bypass off
```
直接访问url，查看返回状态码

两者都可以在 /tmp/squid-redirector.log  查看具体的日志
