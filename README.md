# sina-weibo-crawler

## 抽取数据段

| 段域 | 数据类型 | 含义 | 附加说明 |
|-------------|-------------|------------|---------------|
| url | string | 主页的链接地址 | |
| nickname | string | 昵称 | |
| verify_type | string | 认证类型 | |
| verify_info | string | 认证信息 | |
| num_fans | int | 粉丝数目 | |
| num_follow | int | 关注数目 | |
| num_weibo | int | 发布微博数目 | |
| gender | string  | 性别 | |
| birthday | string | 生日 | 部分情况下新浪返回星座 |
| weibo | array | 用户所发微博 | 数组每一个元素为微博文本 |
| fans | array | 用户粉丝信息 | 每一个元素包含num_fans, url, nickname, verify_info |
| follow | array | 用户关注信息 | 每一个元素包含num_fans, url, nickname, verify_info |
| location | string | 地区 | |
| relationship_status | string | 感情状态 | |
| sexual_orientation | string | 性取向 | |
| self-intro | string | 简介 | |
| tags | array | 用户标签 | 每个元素为标签字符串 |

## 使用示例

 ```python
 # -*- coding: utf-8 -*-
from wcrawler import *

if __name__ == '__main__':
    crawler = WCrawler(cookie = '_T_WM=1764ed14d4a61ef43ab86ce292307697; SUHB=0G0veCMff5FczB; SUB=_2A257Qs6KDeTxGeRP6VYZ9yrLzz2IHXVYzNLCrDV6PUJbrdAKLWvFkW1D2q2amgN3BCri-O-SXueGVG-2Rg..; gsid_CTandWM=4urb5d951ez5pXptyT36L8UMabX', \
        max_num_weibo = 10, \
        max_num_fans = 10, \
        max_num_follow = 10, \
        wfilter = ALL)
    print crawler.crawl(url = 'http://weibo.cn/yaochen')
 ```

