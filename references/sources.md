# 来源、许可与适用范围

整理版本：2.0.0，2026-11-02。基于原工作区已保存的核读记录与用户手动布局样本；没有重新全文核读所有网页/PDF。下列页码均为 PDF 文件页序，具体应用还需核对准确器件与版本。

| 编号 | 来源与已核读范围 | 支持的内容和边界 |
|---|---|---|
| S01 | SparkFun Electronics / jimblom，[How to Read a Schematic](https://learn.sparkfun.com/tutorials/how-to-read-a-schematic/all)，连接点、网络名与 Schematic Reading Tips | 功能分块、阅读方向和器件资料回查；CC BY-SA 4.0。字体尺寸及 SCH 编号为本地建议 |
| S03 | [KiCad Schematic Editor 手册](https://docs.kicad.org/master/en/eeschema/eeschema.html)，既有快照 10.99 开发版、修订 e7c04bc7，Connections/Labels/NC/ERC | 连接表达和检查边界；手册 GPL v3+ 或 CC BY 3.0+。嘉立创网络作用域和连接行为须按当前版本验证，本文为概括 |
| S04 | SparkFun [Pro Micro](https://github.com/sparkfun/Pro_Micro/tree/df836f3bf2955c4f1199a852f618d2ac80866d47/Hardware/v20)，既有固定提交与结构核对 | 开源硬件示例入口，硬件 CC BY-SA 4.0；没有完成全量电气认证，不迁移其参数 |
| U03 | 用户手动原理图排版要求，2026-10-25 | SCH-23～27：本体/引脚一致、不遮挡、连续同网单标签、功能分框和简洁连接；原始工程与截图不公开 |
| S02 | SparkFun Electronics / jimblom，[Using EAGLE: Board Layout](https://learn.sparkfun.com/tutorials/using-eagle-board-layout/all)，Arranging/Routing/Checking/Finishing/Generating Gerbers | 布局→布线→检查→生产输出的流程；CC BY-SA 4.0。此处为中文概括重组并加入用户检查要求，旧软件快捷键和制造例值不沿用 |
| S05 | TI [SLLA414A](https://www.ti.com/lit/an/slla414a/slla414a.pdf)，2026-01修订；p5–6、6–10、12–13、15–18、20–22 | 偏斜、短路径、回流、耦合、过孔、转角与保护。既有记录目视p5/6/8/13/18，其余部分核读正文；不能代替目标芯片、DDR或SerDes专用指南 |
| S06 | TI [SLYT499](https://www.ti.com/lit/an/slyt499/slyt499.pdf)，p1–4，重点p4图4–5 | 混合信号分区与回流，AGND/DGND不机械分割 |
| S07 | TI [SNVA021C / AN-1149](https://www.ti.com/lit/an/snva021c/snva021c.pdf)，p2–4，目视p3 | 开关电源回路、反馈与热；Boost例图不推广成所有拓扑，旧固定线宽/过孔载流经验不作为通用规格 |
| S08 | ADI [MT-101 Rev.0, 03/09](https://www.analog.com/media/en/training-seminars/tutorials/MT-101.pdf)，p1、6–7，目视p6–7 | 去耦、连接寄生和谐振；不统一照抄电容数量与容量 |
| S12 | 嘉立创[设计/生产入口](https://wiki.lceda.cn/zh-hans/design-production/free-pcb.html)、[等长调节](https://prodocs.lceda.cn/cn/pcb/route-equal-length-tuning/)、[差分对等长调节](https://prodocs.lceda.cn/cn/pcb/route-differential-pair-equal-length-tuning/) | 既有Wiki记录枚举70链接，59有正文、2仅标题、9获取失败，不能声称全站图文已读完；等长工具定义不能证明任何接口的电气容差 |
| S13 | ST [AN2867 Rev.25](https://www.st.com/resource/en/application_note/cd00221665-oscillator-design-guide-for-stm8afals-stm32-mcus-and-mpus-stmicroelectronics.pdf)，p45–47、图13–16已目视 | STM32振荡回路、护地与其他层局部地；不能直接作为WCH等其他芯片的专用铜皮规范 |
| U01 | 用户明确规则，2026-10-25至2026-11-02 | GND过孔优先、非过孔90°限制、20→10→20mil、MCU同层去耦、丝印及机械锁定等。它们是用户设计约定，不冒称厂家强制标准 |
| U02 | 用户手动完成后的实时PCB/DSN样本，2026-11-01；结合用户要求逐层观察并绘制几何图 | 差分端点/匹配器件顺通道摆放、顶层直通、晶振沿敏感回路勾勒禁铜及外围GND孔。只提炼方法，不分发用户工程；样本尚有DRC待修项，不把孔距、蛇形或电气容差视为已验证通用值 |

TI/ST/ADI与嘉立创资料保留各自版权；本仓库仅保存整理后的文字、链接及适用性说明，不随包分发厂商PDF、图片、用户附件或EDA工程。原工作区三份二次PDF只作交叉审查，不作为独立数值权威，也不随包分发。

本规则文档对原工作区CC BY-SA 4.0规范进行压缩、去重、按任务重组，保留来源归属；许可见[LICENSE](../LICENSE)。引用不表示原作者认可本Skill或任何PCB。

## 更新一条规则时

记录规则编号、触发条件、做法、原厂文件名/修订/页码或用户要求日期、适用芯片/接口及证据状态。区分“物理原则”“用户偏好”“项目参数”“待验证建议”。与旧规则冲突时标明替代关系，同步项目适用版本；不得把一次失败或未知规格固化为跨项目硬限制。

发布源码的来源指纹在 [provenance.json](../provenance.json)。它用于追溯提炼依据，不证明设计或研究已经全面验证。规则变更修改源码、记录变更、重新核对相关条款，再生成新版本；不要直接修改已安装副本后丢失同步。

2026-11-02 技术澄清：PCB-L17/L20 不统一规定所有电源域使用 100 nF，不把并联去耦当作串联器件，不认为直接平面供电必然使去耦失效。大小电容顺序仅在不损害原厂布局、低电感回路与稳定性时采用。此为基于既有 S07/S08 的规则纠偏，未新增声称 STM32/ME6210 特定参数已经原厂核验。
