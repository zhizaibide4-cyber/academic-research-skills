# 修改说明与逐条回应（R→A→C 格式）

格式说明：**R** 为审稿意见，**A** 为作者回应（作者需确认或改写），**C** 为修订稿中的具体改动及位置。修订稿指 `02_Manuscript_NatMed_Review_EN.md`。

---

## 一、总体改动

| 项目 | 原稿 | 修订稿 |
|---|---|---|
| 语言 | 中文 | 英文（英式拼写，符合 Nature 体例） |
| 标题 | 从通用病理基础模型到罕见病精准诊疗：小样本适配、跨域泛化与临床转化 | Pathology foundation models for rare disease diagnosis: data-efficient adaptation, cross-site robustness and the evidence gap |
| 摘要 | 约 480 字，含参考文献式数字 | 147 词，无引文，符合 Review 摘要体例 |
| 正文 | 约 2.2 万字 | 4931 词（不含 Box、图注、表格） |
| 展示项 | 5 图 + 5 表 + 21 个开放问题 | 5 图 + 2 表 + 3 个 Box；原表 3 和表 5 移入附录 |
| 参考文献 | 106 条，其中 25 条无法核实 | 123 条，全部可追溯（DOI、arXiv 或官方注册号） |
| 文章定位 | 自称"系统梳理" | 叙述性综述，检索策略透明并放入附录 |
| 署名 | AI 系统 | 人类作者占位符，附 AI 使用声明 |

---

## 二、逐条回应

### EIC

**R-EIC-1** AI 系统不能署名为作者。
**A** 接受。
**C** 首页改为人类作者占位符并附政策说明；文末新增 "Use of AI-assisted technologies" 一节。

**R-EIC-2** 自由投稿的 Review 应先提交预投稿询问。
**A** 接受。
**C** 新增 `05_Presubmission_Enquiry_EN.md`。

**R-EIC-3** 篇幅与展示项超标。
**A** 接受。
**C** 正文压缩到约 4900 词；21 个开放问题合并为 Box 3 的 8 个问题；原表 3（域偏移缓解）和表 5（可信性要求）改为附录表 S2、S3。

### 审稿人 1

**R1-M1** 规模律引文方向错误。
**A** 接受。
**C** 新写 "Does scale help rare diseases?" 小节：引用 Bareja 2026（规模不能稳定预测性能）、Neidlinger 2026（多样性优于体量）、PathoROB（数据量与稳健性相关，ρ = 0.692）、Virchow2 与 Atlas 原文；删去 ρ = 0.71/0.73。第 4 节中"扩大数据量不能弥合跨机构差距"一句一并删除。

**R1-M2** 数字与原文不一致。
**A** 接受。
**C** Virchow 改为"9 种常见癌 + 7 种罕见癌，整体 AUC 0.950，罕见癌 0.937，且各罕见癌之间性能不均"；CONCH 统一为 117 万对；BiomedCLIP 比较删除；Atlas 改引原始报告；MI-VisionShot 的数字删除。

**R1-M3** 无出处的定量论断。
**A** 接受。
**C** 删除"跨机构检索 63%–69% → 18%–44%"、PANDA-PLUS-Bench 的"20–27 个百分点"、"3.25 亿图像块饱和"和 MIDOG Zenodo 的数字。

**R1-M4** 证据分级口径不一致。
**A** 接受。
**C** Box 1 给出以验证设计为准的判定规则；表 2 全部按新规则重定级，并在"级别"列中标注预印本和会议摘要。

**R1-M5** 非组织学证据。
**A** 接受。
**C** COL6 移入 "Outlook"，并注明为成纤维细胞免疫荧光图像；IgG4 拉曼光谱一节删除。

**R1-次要** LoRA 参数比例、Prov-GigaPath 目标函数、图 2(b) 评级。
**C** 删去具体比例；表 1 写明 tile 用 DINOv2、slide 用 MAE；图 2 图注加"Ratings summarize the cited literature and are not measured on a common benchmark"。

### 审稿人 2

**R2-M1** 流行病学数字。
**A** 接受。
**C** 引言第一段整体重写，数字分别来自 Nguengang Wakap 2020、Haendel 2020、Faye 2024、100,000 Genomes 2021 和 Marwaha 2022；网页和新闻来源全部删除。

**R2-M2** 漏判 Hetairos 和 AIOLI 的前瞻性评估。
**A** 接受，这是本轮最重要的修改。
**C** Hetairos 定为 L3（11 个中心，9606 例患者，前瞻性常规诊断评估，周转时间从 12 天缩短到 12 分钟）；AIOLI 定为 L3，同时报告外部 AUC 0.74 和与乙肝鉴别 AUC 0.42。摘要、"What the evidence shows"、"Reporting guidelines, regulation and prospective evidence"、结论、图 4 图注、图 5 图注和表 2 同步修改。核心表述由"前瞻性评估空白"改为"已有前瞻性准确性评估，尚无临床效用证据"。

**R2-M3** 无法核实的疾病条目；炎症性肠病定位。
**A** 接受。
**C** 删除血管肉瘤、尤文肉瘤 MIL、AI(H)、利什曼病和 NTRK 联邦平台；炎症性肠病改为"可借鉴的转化模板"，不计入罕见病证据统计。