## 示例输出结果

    {
    "birthday": "",
    "fans": [
        {
            "nickname": "丿子任",
            "num_fans": 18,
            "url": "http://weibo.cn/u/5301151254",
            "verify_info": ""
        },
        {
            "nickname": "Jasmine_200105",
            "num_fans": 16,
            "url": "http://weibo.cn/u/5754254176",
            "verify_info": ""
        },
        {
            "nickname": "赵赵赵赵娟GZ",
            "num_fans": 17,
            "url": "http://weibo.cn/u/5229049331",
            "verify_info": ""
        },
        {
            "nickname": "用户5194588785",
            "num_fans": 2,
            "url": "http://weibo.cn/u/5194588785",
            "verify_info": ""
        },
        {
            "nickname": "ai正少",
            "num_fans": 49,
            "url": "http://weibo.cn/u/2681105533",
            "verify_info": ""
        },
        {
            "nickname": "D3逗啵小耗子",
            "num_fans": 4,
            "url": "http://weibo.cn/u/5717791993",
            "verify_info": ""
        },
        {
            "nickname": "小美8679",
            "num_fans": 50,
            "url": "http://weibo.cn/u/3790702567",
            "verify_info": ""
        },
        {
            "nickname": "byhcrown123",
            "num_fans": 9,
            "url": "http://weibo.cn/u/5280328847",
            "verify_info": ""
        },
        {
            "nickname": "浮云总在天边",
            "num_fans": 2,
            "url": "http://weibo.cn/u/5758789211",
            "verify_info": ""
        },
        {
            "nickname": "赛车手198411",
            "num_fans": 1,
            "url": "http://weibo.cn/u/5759176656",
            "verify_info": ""
        }
    ],
    "follow": [
        {
            "nickname": "毕飞宇",
            "num_fans": 798868,
            "url": "http://weibo.cn/bifeiyu"
        },
        {
            "nickname": "编剧王小平",
            "num_fans": 33531,
            "url": "http://weibo.cn/u/1150691890"
        },
        {
            "nickname": "英国报姐",
            "num_fans": 8127079,
            "url": "http://weibo.cn/uktimes"
        },
        {
            "nickname": "早稻-野獸",
            "num_fans": 177911,
            "url": "http://weibo.cn/u/1835883650"
        },
        {
            "nickname": "韩浩月",
            "num_fans": 52687,
            "url": "http://weibo.cn/hanhaoyue"
        },
        {
            "nickname": "故宫博物院",
            "num_fans": 1713654,
            "url": "http://weibo.cn/gugongweb"
        },
        {
            "nickname": "Mr_凡先生",
            "num_fans": 12055001,
            "url": "http://weibo.cn/u/3591355593"
        },
        {
            "nickname": "洛梅笙",
            "num_fans": 27326,
            "url": "http://weibo.cn/u/2034280670"
        },
        {
            "nickname": "企鹅奸妃",
            "num_fans": 2779,
            "url": "http://weibo.cn/u/1165842462"
        },
        {
            "nickname": "张译",
            "num_fans": 2342913,
            "url": "http://weibo.cn/yanyuanzhangyi"
        }
    ],
    "gender": "女",
    "location": "北京 朝阳区",
    "nickname": "姚晨",
    "num_fans": 78474009,
    "num_follow": 456,
    "num_weibo": 8240,
    "relationship_status": "",
    "self-intro": "",
    "sexual_orientation": "",
    "tags": [],
    "url": "http://weibo.cn/yaochen",
    "verify_info": "演员，联合国难民署中国亲善大使。",
    "verify_type": "RED_V",
    "weibo": [
        "转发了 中国新闻网 的微博:【浙江丽水山体滑坡已致4死33失踪】昨晚22点50分左右，浙江丽水莲都区雅溪镇里东村发生山体滑坡，据当地新闻发布会上最新消息：①滑坡已致4人死亡，33人失踪，27户房屋被埋，21户房屋进水；②当地已转移群众300多人；③抢险救灾正全力展开，灾害原因正在进一步调查中。 [组图共9张]转发理由:愿逝者安息，早日找到生还者。[蜡烛][祈祷]  ",
        "转发了 南方都市报 的微博:#巴黎遇袭#中国驻法国使馆建议，在法中国公民如无特殊需要，近期内尽量减少出行，密切跟踪法国当地媒体的相关报道和警方的安全提示，并配合警方的安全检查和证件检查。如遇紧急情况，可以拨打以下电话。@与欧洲有关的一切转发理由:转发微博  ",
        "转发了 央视新闻 的微博:#巴黎恐怖袭击#【[话筒]紧急扩散：出国旅游一定记住电话12308】法国发生恐怖袭击事件，中国驻法国使馆发紧急通知，提醒在法中国公民注意安全。中国驻法使馆领事保护与协助电话：0033-615742537。外交部全球领保与服务应急呼叫中心电话：00861012308。不管同胞身处哪国，拨通电话，就能得到帮助！转！转发理由:[蜡烛] //@李晨:[祈祷]  ",
        "转发了 头条新闻 的微博:【再次提醒：所有在法中国人留在家中，不要出门！】11月13日晚，法国遇恐怖袭击153人死亡。中国驻法使馆紧急通知，所有在法中国公民留在家中，避免出门。遇紧急情况请即拨报警电话17或197。中国使馆领保电话：0033-615742537；外交部应急呼叫电话：00861012308。新浪新闻正播报：http://t.cn/RUY2svA [组图共3张]转发理由:[伤心]  ",
        "转发了 北京人不知道的北京事儿 的微博:#北京提个醒儿# 【五年不换手机号的人可信度高！】@法制晚报 ：据统计5年以上不换手机号码者，是个相当值得信赖的可交之友。据中、美、英、韩、俄等国抽样调查得出结论：若一个人的手机号码能8年以上保持不变，则可以判定这是一个非常值得信赖的人。你手机号有几年没换了？[嘻嘻] 是这样么[思考] [组图共2张]转发理由:没记错的话，我的手机号应该用了十四年了…[doge] //@亲爱的黄金:十年了我的已经 //@loverwg:我十年了 还欠着你的钱。。。。。。。。 //@加娟:我的六年了，从不欠别人钱  ",
        "转发了 南方都市报 的微博:#午间分享#我们怀念的童年，一去不复返了。@复古老照片 [组图共9张]转发理由:童年的小溪，池塘和大树，都不知何时离开了我们…[白云]  ",
        "真正有用的东西，其实是陪伴。🌛 http://t.cn/RUWyzme ",
        "转发了 姚晨 的微博:爸妈不在家，老婆还没有，独自过双11。[doge]转发理由:这是爸妈的床，角度问题显大。土豆每天睡前都坐在这里看巧虎，等着妈妈回家，妈妈的怀抱就是他的温床。[张嘴][月亮] //@新浪娱乐:回复@Adela曾晓敏:小土豆只是想要一张小床[笑cry] //@Adela曾晓敏:每天在两百万平方米的床上醒来[眼泪]  ",
        "爸妈不在家，老婆还没有，独自过双11。[doge] 原图 ",
        "转发了 毕飞宇 的微博:【毕飞宇：关于《红楼梦》答新京报记者柏琳问】我一直建议年轻人去读《红楼梦》，尤其是独生子女，不读，就不会懂得中国的宗亲，就无法了解那个巨大的、隐形的、神秘的中国，就无法懂得中国的社会为什么会是“人情社会”，就没法认识“人情社会”的温暖和“人情社会”的邪恶。http://t.cn/RUNpfM2转发理由:转发微博  "
    ]
    }


## 待实现的功能

1.用email和密码组合来模拟登录

登录过程的http重定向比较多，还在尝试中。。。

## FAQ

1.爬取大量数据会不会被新浪封禁账户？

会的。我只碰到临时封禁的情况，过段时间自动解禁，建议注册马甲。

2.不要爬取所登录账户的微博数据！！网页结构不一样，会挂掉的。
