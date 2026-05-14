# 双模型协作计划

本项目由两个模型协作完成：

- `gpt-5.5`：高级模型，负责方案设计、候选工具筛选标准、复杂失败诊断、结果审查、最终方案收敛。
- `deepseek-v4-pro`：执行模型，运行在 Claude Code 中，负责重复性执行、候选工具安装尝试、命令记录、原始输出整理、基础问题归档。

核心原则：`deepseek-v4-pro` 多做可验证的机械工作，`gpt-5.5` 少量介入但负责关键判断。

## 协作边界

### 分工原则

`deepseek-v4-pro` 可以承担更多工作，但任务必须满足三个条件：

1. 结果可由文件、日志、命令输出或统计指标复核。
2. 不需要它做最终路线判断。
3. 不会覆盖样本、评审结论或其他模型已经产出的文件。

更具体地说，`deepseek-v4-pro` 是执行和证据整理角色；`gpt-5.5` 是任务拆分、质量门禁和方案收敛角色。

### gpt-5.5 负责

1. 制定和更新整体评估标准。
2. 从候选工具列表中选择优先测试顺序。
3. 判断某个工具失败后是否值得继续修复。
4. 审查转换结果中的结构性问题：
   - 标题层级是否可信。
   - 条款编号是否完整。
   - 表格是否可用于后续 agent 理解。
   - 图片、公式、脚注是否需要单独处理。
5. 设计后处理脚本策略。
6. 最终确定主方案、兜底方案和输出规范。
7. 写最终 `README.md` 操作说明和批处理方案。

### deepseek-v4-pro 负责

1. 按任务卡执行具体命令。
2. 克隆或安装候选 GitHub 项目。
3. 对同一个样本 PDF 跑转换命令。
4. 保存原始输出，不做主观改写。
5. 记录安装日志、运行日志、错误日志。
6. 填写基础评审模板中的客观字段。
7. 统计转换结果的可复核指标：
   - Markdown 行数和字符数。
   - 标题数量和标题层级分布。
   - 表格数量。
   - 图片引用数量。
   - 是否包含标准号、标准名称、目录、前言、范围、规范性引用文件。
   - 是否出现明显字符拆分，例如 `GB / T 1 3 5 9 4`。
   - 是否出现页眉页脚重复、空行过多、乱码或异常符号。
8. 按明确规则执行轻量后处理实验：
   - 保存清洗前后的文件。
   - 保存 diff 或变更说明。
   - 不把清洗结果标记为最终方案。
9. 做 API 连通性和小样本测试：
   - 查询模型列表。
   - 发极短文本请求。
   - 对单页截图或小图做一次视觉请求。
   - 记录响应格式、错误码、耗时和 token 用量。
10. 汇总每个工具或模型的：
   - 是否安装成功。
   - 是否生成 Markdown。
   - 输出文件路径。
   - 明显错误。
   - 依赖问题。
   - 运行命令。

### deepseek-v4-pro 可扩展承担的任务

这些工作优先交给 `deepseek-v4-pro`：

1. 新候选工具的安装、试跑和日志整理。
2. 已有候选工具在新样本 PDF 上的重复试跑。
3. 输出文件的客观统计和片段摘录。
4. 把失败信息整理成 `candidates/<tool-name>/NOTES.md`。
5. 按模板起草 `reviews/<tool-name>.md` 的客观部分。
6. 根据明确规则运行后处理脚本，并生成清洗前后对比。
7. 检查文档中的命令是否能在本地实际执行。
8. 对在线模型接口做低成本连通性测试。

这些工作仍由 `gpt-5.5` 负责：

1. 决定是否淘汰候选方案。
2. 判断转换质量是否足够给后续 agent 使用。
3. 设计最终 PDF 到 Markdown 的 pipeline。
4. 制定 API 调用预算和批量处理策略。
5. 审查可能改变标准语义的后处理规则。
6. 合并多工具、多模型实验结论。
7. 决定何时提交和推送 GitHub。

## 禁止事项

### deepseek-v4-pro 不要做

