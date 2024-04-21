<!-- markdownlint-disable MD033 MD036 -->

# BAWiki Data

这里是供 [nonebot-plugin-bawiki](https://github.com/lgc2333/nonebot-plugin-bawiki) 插件使用的的数据源仓库

## 🌏 可用地址

<!-- - (国内 CDN) <https://bawiki.lgc.cyberczy.xyz> -->

- (Anycast, 实时更新, by [@Vercel](https://vercel.com/)) <https://bawiki.lgc2333.top>
- (CN, 半小时一次, by [@ltzXiaoYanMo](https://ymbit.cn/)) <https://bawiki-data.ymbit.cn>

直接访问跳转到仓库主页是正常的，加上文件路径就行了  
比如 <https://bawiki.lgc2333.top/img/student/_all.png>

如果有佬搭建了国内好用的反代的话，欢迎联系我在这里添加上你的地址！

## 📦 使用本仓库的项目

如果想往这里加上你的项目，可以直接[联系我](#-联系)，或者提交一个 PR

- [lgc-NB2Dev/nonebot-plugin-bawiki](https://github.com/lgc-NB2Dev/nonebot-plugin-bawiki)
  - 基于 NoneBot2 的碧蓝档案 Wiki 插件
- [staytomorrow/ba_calendar_e](https://github.com/staytomorrow/ba_calendar_e)
  - 基于 CQHTTP 及 KuMiao，支持私聊 / 群聊 / QQ 频道，碧蓝档案图形化日程表，Wiki 查询，模拟抽卡等功能
- [Alin-sky/koishi-plugin-ba-plugin](https://github.com/Alin-sky/koishi-plugin-ba-plugin)
  - Koishi 插件，BlueArchive / 碧蓝档案 工具箱，正在不断开发新功能

## 📝 贡献指南

欢迎各位向数据源贡献内容~  
当你成功提交一次贡献之后，我将会邀请你成为本仓库的 Contributor，下面的鸣谢栏里也会写上你的名字！  
如果你不会编写 json 或提交 Pull Request，也可以直接向仓库提交一个 Issue 说明并提供你要提交的内容！

插件所需的数据基本上来自 `data` 文件夹，下面是 `data` 文件夹下各 json 的用途解释

<details>

<summary>点击展开</summary>

**!!! 注意 !!!** 下面数据中的学生名中的括号请一律使用 **英文半角** 括号

### `emoji.json`

这个文件是 `ba表情` 功能的表情列表

该文件会自动由 Actions 工作流根据 `img/emoji` 文件夹中的内容自动生成  
所以想要加表情的话请直接往这个文件夹里扔图片就行

### `event_alias.json`

这个文件是 `ba活动` 功能的活动别名数据

该文件的格式如下

```jsonc
{
  // 这里的 701 代表该活动在 SchaleDB 中的 ID，可以在下面链接中的 EventNames 中找到
  // https://github.com/lonqie/SchaleDB/blob/main/data/cn/localization.json
  // 数组中的内容代表活动别名
  "701": ["特殊作战·十字神名篇", "特殊作战 十字神名篇"],
}
```

### `extra_l2d_list.json`

这个文件是 `ba羁绊` 功能使用的学生 L2D 图片数据

当没有在此文件中找到学生 L2D 信息时，才会去 GameKee 中抓取

该文件的格式如下

```jsonc
{
  // 键名是对应学生在 SchaleDB 中的 中文名
  // 数组中的内容是对应图片在数据源中的路径（下文中路径仅供演示）
  "阿露": ["img/l2d/aru/1.png"],
}
```

### `gacha.json`

这个文件是 `ba抽卡` 功能使用的卡池数据

该文件的格式如下

```jsonc
{
  // 常驻卡池数据
  "base": {
    // 三星常驻角色数据
    "3": {
      // 基础出率，2.5 代表 2.5%
      "chance": 2.5,

      // 常驻角色在 SchaleDB 中的 ID，会由 Actions 工作流自动生成
      "char": [10000], // ...
    },

    // 两星常驻角色数据，结构同上
    "2": {
      "chance": 18.5,
      "char": [13000], // ...
    },

    // 一星常驻角色数据，结构同上
    "1": {
      "chance": 79.0,
      "char": [16000], // ...
    },
  },

  // UP 卡池数据
  "up": {
    // 三星 UP 角色数据
    "3": {
      // UP 角色出率
      "chance": 0.7,
    },

    // 两星 UP 角色数据，结构同上
    "2": {
      "chance": 3.0,
    },
  },

  // 当前 UP 池数据，用于 `ba切换卡池` 功能
  "current_pools": [
    {
      // 池子名称，通常为角色名称
      "name": "若藻(泳装)",

      // 池子包含的 UP 角色 SchaleDB 中的 ID，可以在下面的链接找到
      // https://github.com/lonqie/SchaleDB/blob/main/data/cn/students.json
      "pool": [10043],
    },
  ],
}
```

### `manga.json`

此文件已弃用

<!-- 这个文件是 `ba漫画` 功能所使用的数据

该文件会由 Actions 工作流爬取 GameKee 数据并自动生成

该文件的格式如下

```jsonc
[
  {
    // 漫画在 GameKee 中的 content_id，需要爬取 GameKee 的接口获取
    // 额外添加的漫画设为与其他所有漫画不同的负数即可
    "cid": 72443,

    // 漫画标题
    "title": "【ぶるーあーかいぶっ！】第一话",

    // 漫画简介
    "detail": "第一话 对策委员会\n\n来源：BA官推漫画作者：純粋な不純物(@parang9494)先生\n汉化：小番茄",

    // 漫画的图片链接列表，需要使用完整链接
    "pics": ["https://cdnimg.gamekee.com/images/www/1616470072424_26237045.jpg"]
  }
]
``` -->

### `raid_alias.json`

这个文件是 `ba总力战` 功能使用的 Boss 别名列表

该文件的格式如下

```jsonc
{
  // 这里的 1 代表该 Boss 在 SchaleDB 中的 ID，可以在下面的链接中找到
  // https://github.com/lonqie/SchaleDB/blob/main/data/cn/raids.json
  // 后面数组中的内容是该 Boss 对应的别名
  "1": ["binah", "薇娜", "大蛇"],
}
```

### `schale_to_gamekee.json`

这个文件是 SchaleDB 学生中文名到 GameKee 学生名称的映射表  
用于 `ba学生wiki`、`ba羁绊` 等需要用到 GameKee 数据源的场合

该文件的格式如下

```jsonc
{
  // 键为学生在 SchaleDB 的中文名
  // 值为学生在 GameKee 中的名称
  "真纪": "真希",
}
```

### `stu_alias.json`

这个文件是所有的学生别名列表

其中，下面的内容会自动由 Actions 工作流补全：

- 学生的日语名称 与 英文（罗马音）名称；
- 学生的中日英全名；
- 特殊（带括号名称）学生 的别名（根据普通学生的别名、括号中的内容 及 `suffix_alias.json` 中的内容来补全）；

同时，Actions 工作流会自动对该文件中的内容进行按拼音顺序的排序

该文件的格式如下

```jsonc
{
  // 键为学生在 SchaleDB 的中文名
  // 值为学生的别名列表
  "白子": [
    "シロコ", // 自动由 Actions 工作流补全的 日文名
    "shiroko", // 自动由 Actions 工作流补全的 英文名
    "sunaookami shiroko", // 自动由 Actions 工作流补全的 英文全名
    "xcw",
    "砂狼白子", // 自动由 Actions 工作流补全的 中文全名
    "砂狼シロコ", // 自动由 Actions 工作流补全的 日文全名
    "唯",
    "小仓唯",
  ],

  // 同上
  "白子(单车)": [
    "シロコ(ライディング)", // 自动由 Actions 工作流补全的 日文名
    "shiroko (cycling)", // 自动由 Actions 工作流补全的 英文名
    "sunaookami shiroko (cycling)", // 自动由 Actions 工作流补全的 英文全名
    "单车shiroko", // 自动由 Actions 工作流补全的 特殊学生别名
    "单车xcw", // 自动由 Actions 工作流补全的 特殊学生别名
    "单车白子", // 自动由 Actions 工作流补全的 特殊学生别名
    "单车シロコ", // 自动由 Actions 工作流补全的 特殊学生别名
    "单车唯", // 自动由 Actions 工作流补全的 特殊学生别名
    "单车小仓唯", // 自动由 Actions 工作流补全的 特殊学生别名
    "骑行shiroko", // 自动由 Actions 工作流补全的 特殊学生别名
    "骑行xcw", // 自动由 Actions 工作流补全的 特殊学生别名
    "骑行白子", // 自动由 Actions 工作流补全的 特殊学生别名
    "骑行唯", // 自动由 Actions 工作流补全的 特殊学生别名
    "骑行小仓唯", // 自动由 Actions 工作流补全的 特殊学生别名
    "骑行シロコ", // 自动由 Actions 工作流补全的 特殊学生别名
    "砂狼白子(单车)", // 自动由 Actions 工作流补全的 中文全名
    "砂狼シロコ(ライディング)", // 自动由 Actions 工作流补全的 日文全名
  ],
}
```

### `suffix_alias.json`

这个文件是补全括号后缀的特殊学生别名时使用的数据

该文件的格式如下

```jsonc
{
  // 键名是特殊学生名中括号内的内容
  // 值是另外的要加在补全后别名中的前缀
  // 比如 `星野(泳装)` 会补全成 `泳装星野`、`水星野`
  "泳装": ["水"],
}
```

### `terrain_alias.json`

这个文件是 `ba总力战` 功能中使用的战斗环境匹配别名

该文件的格式如下

```jsonc
{
  // 键名为环境英文名，可以在下面链接的 AdaptationType 里找到
  // https://github.com/lonqie/SchaleDB/blob/main/data/cn/localization.json
  // 值为对应的别名数组
  "Street": ["市区", "城镇", "市区战", "城镇战"],
  "Outdoor": ["野外", "野外战", "野战"],
  "Indoor": ["室内", "屋内", "室内战", "屋内战"],
}
```

### `wiki.json`

这个文件里的东西比较杂，请看下面注释

该文件的格式如下

```jsonc
{
  // 总力战 wiki 图片列表
  "raid": {
    // 键名为 Boss ID，请见 raid_alias.json 的说明
    "1": {
      // Boss wiki 图片路径（以仓库根目录为基准）
      "wiki": "img/raid/binah.png",

      // Boss 战斗环境与对应图片
      "terrains": {
        // 键名为战斗环境英文名称
        // 值为 [ 日服对应图片路径, 国际服对应图片路径 ]
        "Street": ["img/raid/jp/1_Street.png", "img/raid/global/1_Street.png"],
        "Outdoor": [
          "img/raid/jp/1_Outdoor.png",
          "img/raid/global/1_Outdoor.png",
        ],
      },
    },
    // ...
  },

  // 制造相关一图流
  "craft": ["img/craft/1.png"],

  // 活动一图流，键名是活动 ID（详见 event_alias.json 介绍）
  "event": {
    "801": ["img/event/801_re.png"],
    // ...
  },

  // 学生角评一图流，键名是学生 SchaleDB 中文名（all 是总览图）
  "student": {
    "all": "img/student/_all.png",
    "阿露": "img/student/aru.png",
    // ...
  },

  // 战术考试一图流，从第一期开始，按顺序排期数
  "time_atk": [
    "img/time_atk/1.png",
    "img/time_atk/2.png",
    // ...
  ],

  // 互动家具一图流（我好像没实装？）
  "furniture": ["img/furniture.png"],

  // 国际服前瞻图相关信息
  "global_future": {
    // 图片路径
    "img": "img/global_future.png",

    // 图片表格头部起止 Y 轴坐标
    "banner": [0, 195],

    // 图片各部分对应的前瞻数据
    "parts": [
      {
        // 该部分对应的日期区间，格式必须与下面相同（YYYY/M/D）
        "date": ["2023/4/25", "2023/5/09"],

        // 该部分对应的图片起止 Y 轴坐标
        "part": [192, 484],
      },
      // ...
    ],
  },
}
```

</details>

## 💡 鸣谢

_名单按首字母排序_

| 贡献者                                                       | 内容                                     |
| :----------------------------------------------------------- | :--------------------------------------- |
| [Alin-sky](https://github.com/Alin-sky)                      | 仓库贡献                                 |
| [blacksidd](https://github.com/blacksidd)                    | 仓库贡献                                 |
| [Ealvn](https://github.com/Ealvn)                            | 仓库贡献                                 |
| [FuRobert](https://github.com/FuRobert)                      | 仓库贡献                                 |
| [GameKee](https://ba.gamekee.com/)                           | 官推漫画，部分翻译等                     |
| [黑枪灬王子](mailto:1109024495@qq.com)                       | 学生别名提供                             |
| [ltzXiaoYanMo](https://ymbit.cn/)                            | 镜像贡献                                 |
| [Nekowryyy](https://github.com/Nekowryyy)                    | 仓库贡献                                 |
| [Rouphy](https://github.com/Rouphy)                          | 学生别名提供                             |
| [SchaleDB](https://schale.gg/)                               | 部分中文翻译等                           |
| [夜猫咪喵喵猫](https://space.bilibili.com/425535005/article) | 总力战一图流，活动一图流，学生角评等图片 |

## 📞 联系

QQ：3076823485  
Telegram：[@lgc2333](https://t.me/lgc2333)  
吹水群：[1105946125](https://jq.qq.com/?_wv=1027&k=Z3n1MpEp)  
邮箱：<lgc2333@126.com>

## 💰 赞助

**[赞助我](https://blog.lgc2333.top/donate)**

感谢大家的赞助！你们的赞助将是我继续创作的动力！