**R2-M4** 儿科罕见肿瘤比例方向写反。
**C** 改为"rare cancers … account for more than 70% of cancers in paediatric oncology"。

**R2-M5** 甲基化分类器的数字。
**C** 删除 0.65% 与 61%；保留 Capper 2018、Koelsche 2021 原文，并以定性方式讨论。

### 审稿人 3

**R3-M1** 监管来源。
**C** 删除 Artera、Ibex 和 Innolitics；改引 FDA DEN200080、FDA PCCP 最终指南（2024 年 12 月）、EU AI Act。新增一句："Current authorizations are for locked algorithms with assistive labelling, which fits poorly with rare disease models that need to be updated as cases accumulate."

**R3-M2** MASAI 作者。
**C** 拆分为 Lång 2023 *Lancet Oncol.* 和 Hernström 2025 *Lancet Digit. Health* 两条。

**R3-M3** 补引 Campanella 2025 静默试验。
**C** 已补入 "From discrimination to clinical evidence" 和 "When to fine-tune the full model" 两节。

**R3-M4** 注册试验信息。
**C** 删除 LEAP（实际入组 10 例，病种与稿件描述不符）；其余 3 项按注册库原始标题和预计样本量引用，并注明"none addresses a rare disease"。

**R3-M5** 补入 STARD-AI。
**C** 补入 Box 2 第 10 条和正文报告规范段落。

**R3-M6** 全球可及性数字。
**C** 删除"300 美元""4–6 倍""92%–98%"等无法核实的数字，保留 Bai 2025。

### 魔鬼代言人

**DA-1** "瓶颈不在表征"自相矛盾。
**A** 部分接受。我们仍然认为证据设计是最被低估的瓶颈，但同意表征稳健性同样未解决。
**C** 结论改为："the decisive factors [are] adaptation strategy, cross-site reliability and clinical evidence rather than model size"，并明确列出"current models encode the medical centre of origin strongly enough that it can be predicted from their embeddings"。

**DA-2** "系统梳理"缺乏方法学。
**A** 接受。
**C** 引言末段改为 "This is a narrative review rather than a systematic review…"，检索式与纳入标准移入 `07_Supplementary_Information_EN.md`。

**DA-3** 替代解释（置信区间、小测试集）。
**C** Box 2 第 1、3 条要求报告每类样本数与 95% 置信区间。

**DA-4** 缺失的利益相关方视角。
**A** 接受，篇幅所限只做部分补充。
**C** Box 3 第 7 条加入以注册库为单位的前瞻性设计；成本–效果评价的缺失写入附录表 S3。患者组织视角建议作者在终稿中补一句，并引用本人团队或合作注册库的实践。

---

## 三、图形重绘要求（作者需完成）

修订稿只修改了图注，原 PDF 中的图形文件需要按以下要求重绘。

| 图 | 必须修改的内容 | 建议规格 |
|---|---|---|
| 图 1 框架图 | 右侧七项约束不变；适配层顺序改为"zero-shot → prototype/retrieval → linear probe/MIL → PEFT/prompt → full FT"，与正文一致 | 双栏宽 180 mm；Arial/Helvetica 7–8 pt；色盲友好配色 |
| 图 2 适配策略 | (b) 图注加"基于文献的综合判断"；删去 LoRA"0.1%–2%"等无出处的刻度 | 同上 |
| 图 3 域偏移 | (b) 只保留三组可核实数字：PathoROB 中心可预测性 88%–98%；肾脏罕见病变精度最多下降 70.3%、适配后最多恢复 63.4%；淋巴瘤分布内 >80% → 分布外约 60%。删除 PANDA-PLUS-Bench 与 MIDOG 的数字；相对降幅与绝对降幅分色表示 | 同上 |
| 图 4 证据图谱 | **L3 列新增两个实心点：CNS 肿瘤（Hetairos）和自身免疫性肝炎（AIOLI）**；删除 IgG4、利什曼病、血管肉瘤、尤文 MIL 和 NTRK；COL6 移出组织学矩阵；炎症性肠病移入"转化模板"侧栏 | 同上 |
| 图 5 路线图 | S3 阶段标注"reached for two disease groups (CNS tumours, autoimmune hepatitis)"；S4–S5 保持空白；底部规范层加入 STARD-AI | 同上 |

提交要求：矢量格式（PDF/EPS/AI）或 ≥300 dpi 的 TIFF；每张图单独成文件；图中文字不小于 5 pt；避免红绿配色。

---

## 四、作者仍需完成的事项

1. 填写作者、单位、ORCID、通讯作者信息，以及基金、致谢和 CRediT 贡献。
2. 申报利益冲突，尤其是与病理 AI 公司的雇佣、咨询或持股关系。
3. 逐条阅读修订稿中的预印本和会议摘要（已在参考文献中标注），决定是否保留。
4. 重绘图 1–5，并按附录模板补全附录表 S1–S3。
5. 在 *Nature Medicine* 官网确认当前 Review 的字数与展示项上限，并通过投稿系统提交预投稿询问。