- 不要覆盖已有候选工具输出。
- 不要删除样本 PDF。
- 不要删除其他模型创建的文件。
- 不要在未记录原始输出前手工清洗 Markdown。
- 不要擅自决定最终方案。
- 不要为了让结果看起来更好而静默修改转换产物。
- 不要把验证码识别、绕过验证码作为任务。
- 不要直接改写 `reviews/round-*-summary.md` 的最终结论。
- 不要把 API key 写入仓库文件、日志或命令记录。
- 不要在没有预算说明时对整份 PDF 发起大规模模型调用。
- 不要对标准正文做不可追溯的语义改写。
- 不要使用 `git add .`、`git commit` 或 `git push`，除非任务卡明确授权。

### gpt-5.5 尽量不要做

- 不要把大量重复安装和试跑工作都放在高级模型里完成。
- 不要在没有原始输出证据时直接判断工具优劣。
- 不要过早写复杂后处理脚本。

## deepseek-v4-pro 任务卡护栏

每次给 `deepseek-v4-pro` 派任务时，默认附带下面这段约束：

```text
你只负责执行、记录和生成草稿，不做最终方案判断。
不得删除或覆盖已有文件。
新增文件必须放在任务卡指定目录。
不得把 API key 写入仓库文件或日志。
失败时保留完整错误信息并停止，不要自行扩大任务范围。
不要使用 git add、git commit、git push，除非任务卡明确授权。
```

推荐任务卡格式：

```text
任务目标：

输入文件：

允许写入：

禁止修改：

执行命令建议：

需要记录：

停止条件：

交付物：
```

## 推荐目录约定

每个候选工具使用同名目录：

```text
candidates/<tool-name>/
  NOTES.md
  install.log
  run.log

outputs/<tool-name>/
  GBT-13594-2025.md
  GBT-13594-2025.cleaned.md
  assets/
  raw/

reviews/<tool-name>.md
```

命名规则：

- `<tool-name>` 使用小写英文和连字符，例如 `marker`、`docling`、`nougat`。
- 首轮输出统一命名为 `GBT-13594-2025.md`。
- 工具原始中间文件放入 `outputs/<tool-name>/raw/`。
- 图片和表格截图放入 `outputs/<tool-name>/assets/`。

## 阶段拆分

### 阶段 1：基线与评审框架

`gpt-5.5`：

1. 确认评估维度。
2. 设计 `reviews/review-template.md`。
3. 指定样本 PDF 和统一输出目录。

`deepseek-v4-pro`：

1. 运行以下检查命令并记录结果：

```sh
file "samples/GBT 13594-2025.pdf"
ls -lh "samples/GBT 13594-2025.pdf"
md5 "samples/GBT 13594-2025.pdf"
```

2. 如本地有 `pdfinfo`，记录页数和元数据：

```sh
pdfinfo "samples/GBT 13594-2025.pdf"
```

3. 把结果写入 `candidates/baseline/NOTES.md`。

交付物：

- `candidates/baseline/NOTES.md`

### 阶段 2：候选工具搜索与初筛

`gpt-5.5`：

1. 给出候选工具优先级。
2. 判断哪些工具适合先试。
3. 排除明显不合适的方案，例如只适合英文论文、长期未维护且安装复杂、强依赖 GPU。

`deepseek-v4-pro`：

1. 根据候选清单为每个工具建立目录。
2. 记录项目来源、安装方式、主要依赖。
3. 不需要深度判断，只做客观信息整理。

交付物：

```text
candidates/<tool-name>/NOTES.md
```

`NOTES.md` 至少包含：

```text
source:
license:
install:
run:
expected output:
known limitations:
status:
```

### 阶段 3：单工具试跑

`gpt-5.5`：

1. 给每个工具一张清晰任务卡。
2. 处理 `deepseek-v4-pro` 无法解决的关键失败。
3. 决定是否继续修复安装失败的工具。

`deepseek-v4-pro`：

1. 按任务卡运行安装命令。
2. 跑 `samples/GBT 13594-2025.pdf`。
3. 把输出保存到 `outputs/<tool-name>/`。
4. 保存完整日志。
5. 填写 `reviews/<tool-name>.md` 的客观部分。

交付物：

```text
candidates/<tool-name>/install.log
candidates/<tool-name>/run.log
outputs/<tool-name>/GBT-13594-2025.md
reviews/<tool-name>.md
```

### 阶段 4：结果审查

`gpt-5.5`：

