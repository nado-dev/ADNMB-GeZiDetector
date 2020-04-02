# GeZiDetector

简陋的python(**2.7**)小脚本，网课摸鱼，python复健，图一乐

## update
* 20.3.31 initial commit
* 20.4.2  依赖文件更改为json，可以追踪多个串
## 功能

跟踪某串的动态，更新时通过 Server Chan 提供的微信推送功能提醒。

* 建议与`cron `配合使用
## 已知问题
+ [ ] 愚人节全员红名特效时失效

## Before It

* `git clone https://github.com/AaronFang123/ADNMB-GeZiDetector`

* 去 [Server Chan](http://sc.ftqq.com/3.version)使用Github账号申请`SCKEY`，在同一目录下建立一个`SCKEY.config`文件，将`SCKEY`放入其中

  `echo "[SCKEY]" > SCKEY.config`

* `python Adnmb2.py`(adnmb2依赖的文件是`Adnmb.json`, 支持多串)
 
    或`python adnmb.py`(依赖的文件是`Adnmb.config`,仅支持单串，不建议)

> `check_status.py`用于辅助管理列表
## 依赖

* bs4
* requests
* codecs

## Other

~~目前只可以跟踪一个串（不会补充，摸了摸了）~~
