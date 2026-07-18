<script setup lang="ts">
import { computed, ref } from 'vue'

type ActionItem = {
  owner: string | null
  task: string
  deadline: string | null
  content?: string | null
}

type MeetingSummary = {
  meeting_time: string | null
  participants: string[]
  speakers: string[]
  topics: string[]
  conclusions: string[]
  action_items: ActionItem[]
  risks: string[]
  next_steps: string[]
}

const sampleText = `会议标题：订单履约系统二期评审会
会议时间：2026年7月16日 周四 14:00-16:10
参会人员：张伟（产品负责人）、李娜、王磊、赵敏、陈晨、刘洋
主持人：张伟

会议议题：
1. 确认订单拆单策略和库存锁定方案
2. 讨论支付回调延迟对履约链路的影响
3. 明确灰度上线范围、监控指标和回滚预案

张伟：今天主要确认二期履约方案，目标是月底前支持多仓拆单和异常订单人工兜底。
李娜：产品侧确认拆单规则按仓库优先、时效次之执行，特殊大客户订单需要保留人工审核入口。
王磊：技术方案上，库存锁定服务会在支付成功后写入锁定流水；如果支付回调超过 5 分钟，会触发补偿任务。
赵敏：测试发现沙箱环境里支付回调偶发延迟，可能导致订单状态停留在待确认，影响客服查询。

关键结论：
- 拆单策略最终采用“仓库优先 + 时效兜底”，大客户订单保留人工审核。
- 灰度范围先限定华东仓 10% 流量，稳定 48 小时后再扩大到 50%。

待办事项：
1. 李娜负责补充大客户人工审核的产品交互，截止 7月18日 18:00。
2. 王磊完成库存锁定接口和补偿任务联调，DDL：7月22日。
3. 赵敏跟进支付回调延迟的自动化回归用例，最晚下周三。

风险与问题：
- 支付渠道回调延迟仍存在不确定性，可能影响订单状态一致性。
- 华东仓库存服务当前 QPS 余量不足，灰度扩大时存在瓶颈。

下一步安排：
- 明天上午同步支付渠道补偿接口人，确认重试频率和告警阈值。
- 下周一进行第一轮联调评审。`

const emptySummary = (): MeetingSummary => ({
  meeting_time: null,
  participants: [],
  speakers: [],
  topics: [],
  conclusions: [],
  action_items: [],
  risks: [],
  next_steps: [],
})

const rawText = ref('')
const summary = ref<MeetingSummary | null>(null)
const isLoading = ref(false)
const errorMessage = ref('')
const copyMessage = ref('')

const markdown = computed(() => {
  if (!summary.value) {
    return '解析后将在这里生成 Markdown 纪要。'
  }

  const data = summary.value
  return [
    '# 会议纪要',
    '',
    `- 会议时间：${data.meeting_time || '未识别'}`,
    `- 参会人员：${formatInlineList(data.participants)}`,
    `- 发言人：${formatInlineList(data.speakers)}`,
    '',
    '## 会议议题',
    formatMarkdownList(data.topics),
    '',
    '## 关键结论',
    formatMarkdownList(data.conclusions),
    '',
    '## 待办事项',
    formatActionItems(data.action_items),
    '',
    '## 风险与问题',
    formatMarkdownList(data.risks),
    '',
    '## 下一步安排',
    formatMarkdownList(data.next_steps),
  ].join('\n')
})

function useSampleText() {
  rawText.value = sampleText
  errorMessage.value = ''
}

async function generateSummary() {
  errorMessage.value = ''
  copyMessage.value = ''

  if (!rawText.value.trim()) {
    errorMessage.value = '请输入会议原文。'
    return
  }

  isLoading.value = true
  try {
    const response = await fetch('/api/meetings/parse', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ rawText: rawText.value }),
    })

    if (!response.ok) {
      throw new Error('生成纪要失败，请检查后端服务是否已启动。')
    }

    summary.value = await response.json()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '生成纪要失败。'
  } finally {
    isLoading.value = false
  }
}

function addActionItem() {
  ensureSummary().action_items.push({ owner: '', task: '', deadline: '' })
}

function deleteActionItem(index: number) {
  summary.value?.action_items.splice(index, 1)
}

async function copyMarkdown() {
  copyMessage.value = ''
  await navigator.clipboard.writeText(markdown.value)
  copyMessage.value = '已复制 Markdown。'
}

