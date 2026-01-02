<template>
  <v-container fluid class="pa-6">
    <v-row>
        <v-col cols="12">
            <div class="d-flex justify-space-between align-center mb-6 flex-wrap gap-3">
                <div>
                    <h1 class="text-h3 font-weight-bold text-navy mb-2">
                        <v-icon color="purple" size="36" class="mr-2">mdi-brain</v-icon>
                        AI Sales Insights
                    </h1>
                    <p class="text-h6 text-grey-darken-1">Powered by intelligent deal scoring and predictive analytics</p>
                </div>
            </div>
        </v-col>
    </v-row>

    <!-- Loading State -->
    <v-progress-linear v-if="loading" indeterminate color="purple"></v-progress-linear>

    <!-- Main Insights -->
    <v-row v-if="!loading && insights">
      <!-- Pipeline Health Score -->
      <v-col cols="12" md="4">
        <v-card elevation="4" class="gradient-card purple-gradient">
          <v-card-text class="text-center pa-6">
            <v-icon size="48" color="white" class="mb-2">mdi-heart-pulse</v-icon>
            <div class="text-h2 font-weight-bold text-white mb-2">
              {{ insights.pipeline_health_score }}
            </div>
            <div class="text-h6 text-white opacity-90">Pipeline Health</div>
            <v-progress-linear
              :model-value="insights.pipeline_health_score"
              color="white"
              height="8"
              rounded
              class="mt-4"
            ></v-progress-linear>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Win Rate -->
      <v-col cols="12" md="4">
        <v-card elevation="4" class="gradient-card success-gradient">
          <v-card-text class="text-center pa-6">
            <v-icon size="48" color="white" class="mb-2">mdi-trophy</v-icon>
            <div class="text-h2 font-weight-bold text-white mb-2">
              {{ insights.win_rate }}%
            </div>
            <div class="text-h6 text-white opacity-90">Win Rate</div>
            <div class="text-caption text-white opacity-80 mt-2">
              {{ insights.won_deals }} won / {{ insights.total_deals }} total
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Pipeline Value -->
      <v-col cols="12" md="4">
        <v-card elevation="4" class="gradient-card primary-gradient">
          <v-card-text class="text-center pa-6">
            <v-icon size="48" color="white" class="mb-2">mdi-currency-usd</v-icon>
            <div class="text-h2 font-weight-bold text-white mb-2">
              ${{ formatCurrency(insights.total_pipeline_value) }}
            </div>
            <div class="text-h6 text-white opacity-90">Pipeline Value</div>
            <div class="text-caption text-white opacity-80 mt-2">
              {{ insights.active_deals_count }} active deals
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Alert Cards -->
    <v-row v-if="!loading && insights">
      <v-col cols="12" md="4">
        <v-alert
          :model-value="insights.stale_deals_count > 0"
          type="warning"
          variant="tonal"
          prominent
          border="start"
        >
          <div class="d-flex align-center">
            <v-icon size="40" class="mr-4">mdi-alert-circle</v-icon>
            <div>
              <div class="text-h5 font-weight-bold">{{ insights.stale_deals_count }}</div>
              <div class="text-body-2">Deals Need Attention</div>
              <div class="text-caption">Not updated in 14+ days</div>
            </div>
          </div>
        </v-alert>
      </v-col>

      <v-col cols="12" md="4">
        <v-alert
          :model-value="insights.high_value_opportunities > 0"
          type="success"
          variant="tonal"
          prominent
          border="start"
        >
          <div class="d-flex align-center">
            <v-icon size="40" class="mr-4">mdi-star</v-icon>
            <div>
              <div class="text-h5 font-weight-bold">{{ insights.high_value_opportunities }}</div>
              <div class="text-body-2">High-Value Opportunities</div>
              <div class="text-caption">Premium deals in pipeline</div>
            </div>
          </div>
        </v-alert>
      </v-col>

      <v-col cols="12" md="4">
        <v-alert
          :model-value="insights.overdue_tasks > 0"
          type="error"
          variant="tonal"
          prominent
          border="start"
        >
          <div class="d-flex align-center">
            <v-icon size="40" class="mr-4">mdi-clock-alert</v-icon>
            <div>
              <div class="text-h5 font-weight-bold">{{ insights.overdue_tasks }}</div>
              <div class="text-body-2">Overdue Tasks</div>
              <div class="text-caption">Require immediate action</div>
            </div>
          </div>
        </v-alert>
      </v-col>
    </v-row>

    <!-- Top Deals by AI Score -->
    <v-row v-if="!loading && insights && insights.top_deals">
      <v-col cols="12">
        <v-card elevation="2">
          <v-card-title class="bg-purple-lighten-5">
            <v-icon color="purple" class="mr-2">mdi-trophy-award</v-icon>
            Top Deals by AI Score
          </v-card-title>
          <v-card-text class="pa-0">
            <v-list>
              <v-list-item
                v-for="(deal, index) in insights.top_deals"
                :key="deal.id"
                :to="`/deals`"
              >
                <template v-slot:prepend>
                  <v-avatar :color="getScoreColor(deal.score)" size="48">
                    <span class="text-h6 font-weight-bold">{{ deal.score }}</span>
                  </v-avatar>
                </template>

                <v-list-item-title class="font-weight-medium">
                  {{ deal.title }}
                </v-list-item-title>
                <v-list-item-subtitle>
                  ${{ formatCurrency(deal.amount) }} • {{ formatStage(deal.stage) }}
                </v-list-item-subtitle>

                <template v-slot:append>
                  <v-chip :color="getScoreColor(deal.score)" variant="flat" size="small">
                    {{ getScoreLabel(deal.score) }}
                  </v-chip>
                </template>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- AI Recommendations -->
    <v-row v-if="!loading">
      <v-col cols="12">
        <v-card elevation="2">
          <v-card-title class="bg-blue-lighten-5">
            <v-icon color="blue" class="mr-2">mdi-lightbulb-on</v-icon>
            AI Recommendations
          </v-card-title>
          <v-card-text>
            <v-list lines="two">
              <v-list-item
                v-for="(rec, i) in recommendations"
                :key="i"
                :prepend-icon="rec.icon"
              >
                <v-list-item-title class="font-weight-medium">{{ rec.title }}</v-list-item-title>
                <v-list-item-subtitle>{{ rec.description }}</v-list-item-subtitle>
                <template v-slot:append>
                  <v-chip :color="rec.color" size="small" variant="tonal">
                    {{ rec.impact }}
                  </v-chip>
                </template>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- How AI Scoring Works -->
    <v-row>
      <v-col cols="12">
        <v-expansion-panels>
          <v-expansion-panel>
            <v-expansion-panel-title>
              <v-icon class="mr-2">mdi-information</v-icon>
              How AI Deal Scoring Works
            </v-expansion-panel-title>
            <v-expansion-panel-text>
              <div class="pa-4">
                <h4 class="text-h6 mb-3">Our AI analyzes multiple factors:</h4>
                <v-row>
                  <v-col cols="12" md="6">
                    <v-list density="compact">
                      <v-list-item prepend-icon="mdi-clock-outline">
                        <v-list-item-title>Time in Stage</v-list-item-title>
                        <v-list-item-subtitle>Fresh deals score higher</v-list-item-subtitle>
                      </v-list-item>
                      <v-list-item prepend-icon="mdi-history">
                        <v-list-item-title>Company History</v-list-item-title>
                        <v-list-item-subtitle>Past win rate with this client</v-list-item-subtitle>
                      </v-list-item>
                      <v-list-item prepend-icon="mdi-checkbox-marked-circle">
                        <v-list-item-title>Task Completion</v-list-item-title>
                        <v-list-item-subtitle>Higher completion = better engagement</v-list-item-subtitle>
                      </v-list-item>
                    </v-list>
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-list density="compact">
                      <v-list-item prepend-icon="mdi-currency-usd">
                        <v-list-item-title>Deal Value</v-list-item-title>
                        <v-list-item-subtitle>Compared to average deal size</v-list-item-subtitle>
                      </v-list-item>
                      <v-list-item prepend-icon="mdi-chart-timeline-variant">
                        <v-list-item-title>Stage Progression</v-list-item-title>
                        <v-list-item-subtitle>Later stages score higher</v-list-item-subtitle>
                      </v-list-item>
                      <v-list-item prepend-icon="mdi-account-voice">
                        <v-list-item-title>Contact Engagement</v-list-item-title>
                        <v-list-item-subtitle>Interaction frequency and quality</v-list-item-subtitle>
                      </v-list-item>
                    </v-list>
                  </v-col>
                </v-row>
              </div>
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { crmService } from '@/services/api'

