# 参考文献核查表（原稿 106 条）

**核查方法。** 每条参考文献都通过以下至少一种渠道核对：Crossref REST API（DOI 元数据与摘要）、arXiv API（编号、题名、作者、摘要）、期刊官网全文（用于核对关键数字）、ClinicalTrials.gov API v2（注册号）。核查日期为 2026 年 10 月 13 日。

**状态代码**

- ✅ 已核实：题名、作者、出处一致，被引内容与原文相符。
- ⚠️ 需更正：文献存在，但作者、题名、出处或被引内容有误。
- ❌ 无法核实或不合格：找不到原始出处，或属于新闻、网页、博客，或只有题名没有可定位信息。
- ➡️ 处理方式：保留、更正、替换或删除（对应修订稿 `02_Manuscript_NatMed_Review_EN.md`）。

**汇总**

| 状态 | 条数 | 说明 |
|---|---|---|
| ✅ 已核实 | 38 | 其中 37 条在修订稿中保留，1 条为精简篇幅删除 |
| ⚠️ 需更正 | 43 | 作者、题名、出处等元数据错误，或被引内容与原文不符、张冠李戴；严重错误见第 17、58 条，错引见第 18、61 条 |
| ❌ 无法核实或不合格 | 25 | 网页、新闻、博客或灰色文献 4 条；无出处或无法定位 21 条 |

---

## 逐条核查

