# HeCaiYun签到

本仓库由[xuthus5/HeCaiYun](https://github.com/xuthus5/HeCaiYun)修改而来。

## 特色

1. 支持多账号按顺序签到

2. 支持多种方案启动
   1. 腾讯云函数启动
   2. 配置文件方式启动

## 使用方法

### 获取Cookie

打开[和彩云签到有礼 (10086.cn)](https://caiyun.feixin.10086.cn:7071/portal/newsignin/index.jsp)页面=>登录=>按`F12`打开开发者工具-Network=>F5刷新页面=>过滤参数填`caiYunSignIn`=>找到`caiYunSignIn.action`请求=>点击查看**cookie**，只要从`JSESSIONID`到第一个`;`，即类似于`JSESSIONID=8BCB8BCB8BCB8BCB8BCB8BCB8BCB8BCB-n1;`的内容。

### 开始运行

#### 配置字段解释

| 字段名         | 含义                                    | 数据类型 | 是否必须 | 默认策略 |
| -------------- | --------------------------------------- | -------- | -------- | -------- |
| `Cookie`       | 用户账户认证                            | 字符串   | **是**   |          |
| `OpenLuckDraw` | 开启抽奖                                | 布尔     | 否       | 不抽奖   |
| `push_key`     | 推送Key，根据此值确定推送通道。[详解]() | 字符串   | 否       | 不推送   |

#### 腾讯云函数环境变量运行

将配置字段填入腾讯云环境变量：

1. `Cookie`(必须)：如需多个账户，请在每个账号Cookie之间加上`#`符号。
2. `OpenLuckDraw`：设为`ture`则为开启，其他为关闭。多个账户请加`#`，数量与Cookie数量不一致会，后边的账户采用默认策略（不抽奖）。
3. `push_key`：多个账户请加`#`，如果push_key的数量没有cookie的多，则只使用第一个push_key，否则按顺序使用。

#### 配置文件运行

`[]`内填任意个`{}`，每个`{}`是一个账户的信息，`{}`必须是三个键、值都存在。

```
[
  {
    "Cookie": "Cookie1",
    "OpenLuckDraw": true,
    "push_key": "push_key1"
  },
  {
    "Cookie": "Cookie2",
    "OpenLuckDraw": true,
    "push_key": "push_key2"
  }
]
```

## 注

因本人不会go语言，遂不维护go语言版本，如有需要请使用原仓库[xuthus5/HeCaiYun](https://github.com/xuthus5/HeCaiYun)