const insights = ref(null)
const loading = ref(false)

const recommendations = computed(() => {
  if (!insights.value) return []
  
  const recs = []
  
  if (insights.value.stale_deals_count > 0) {
    recs.push({
      title: 'Re-engage stale deals',
      description: `${insights.value.stale_deals_count} deals haven't been updated recently. Schedule follow-ups to keep momentum.`,
      icon: 'mdi-phone-in-talk',
      color: 'warning',
      impact: 'High Impact'
    })
  }
  
  if (insights.value.win_rate < 30) {
    recs.push({
      title: 'Improve qualification process',
      description: 'Win rate is below 30%. Focus on better lead qualification to improve efficiency.',
      icon: 'mdi-filter',
      color: 'error',
      impact: 'Critical'
    })
  }
  
  if (insights.value.high_value_opportunities > 0) {
    recs.push({
      title: 'Prioritize high-value deals',
      description: `You have ${insights.value.high_value_opportunities} premium opportunities. Allocate more resources here.`,
      icon: 'mdi-star',
      color: 'success',
      impact: 'High Revenue'
    })
  }
  
  if (insights.value.overdue_tasks > 0) {
    recs.push({
      title: 'Complete overdue tasks',
      description: `${insights.value.overdue_tasks} tasks are overdue. These may be blocking deal progress.`,
      icon: 'mdi-alert',
      color: 'error',
      impact: 'Urgent'
    })
  }
  
  if (insights.value.active_deals_count < 5) {
    recs.push({
      title: 'Build pipeline volume',
      description: 'Pipeline is thin. Focus on lead generation to maintain healthy deal flow.',
      icon: 'mdi-trending-up',
      color: 'info',
      impact: 'Medium Impact'
    })
  }
  
  return recs
})

