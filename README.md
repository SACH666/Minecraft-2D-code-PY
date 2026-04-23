> 出于娱乐与学习目的，请勿用于商业目的
***
<a href='https://dashuaige2025.lanzouu.com/iV9tP3n1fb3c'>![download](https://img.shields.io/badge/download%20%7C%20last-exe-blue.svg)</a>
<a href='https://dashuaige2025.lanzouu.com/b016knwxli'>![download](https://img.shields.io/badge/download%20%7C%20history%20%7C%20password%20c72r-exe-blue.svg)</a>
![Version](https://img.shields.io/badge/version-b26.9-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-green.svg)

# Minecraft-2D-code-PY
## 这是一个2D版我的世界的项目
这会展示Minecraft 2D的最新版本
# 免责声明

## 2D Minecraft 游戏免责声明

### 1. 项目性质
本软件（以下简称“本游戏”）是一个非商业性质的粉丝自制项目，仅供个人学习、研究和娱乐使用。本游戏是对《Minecraft》（我的世界）游戏机制的致敬和二次创作，并非官方授权产品。

### 2. 版权声明
- 《Minecraft》是 Mojang AB 公司的注册商标和版权作品
- 本游戏与 Mojang AB、Microsoft 及其关联公司没有任何官方关联、认可或授权
- 游戏中的方块名称、游戏机制等元素灵感来源于《Minecraft》，但代码实现为原创
- 如涉及侵权，请联系删除

### 3. 使用限制
- 本游戏完全免费，任何个人或组织不得将其用于商业目的
- 不得将本游戏或其任何部分声称拥有版权或所有权
- 不得将本游戏用于任何非法活动或违反道德的行为

### 4. 风险声明
- 本游戏按“现状”提供，不提供任何明示或暗示的保证
- 使用本游戏所产生的任何数据丢失、硬件损坏或其他损失，开发者不承担责任
- 联机功能通过网络传输数据，请勿在不可信的网络环境中使用

### 5. 源代码
- 本游戏源代码仅供学习和研究目的
- 如需修改或分发，请保留原始版权声明和免责声明

### 6. 联系方式
如有版权问题或其他疑问，请通过以下方式联系：
- 项目 Issue 页面提交问题

---

**使用本游戏即表示您已阅读、理解并同意本免责声明的所有条款。**

---

# README.md


## 目录结构

``` Text
2D_Minecraft/
├── minecraft2d.py      # 主游戏文件
├── dark.png            # 地底滤镜图片（可选）
├── saves/              # 存档目录
│   └── *.json          # 世界存档文件
├── skins/              # 皮肤目录
│   └── *.png           # 皮肤图片（建议 32x64 或 32x32）
├── fonts/              # 字体目录（可选）
└── textures/           # 纹理目录（内置纹理优先）
```


## 常见问题

### Q: 游戏启动后显示黑色画面？
A: 确保 Pygame 正确安装，尝试更新显卡驱动。

### Q: 中文字体显示异常？
A: 将中文字体文件（如 simhei.ttf）放入 `fonts/` 目录，或安装系统字体。

### Q: 联机模式无法连接？
A: 
- 检查防火墙是否允许 Python 访问网络
- 确保服务器地址和端口正确
- 服务器需要开放指定端口

### Q: 皮肤不显示？
A: 将 PNG 图片放入 `skins/` 目录，皮肤尺寸建议为 32x64 或 32x32。

### Q: 游戏卡顿？
A: 
- 减小 `RENDER_DISTANCE` 配置
- 关闭 `SHOW_CLOUDS` 效果
- 关闭 `AMBIENT_OCCLUSION` 效果

### Q: 如何自定义地底滤镜？
A: 在游戏根目录放置 `dark.png` 图片，程序会读取图片从左到右的渐变颜色作为滤镜。

## 开发计划

- [ ] 更多方块类型（玻璃、羊毛、红石电路）
- [ ] 动物系统
- [ ] 掉落物实体
- [ ] 更完善的地形生成
- [ ] 音效和背景音乐
- [ ] 成就系统

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

本项目仅供学习和研究使用，请勿用于商业用途。

## 致谢

- Mojang AB 创作的《Minecraft》游戏
- Pygame 社区提供的优秀游戏开发库