| # | 原稿条目（简写） | 状态 | 核查发现 | 处理 |
|---|---|---|---|---|
| 1 | EURORDIS Rare Disease Day 2026 网页 | ❌ | 宣传网页，非学术来源 | 替换为 Nguengang Wakap 2020、Faye 2024 |
| 2 | EPRS At a Glance 779215 | ❌ | 灰色文献，且与第 1 条重复 | 删除 |
| 3 | News Medical / Medical Research NSW | ❌ | 新闻稿；"近 60% 无确诊"无学术出处 | 替换为 Smedley 2021、Marwaha 2022 |
| 4 | Chada A, Arch Pathol Lab Med 2025 | ❌ | Crossref 未检得 | 替换为 Wilson 2018 *Lancet* |
| 5 | Rahman A, Expert Rev Mol Diagn 2025 | ❌ | 未检得 | 删除 |
| 6 | Bilal M, arXiv:2502.08333 | ⚠️ | 文献存在，但被当作 Atlas、规模饱和等一手结论的来源 | 改引原始研究，本条删除 |
| 7 | Chen RJ, UNI, Nat Med 2024 | ✅ | — | 保留 |
| 8 | Vorontsov E, Virchow, Nat Med 2024 | ⚠️ | 文献无误；正文"17 种常见癌，AUC 0.949"有误，原文为 9 种常见癌 + 7 种罕见癌，整体 0.950，罕见癌 0.937 | 更正数字 |
| 9 | Virchow2, arXiv:2408.00738 | ⚠️ | 第一作者是 Zimmermann E，不是 Vorontsov E | 更正 |
| 10 | Xu H, Prov-GigaPath, Nature 2024 | ✅ | — | 保留 |
| 11 | Lu MY, CONCH, Nat Med 2024 | ⚠️ | 文献无误；正文中训练对数前后不一致（110 万与 117 万），原文为 117 万 | 统一为 117 万 |
| 12 | Huang Z, PLIP, Nat Med 2023 | ✅ | — | 保留 |
| 13 | Zhou Y, KEEP, arXiv/Cancer Cell 2026 | ⚠️ | 第一作者是 Zhou X；正式发表于 *Cancer Cell* 44, 777–791 (2026)，题名为 "Knowledge-enhanced pretraining for vision-language pathology foundation model on cancer diagnosis" | 更正 |
| 14 | Lu MY, PathChat, Nature 2024 | ✅ | — | 保留 |
| 15 | Filiot A, Phikon medRxiv + Phikon-v2 | ⚠️ | 两篇文献合并为一条 | 拆分为两条 |
| 16 | Dippel J, RudolfV, arXiv 2024 | ⚠️ | 合著者写成 "Vaidya A, Zhang K"，arXiv 显示为 Feulner B、Winterhoff T 等 | 更正 |
| 17 | Nat Commun 2026, doi:…76004-6 | ⚠️ **严重** | 缺作者（应为 Bareja R 等）；原文结论是"模型规模与预训练数据量不能稳定预测下游性能"，稿件却引用它支持"规模即能力"（ρ = 0.71/0.73），方向相反 | 更正引用方向 |
| 18 | Neidlinger P, Nat Biomed Eng 2025 | ⚠️ | 文献无误；但"CONCH 超过 BiomedCLIP"被错引到本条 | 改引 CONCH 原文 |
| 19 | Chen RJ, HIPT, CVPR 2022 | ✅ | — | 保留 |
| 20 | Ding T, TITAN, Nat Med 2025 | ✅ | 补卷期：31, 3749–3761 | 保留 |
| 21 | Lu MY, MI-Zero, CVPR 2023 | ⚠️ | MI-VisionShot 的结果被归到本条，二者是不同的工作 | 删去 MI-VisionShot 数字 |
| 22 | Lu MY, CLAM, Nat Biomed Eng 2021 | ✅ | — | 保留 |
| 23 | Shao Z, TransMIL, NeurIPS 2021 | ✅ | — | 保留 |
| 24 | Zhang H, DTFD-MIL, CVPR 2022 | ✅ | — | 精简删除 |
| 25 | Hu EJ, LoRA, ICLR 2022 | ✅ | — | 保留 |
| 26 | Jia M, VPT, ECCV 2022 | ✅ | — | 保留 |
| 27 | Zhou K, CoOp, IJCV 2022 | ✅ | — | 保留 |
| 28 | Lee J, Comput Biol Med 2025 | ✅ | — | 保留 |
| 29 | Ganz J, "Is self-supervision enough?" | ⚠️ | 缺出处，应为 *Bildverarbeitung für die Medizin 2025*, 63–68 | 补全 |
| 30 | 肾脏基准 arXiv:2603.15967 | ⚠️ | 缺作者（Kasireddy HR 等） | 补全 |
| 31 | Spyretos N, bioRxiv 2026 | ⚠️ | 作者名缩写应为 Spyretos C | 更正 |
| 32 | Cai X, IBDAIM, Int J Med Inform 2025 | ❌ | 未检得 | 删除 |
| 33 | 淋巴瘤 MIL 基准 arXiv:2512.14640 | ⚠️ | 缺作者（Umer RM 等）；内容核实无误 | 补全 |
| 34 | MIDOG 2025 LoRA-UNI，Zenodo | ❌ | 无 DOI 和作者，内容无法核实 | 删除，相关数字一并删除 |
| 35 | PEFT 核分裂象 arXiv:2509.16935 | ⚠️ | 缺作者（Ramchandani L 等） | 补全 |
| 36 | "Single-GPU…" + Oskouei A, Algorithms 2025 | ⚠️ | 前者无法定位，后者核实存在；两条被合并 | 删除前者 |
| 37 | PAMT, arXiv:2403.12537 | ⚠️ | arXiv 核实存在；"Med Image Anal 2026"无法核实 | 只保留 arXiv |
| 38 | He D, PathPT, Nat Commun 2026 | ✅ | 0.679 BACC 经原文核实 | 保留 |
| 39 | Kömen J, PathoROB, Nat Commun 2026 | ✅ | 88%–98% 中心可预测性经原文核实；补卷号 17, 5218 | 保留 |
| 40 | Kömen J, arXiv:2411.05489 | ✅ | — | 保留 |
| 41 | arXiv:2501.18055 | ⚠️ | 第一作者是 de Jong ED，不是 Kömen J | 更正 |
| 42 | Matsui K, npj Digit Med 2025 | ⚠️ | 第一作者缩写为 Matsui I；70.3%、55.9 → 20.2、63.4% 均经原文核实 | 更正 |
| 43 | PANDA-PLUS-Bench 2026 | ❌ | 无作者、无出处 | 删除，"20–27 个百分点"一并删除 |
| 44 | Khan A, Sci Rep 2026 | ⚠️ | 第一作者缩写为 Khan U | 更正 |
| 45 | StainLUT, npj Digit Med | ⚠️ | 缺作者（Wang J 等）；卷 9 (2026) | 补全 |
| 46 | Nguyen T, fmMAP, PMLR 316 | ❌ | 无法核实 | 删除 |
| 47 | FLEX, Nat Commun 2025 | ⚠️ | 缺作者（Huang Y 等） | 补全 |
| 48 | UAD-FM, npj Digit Med 2025 | ⚠️ | 缺作者（Lou S 等） | 补全 |
| 49 | 跨中心检索, Med Image Anal 2026 | ⚠️ | 缺作者（Zhu X 等）与卷号 113, 104213 | 补全 |
| 50 | 解释稳定性 arXiv:2608.07062 | ⚠️ | 缺作者（Bahumanya RG 等） | 补全 |
| 51 | 分布稳健性边际 arXiv:2607.25497 | ⚠️ | 缺作者（Grisi C 等） | 补全 |
| 52 | Thiesen J, PMID:40585079 | ⚠️ | 核实为 medRxiv 预印本（doi:10.1101/2025.06.10.25328700），867 张 WSI | 改为预印本格式，定级 L2（预印本） |
| 53 | Machado A, Ewing MIL + VLM | ❌ | 未检得 | 删除 |
| 54 | Lee J, Cancer Res 摘要 LB117 | ❌ | 会议摘要，无法核实 | 删除 |
| 55 | 子宫平滑肌肉瘤, Med Image Anal 2025 | ⚠️ | 缺作者（Li Q 等），卷 105, 103692 | 补全 |
| 56 | Cross WC, J Pathol Clin Res 2025 | ⚠️ | 文献存在；"训练错误率 0.65%，真实世界 61%"无一手出处 | 删除该数字 |
| 57 | 瑞典儿童脑肿瘤 arXiv:2409.01330 | ⚠️ | 缺作者（Tampu IE 等） | 补全 |
| 58 | "Hetairosis", Nat Cancer 2026 | ⚠️ **严重** | 模型名应为 Hetairos；原文报告了前瞻性常规诊断评估（L3），稿件定为 L2；"top-1 75%/top-3 87%"与原文摘要不符（原文：最高置信预测准确率 0.87） | 更正，并据此重写核心论断 |
| 59 | LymphoVision, Blood 2025 | ✅ | ASH 会议摘要；数字核实无误 | 保留，标注为会议摘要，定级 L1 |
| 60 | PTCL, Blood 2025 | ✅ | ASH 会议摘要；外部验证 118 例 | 保留，标注为会议摘要 |
| 61 | 联邦学习综述, CSBJ 2024 | ⚠️ | 文献存在；"儿童 NTRK 联邦平台 94.3%"不是该综述的内容 | 删除该数字 |
| 62 | 肾肿瘤零样本, J Am Soc Cytopathol 2024 | ⚠️ | 实为 *Lab. Invest.* 105, 103043 (2025)，摘要 810 | 更正 |
| 63 | ZEBRA, Kidney Int Rep 2025 | ⚠️ | 实为 *Sci. Rep.* 16, 5072 (2026) | 更正 |
| 64 | AI(H) 2024 | ❌ | 未检得 | 删除 |
| 65 | AIOLI, Virchows Arch 2026 | ⚠️ | 文献存在；稿件未报告外部 AUC 仅 0.74、与乙肝鉴别 AUC 0.42；前瞻性测试属实（L3） | 补报真实性能，定级 L3 |
| 66 | Das A, Am J Pathol 2025 | ✅ | — | 保留 |
| 67 | Rubin DT, Inflamm Bowel Dis | ✅ | 卷 31, 1630–1636 | 保留 |
| 68 | IgG4 拉曼光谱 | ❌ | 未检得，且不是组织学研究 | 删除 |
| 69 | 血吸虫虫卵, JCPSP 2025 | ✅ | 卷 35, 1385–1390；Crossref 未收录作者 | 保留 |
| 70 | 尿路血吸虫机器人显微镜 | ❌ | 无出处 | 删除 |
| 71 | LeishFuNet / DeepLeish | ❌ | 无具体文献 | 删除 |
| 72 | 被忽视热带病视觉架构 | ❌ | 无出处 | 删除 |
| 73 | IGI Global 章节 | ❌ | 无法定位 | 删除 |
| 74 | 罕见神经病 AI 范围综述, 2026 | ✅ | 24% 外部验证经原文核实 | 保留 |
| 75 | TRIPOD+AI, BMJ 2024 | ✅ | — | 保留 |
| 76 | PROBAST+AI, BMJ 2025 | ✅ | — | 保留 |
| 77 | TRUECAM, Nat Biomed Eng 2026 | ✅ | — | 保留 |
| 78 | HER2 保形 + 白血病保形 | ⚠️ | 两条被合并；白血病一篇核实存在（*JCO Clin. Cancer Inform.* 2025）；HER2 与"0.909 → 0.787"无法核实 | 只保留白血病一篇 |
| 79 | 保形预测批判, Artif Intell Med 2026 | ✅ | Kladny K-R 等，卷 180, 103462 | 保留 |
| 80 | REG 2025, arXiv:2609.00866 | ⚠️ | 题名应为 "Benchmarking vision-language models for automated pathology diagnosis and report generation"（Lee Y 等）；内容属实 | 更正 |
| 81 | PathReportEval 2026 | ❌ | 无出处 | 删除 |
| 82 | PathGLS, arXiv:2603.16113 | ✅ | — | 保留 |
| 83 | "Pathology's last exam" 2025 | ❌ | 无出处 | 删除 |
| 84 | TRIPOD-LLM, Nat Med 2025 | ⚠️ | 缺作者与卷期（Gallifant J 等，31, 60–69） | 补全 |
| 85 | FDA DEN200080 | ✅ | — | 保留 |
| 86 | ArteraAI De Novo + PCCP | ❌ | 无官方来源 | 删除，改引 FDA PCCP 指南 |
| 87 | Ibex 510(k) | ❌ | 无官方来源 | 删除 |
| 88 | Innolitics 博客 | ❌ | 咨询公司博客 | 删除 |
| 89 | 专家视角 arXiv:2603.05884 | ✅ | 第一作者 Da Q | 保留 |
| 90 | Lång K, MASAI, Lancet Digit Health 2025 | ⚠️ | 该文第一作者是 Hernström V；Lång K 的是 2023 年 *Lancet Oncol.* 的安全性分析 | 拆分为两条 |
| 91 | LEAP, NCT07203885 | ⚠️ | 注册信息为急性髓系白血病，不是急性早幼粒细胞白血病；实际入组 10 例，已完成 | 删除（样本量过小） |
| 92 | NCT07291362 | ✅ | 存在，预计入组 1000 例；注册标题未写明胃癌 | 保留，不写病种 |
| 93 | INSIGHT-EIC, NCT07060599 | ✅ | 预计入组 480 例 | 保留 |
| 94 | DeepGEM, NCT07110259 | ✅ | 预计入组 950 例 | 保留 |
| 95 | Pati S, FeTS, Nat Commun 2022 | ✅ | — | 保留 |
| 96 | GenoMed4All, medRxiv 2025 | ❌ | 未检得 | 删除 |
| 97 | FedMSAC-Histo, IEEE 2025 | ❌ | 无具体出处 | 删除 |
| 98 | COL6 联邦学习 arXiv:2512.16876 | ⚠️ | 数据是成纤维细胞免疫荧光图像，不是组织病理 | 移入展望并注明模态 |
| 99 | MISO, Nat Commun 2025 | ✅ | — | 保留 |
| 100 | STPath, arXiv:2602.14177 | ✅ | — | 保留 |
| 101 | Multi-Embed, Nat Methods 2026 | ✅ | — | 保留 |
| 102 | 宫颈细胞学紧凑显微镜, Nat Commun 2025 | ✅ | — | 保留 |
| 103 | 宫颈病理 AI 系统综述, Front Oncol 2025 | ❌ | 未检得 | 删除 |
| 104 | Jaume G, HEST-1k, NeurIPS 2024 | ✅ | — | 保留 |
| 105 | RareCollab, arXiv:2602.04058 | ⚠️ | 题名应为 "an LLM-powered framework for multimodal reasoning in Mendelian disease diagnosis"；"UDN top-5 77%"与摘要不符（摘要：890 例中 94% 的诊断基因位于前 10） | 更正 |
| 106 | Alsentzer E, SHEPHERD, NeurIPS 2023 | ⚠️ | 实际发表于 *npj Digit. Med.* 8, 380 (2025)；它是知识图谱少样本模型，不是"罕见病专用基础模型" | 更正出处与定性 |