onMounted(() => {
  loadInsights()
})

async function loadInsights() {
  loading.value = true
  try {
    insights.value = await crmService.getAIInsights()
  } catch (error) {
    console.error('Failed to load AI insights:', error)
  } finally {
    loading.value = false
  }
}

function formatCurrency(value) {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value)
}

function formatStage(stage) {
  const stages = {
    lead: 'Lead',
    qualified: 'Qualified',
    proposal: 'Proposal',
    negotiation: 'Negotiation',
    won: 'Won',
    lost: 'Lost'
  }
  return stages[stage] || stage
}

function getScoreColor(score) {
  if (score >= 80) return 'success'
  if (score >= 60) return 'primary'
  if (score >= 40) return 'warning'
  return 'error'
}

function getScoreLabel(score) {
  if (score >= 80) return 'Excellent'
  if (score >= 60) return 'Good'
  if (score >= 40) return 'Fair'
  return 'Needs Attention'
}
</script>

<style scoped>
.gradient-card {
  background: linear-gradient(135deg, var(--v-theme-primary) 0%, var(--v-theme-primary-darken-1) 100%);
}

.purple-gradient {
  background: linear-gradient(135deg, #7B1FA2 0%, #4A148C 100%) !important;
}

.success-gradient {
  background: linear-gradient(135deg, #43A047 0%, #2E7D32 100%) !important;
}

.primary-gradient {
  background: linear-gradient(135deg, #1976D2 0%, #0D47A1 100%) !important;
}
</style>