1. 对候选工具输出做结构审查。
2. 按评分表给出评分。
3. 提取每个工具最主要的失败模式。
4. 选出 1 到 2 个进入二轮测试的方案。

`deepseek-v4-pro`：

1. 根据 `gpt-5.5` 指令截取指定章节、表格、附录输出片段。
2. 统计明显乱码、空行、页眉页脚重复等客观问题。
3. 不做最终评分，只补充证据。

交付物：

```text
reviews/<tool-name>.md
reviews/round-1-summary.md
```

### 阶段 5：后处理方案

`gpt-5.5`：

1. 设计清洗规则。
2. 判断是否需要脚本恢复条款层级。
3. 定义最终 Markdown 格式规范。

`deepseek-v4-pro`：

1. 按明确规则实现或运行简单后处理脚本。
2. 保存清洗前后 diff。
3. 对多个样本重复执行同一脚本。

交付物：

```text
scripts/postprocess_standard_md.*
outputs/<tool-name>/GBT-13594-2025.cleaned.md
reviews/postprocess-notes.md
```

### 阶段 6：最终方案固化

`gpt-5.5`：

1. 选择主工具和兜底工具。
2. 更新 `README.md` 为正式操作说明。
3. 写清楚批量转换流程和失败处理策略。

`deepseek-v4-pro`：

1. 按最终说明重新跑一次端到端流程。
2. 记录实际命令输出。
3. 报告文档和实际命令不一致的地方。

交付物：

```text
README.md
scripts/convert_standard_pdf.sh
reviews/final-decision.md
```

## deepseek-v4-pro 任务卡模板

把下面模板复制给 Claude Code 中的 `deepseek-v4-pro` 使用。建议调用方式：

```sh
claude --print --model deepseek-v4-pro --permission-mode bypassPermissions '<任务内容>'
```

注意：首次实测中，`--permission-mode dontAsk` 会自动拒绝 Bash，无法执行安装和转换；`bypassPermissions` 是当前可用的执行方式。另一次 `deepseek-v4-pro` 调用在预算上限内没有完成落盘，因此执行模型任务应设置明确的预算、超时和“必须先创建日志文件”的要求。

```text
你在项目目录 /Users/cui/Documents/pytest/standard-pdf-md-lab 工作。

任务：测试候选工具 <tool-name> 对 `samples/GBT 13594-2025.pdf` 的 PDF 转 Markdown 效果。

要求：
1. 不要删除或覆盖已有文件。
2. 所有输出放到 `outputs/<tool-name>/`。
3. 安装日志保存到 `candidates/<tool-name>/install.log`。
4. 运行日志保存到 `candidates/<tool-name>/run.log`。
5. 原始 Markdown 命名为 `outputs/<tool-name>/GBT-13594-2025.md`。
6. 如果工具生成 assets，放到 `outputs/<tool-name>/assets/`。
7. 如果失败，不要反复盲试超过 3 次，把错误写入 `candidates/<tool-name>/NOTES.md`。
8. 不要对原始 Markdown 做人工修复。
9. 最后填写 `reviews/<tool-name>.md` 的客观信息部分。

完成后汇报：
- 安装是否成功。
- 运行命令。
- 输出文件路径。
- 主要错误或明显问题。
- 你改动或新增了哪些文件。
```

## 交接格式

### deepseek-v4-pro 给 gpt-5.5 的汇报格式

```text
工具：<tool-name>
状态：成功 / 失败 / 部分成功
安装命令：
运行命令：
输出文件：
日志文件：
明显问题：
新增文件：
需要高级模型判断的问题：
```

### gpt-5.5 给 deepseek-v4-pro 的指令格式

```text
目标：
工具：
输入：
输出目录：
必须保存的日志：
最多尝试次数：
失败时停止条件：
完成后汇报格式：
```

## 质量门禁

某个候选工具进入二轮测试前，至少满足：

- 能稳定生成 Markdown 或接近 Markdown 的结构化文本。
- 正文主顺序基本正确。
- 标准条款编号没有大面积丢失。
- 不依赖不可控的在线服务。
- 批处理成本可以接受。

最终方案必须满足：

- 端到端命令可复现。
- 原始输出和清洗输出分开保存。
- 失败时能判断是安装问题、PDF 问题、OCR 问题还是后处理问题。
- 输出 Markdown 对后续 agent 足够友好。
