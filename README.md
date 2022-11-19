# RIME 配置

基于rime实现的 以小鹤双拼作为双拼方案 以超强音形(二笔)作为辅助码 实现的输入方案

## 方案简介

```plaintext
  主: 小鹤双拼
  辅: 单字第三码 由 超强音形 的 形码提供筛选 (正常2码或者多码打单字或词组不受影响)
  例:
    if = chen, m = 乚丨 即 ifm = 陈
    la = la,   l = 口   即 lal = 啦
    jq = jiu,  x = 丨   即 jqx = 旧
    dajx 依旧是 大家，xl 依旧是想，不会受辅助码影响


  超强音形键位图:

    ┌───────────────瞥区───────────────┬───────────────点区───────────────┐
    │                                  │                                  │
    ┌──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┐
    │ Q    │ W    │ E    │ R    │ T    │ Y    │ U 扌 │ I    │ O    │ P    │
    │      │      │      │      │      │      │      │      │      │      │
    │ 丿一 │ 丿丨 │ 丿丿 │ 丿丶 │ 丿乚 │ 丶一 │ 丶丨 │ 丶丶 │ 丶丶 │ 丶乚 │
    └────┬─┴────┬─┴────┬─┴────┬─┴────┬─┴────┬─┴────┬─┴────┬─┴────┬─┴────┬─┘
      ┌──│ A    │ S 日 │ D 月 │ F 亻 │ G    │ H    │ J    │ K    │ L 口 │──┐
      竖 │      │      │      │      │      │      │      │      │      │  │
      区 │ 丨一 │ 丨丨 │ 丨丿 │ 丨丶 │ 丨乚 │ 一一 │ 一丨 │ 一丿 │ 一丶 │  横
      └──└────┬─┴────┬─┴────┬─┴────┬─┴────┬─┴────┬─┴────┬─┴────┬─┴──────┘  区
              │ Z 钅 │ X 木 │ C 氵 │ V 土 │ B 艹 │ N    │ M    │           │
              │ 一   │ 丨   │ 丿   │ 丶   │ 乚   │      │ 一乚 │           │
              │      │      │ 乚丿 │ 乚丶 │ 乚乚 │ 乚一 │ 乚丨 │           │
              └──────┴──────┴──────┴──────┴──────┴──────┴──────┘───────────┘
              │             │                    │             │
              └─────────────┼─单笔画区───────────┘             │
                            │                                  │
                            └───────────────折区───────────────┘

    熟记五个笔画区 瞥点竖横折, 每个区都是 横竖瞥点折
    另需要记忆极少字根 U手、SD 日月、F人、L口、ZXCVB 金木水土草
```

## 配置文件结构

```plaintext
  .
  ├── dicts/                           -- 词库文件夹
  ├── lua/                             -- lua脚本文件夹
  ├── default.custom.yaml              -- 配置索引(配置入口)
  ├── mine.schema.yaml                 -- 配置方案
  ├── custom_phrase.txt                -- 个性短语
  ├── pinyin.extanded.dict.yaml        -- 词库
  ├── rime.lua                         -- lua插件入口
  └── README.md
```

## 如何使用

```shell
# 确保你已经正确安装fictx5和rime, 以archlinux举例
sudo pacman -S fcitx5 fcitx5-qt fcitx5-gtk fcitx5-config-qt fcitx5-material-color fcitx5-im fcitx5-rime
sudo echo '
GTK_IM_MODULE=fcitx
QT_IM_MODULE=fcitx
XMODIFIERS=@im=fcitx
SDL_IM_MODULE=fcitx
GLFW_IM_MODULE=ibus' >> /etc/environment

# clone本仓库
mkdir -p ~/.local/share/fcitx5
git clone https://github.com/yaocccc/rime ~/.local/share/fcitx5
```

## 按键说明

```plaintext
  [        以词定字 选中选中词的第一个字
  ]        以词定字 选中选中词的第二个字
  回车     上屏
  左shift  选中第二个候选
  右shift  选中第三个候选
```

## Q & A

Q: 如何自定义短语?  
A: 修改 custom_phrase.txt 注意不要修改上面的内容  

Q: 是否支持切换双拼方案?
A: 不支持 不仅mine.schema.yaml中是根据小鹤双拼定制的，固定词库中也是以此定制  