> 注：汇总行把"文献存在但被引内容有误"的条目计入"需更正"，把"会议摘要但内容核实无误"的条目（59、60）计入"已核实"。

---

## 修订稿新增的已核实文献（节选）

| 文献 | 用途 |
|---|---|
| Nguengang Wakap S 等, *Eur. J. Hum. Genet.* 2020 | 患病率 3.5%–5.9%，6172 种疾病，71.9% 遗传 |
| Faye F 等, *Eur. J. Hum. Genet.* 2024 | 平均诊断时长 4.7 年（6507 名受访者，41 国） |
| 100,000 Genomes Project, *N. Engl. J. Med.* 2021 | 诊断率 25% |
| Gatta G 等, *Lancet Oncol.* 2017 | 罕见癌定义与负担 |
| Ray-Coquard I 等, *Ann. Oncol.* 2012 | 肉瘤初诊与专家复核完全一致率 56% |
| Capper D 等, *Nature* 2018；Koelsche C 等, *Nat. Commun.* 2021 | 甲基化分类器原始文献 |
| Campanella G 等, *Nat. Med.* 2025 | 病理基础模型的前瞻性静默试验（EGFR，AUC 0.890） |
| Sounderajah V 等, STARD-AI, *Nat. Med.* 2025 | 诊断准确性研究报告规范 |
| Hernström V 等, *Lancet Digit. Health* 2025；Lång K 等, *Lancet Oncol.* 2023 | MASAI 试验 |
| Atlas（Alber M 等, arXiv 2025） | 替代二次引用 |
| CHIEF, MUSK, GPFM, PRISM, Hibou | 补全模型谱系 |
| FDA PCCP 最终指南（2024）；EU AI Act（2024/1689） | 监管的官方来源 |

修订稿全部 123 条参考文献的 DOI 或 arXiv 编号，都可以由附带的核查脚本重新生成并复核。