function downloadMarkdown() {
  const blob = new Blob([markdown.value], { type: 'text/markdown;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = 'meeting-minutes.md'
  link.click()
  URL.revokeObjectURL(url)
}

function ensureSummary() {
  if (!summary.value) {
    summary.value = emptySummary()
  }
  return summary.value
}

function formatInlineList(items: string[]) {
  return items.length ? items.join('、') : '未识别'
}

function formatMarkdownList(items: string[]) {
  return items.length ? items.map((item) => `- ${item}`).join('\n') : '- 无'
}

function formatActionItems(items: ActionItem[]) {
  if (!items.length) {
    return '- 无'
  }

  return ['| 负责人 | 任务 | 截止时间 |', '| --- | --- | --- |']
    .concat(items.map((item) => `| ${item.owner || '-'} | ${item.task || '-'} | ${item.deadline || '-'} |`))
    .join('\n')
}
</script>

<template>
  <main class="page">
    <header class="header">
      <div>
        <h1>会议纪要整理器</h1>
        <p>粘贴会议原文，生成结构化纪要，并维护待办事项。</p>
      </div>
      <div class="header-actions">
        <button type="button" class="secondary" @click="useSampleText">示例会议内容</button>
        <button type="button" :disabled="isLoading || !rawText.trim()" @click="generateSummary">
          {{ isLoading ? '生成中...' : '生成纪要' }}
        </button>
      </div>
    </header>

    <section class="grid two-columns">
      <div class="card">
        <div class="card-title">
          <h2>会议原文</h2>
          <span>{{ rawText.length }} 字</span>
        </div>
        <textarea v-model="rawText" placeholder="请输入或粘贴中文会议原文"></textarea>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      </div>

      <div class="card">
        <div class="card-title">
          <h2>结构化纪要</h2>
        </div>
        <div v-if="summary" class="summary-list">
          <section>
            <h3>基本信息</h3>
            <p><strong>会议时间：</strong>{{ summary.meeting_time || '未识别' }}</p>
            <p><strong>参会人员：</strong>{{ formatInlineList(summary.participants) }}</p>
            <p><strong>发言人：</strong>{{ formatInlineList(summary.speakers) }}</p>
          </section>

          <section>
            <h3>会议议题</h3>
            <ul v-if="summary.topics.length">
              <li v-for="topic in summary.topics" :key="topic">{{ topic }}</li>
            </ul>
            <p v-else class="muted">暂无</p>
          </section>

          <section>
            <h3>关键结论</h3>
            <ul v-if="summary.conclusions.length">
              <li v-for="conclusion in summary.conclusions" :key="conclusion">{{ conclusion }}</li>
            </ul>
            <p v-else class="muted">暂无</p>
          </section>

          <section>
            <h3>风险与问题</h3>
            <ul v-if="summary.risks.length">
              <li v-for="risk in summary.risks" :key="risk">{{ risk }}</li>
            </ul>
            <p v-else class="muted">暂无</p>
          </section>

          <section>
            <h3>下一步安排</h3>
            <ul v-if="summary.next_steps.length">
              <li v-for="step in summary.next_steps" :key="step">{{ step }}</li>
            </ul>
            <p v-else class="muted">暂无</p>
          </section>
        </div>
        <p v-else class="empty">生成后显示结构化纪要。</p>
      </div>
    </section>

    <section class="card">
      <div class="card-title">
        <h2>待办事项</h2>
        <button type="button" class="secondary" @click="addActionItem">新增待办</button>
      </div>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>负责人</th>
              <th>任务</th>
              <th>截止时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody v-if="summary?.action_items.length">
            <tr v-for="(item, index) in summary.action_items" :key="index">
              <td><input v-model="item.owner" placeholder="负责人" /></td>
              <td><input v-model="item.task" placeholder="任务内容" /></td>
              <td><input v-model="item.deadline" placeholder="截止时间" /></td>
              <td><button type="button" class="danger" @click="deleteActionItem(index)">删除</button></td>
            </tr>
          </tbody>
          <tbody v-else>
            <tr>
              <td colspan="4" class="empty-cell">暂无待办事项，可点击“新增待办”。</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <section class="card">
      <div class="card-title">
        <h2>Markdown 预览</h2>
        <div class="inline-actions">
          <span v-if="copyMessage" class="success">{{ copyMessage }}</span>
          <button type="button" class="secondary" :disabled="!summary" @click="copyMarkdown">复制 Markdown</button>
          <button type="button" :disabled="!summary" @click="downloadMarkdown">下载 Markdown</button>
        </div>
      </div>
      <pre class="markdown-preview">{{ markdown }}</pre>
    </section>
  </main>
</template>
