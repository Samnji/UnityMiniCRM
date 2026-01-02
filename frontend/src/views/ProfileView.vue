<template>
  <v-container fluid class="pa-6">
    <!-- Header -->
    <v-row>
        <v-col cols="12">
            <div class="d-flex justify-space-between align-center mb-6 flex-wrap gap-3">
                <div>
                    <h1 class="text-h3 font-weight-bold text-navy mb-2">My Profile</h1>
                    <p class="text-h6 text-grey-darken-1">Manage your account and view your performance</p>
                </div>
                <v-btn
                    color="primary"
                    prepend-icon="mdi-pencil"
                    @click="editMode = !editMode"
                >
                    {{ editMode ? 'Cancel' : 'Edit Profile' }}
                </v-btn>
            </div>
        </v-col>
    </v-row>

    <!-- Loading State -->
    <v-progress-linear v-if="loading" indeterminate color="primary"></v-progress-linear>

    <v-row v-if="!loading && profile">
      <!-- Left Column: Profile Card & Details -->
      <v-col cols="12" md="4">
        <!-- Profile Card -->
        <v-card elevation="4" class="mb-4 profile-card">
          <v-card-text class="pa-6 text-center">
            <div class="position-relative d-inline-block mb-4">
              <v-avatar color="primary" size="120" class="avatar-gradient elevation-8">
                <span class="text-h2 font-weight-bold text-white">{{ getInitials() }}</span>
              </v-avatar>
              <v-btn
                v-if="editMode"
                icon
                size="small"
                color="white"
                class="edit-avatar-btn"
              >
                <v-icon>mdi-camera</v-icon>
              </v-btn>
            </div>

            <h2 class="text-h5 font-weight-bold mb-2">{{ profile.full_name || profile.username }}</h2>
            <p class="text-body-2 text-medium-emphasis mb-3">{{ profile.email }}</p>

            <div class="d-flex justify-center gap-2 mb-4">
              <v-chip :color="getRoleColor(profile.role)" variant="flat">
                <v-icon start>{{ getRoleIcon(profile.role) }}</v-icon>
                {{ profile.role_display }}
              </v-chip>
              <v-chip v-if="profile.team_name" color="blue-grey" variant="tonal">
                <v-icon start>mdi-account-group</v-icon>
                {{ profile.team_name }}
              </v-chip>
            </div>

            <v-divider class="my-4"></v-divider>

            <div class="text-left">
              <div class="d-flex align-center mb-3">
                <v-icon class="mr-3" color="primary">mdi-phone</v-icon>
                <div class="flex-grow-1">
                  <div class="text-caption text-medium-emphasis">Phone</div>
                  <div class="text-body-2 font-weight-medium">{{ profile.phone || 'Not set' }}</div>
                </div>
              </div>

              <div class="d-flex align-center mb-3">
                <v-icon class="mr-3" color="primary">mdi-calendar</v-icon>
                <div class="flex-grow-1">
                  <div class="text-caption text-medium-emphasis">Member Since</div>
                  <div class="text-body-2 font-weight-medium">{{ formatDate(profile.created_at) }}</div>
                </div>
              </div>
            </div>
          </v-card-text>
        </v-card>

        <!-- Edit Form -->
        <v-card v-if="editMode" elevation="2">
          <v-card-title class="bg-primary">
            <span class="text-h6">Update Profile</span>
          </v-card-title>
          <v-card-text class="pa-4">
            <v-text-field
              v-model="editForm.phone"
              label="Phone Number"
              prepend-inner-icon="mdi-phone"
              variant="outlined"
              density="comfortable"
              class="mb-3"
            ></v-text-field>

            <v-text-field
              v-model="editForm.avatar"
              label="Avatar URL"
              prepend-inner-icon="mdi-image"
              variant="outlined"
              density="comfortable"
            ></v-text-field>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn @click="editMode = false">Cancel</v-btn>
            <v-btn color="primary" @click="saveProfile">Save Changes</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <!-- Right Column: Analytics & Stats -->
      <v-col cols="12" md="8">
        <!-- Performance Overview -->
        <v-card elevation="2" class="mb-4">
          <v-card-title class="bg-gradient-primary pa-4">
            <v-icon class="mr-2">mdi-chart-line</v-icon>
            Performance Overview
          </v-card-title>
          <v-card-text class="pa-0">
            <v-row class="ma-0">
              <v-col cols="12" sm="6" md="3" class="pa-4 border-e border-b">
                <div class="text-center">
                  <v-icon size="32" color="blue" class="mb-2">mdi-handshake</v-icon>
                  <div class="text-h4 font-weight-bold">{{ analytics?.total_deals || 0 }}</div>
                  <div class="text-caption text-medium-emphasis">Total Deals</div>
                </div>
              </v-col>
              <v-col cols="12" sm="6" md="3" class="pa-4 border-e border-b">
                <div class="text-center">
                  <v-icon size="32" color="success" class="mb-2">mdi-trophy</v-icon>
                  <div class="text-h4 font-weight-bold">{{ analytics?.won_deals || 0 }}</div>
                  <div class="text-caption text-medium-emphasis">Won Deals</div>
                </div>
              </v-col>
              <v-col cols="12" sm="6" md="3" class="pa-4 border-e border-b">
                <div class="text-center">
                  <v-icon size="32" color="warning" class="mb-2">mdi-progress-clock</v-icon>
                  <div class="text-h4 font-weight-bold">{{ analytics?.active_deals || 0 }}</div>
                  <div class="text-caption text-medium-emphasis">Active Deals</div>
                </div>
              </v-col>
              <v-col cols="12" sm="6" md="3" class="pa-4 border-b">
                <div class="text-center">
                  <v-icon size="32" color="purple" class="mb-2">mdi-percent</v-icon>
                  <div class="text-h4 font-weight-bold">{{ analytics?.win_rate || 0 }}%</div>
                  <div class="text-caption text-medium-emphasis">Win Rate</div>
                </div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <!-- Financial Overview -->
        <v-card elevation="2" class="mb-4">
          <v-card-title class="bg-gradient-success pa-4">
            <v-icon class="mr-2">mdi-cash-multiple</v-icon>
            Financial Performance
          </v-card-title>
          <v-card-text class="pa-6">
            <v-row>
              <v-col cols="12" md="6">
                <v-card variant="tonal" color="success" class="pa-4">
                  <div class="d-flex align-center justify-space-between">
                    <div>
                      <div class="text-caption text-medium-emphasis mb-1">Total Revenue (Won)</div>
                      <div class="text-h4 font-weight-bold">${{ formatCurrency(analytics?.total_won_value || 0) }}</div>
                    </div>
                    <v-icon size="48" color="success">mdi-cash-check</v-icon>
                  </div>
                </v-card>
              </v-col>
              <v-col cols="12" md="6">
                <v-card variant="tonal" color="primary" class="pa-4">
                  <div class="d-flex align-center justify-space-between">
                    <div>
                      <div class="text-caption text-medium-emphasis mb-1">Pipeline Value</div>
                      <div class="text-h4 font-weight-bold">${{ formatCurrency(analytics?.pipeline_value || 0) }}</div>
                    </div>
                    <v-icon size="48" color="primary">mdi-chart-timeline-variant</v-icon>
                  </div>
                </v-card>
              </v-col>
            </v-row>

            <v-row class="mt-4">
              <v-col cols="12" md="6">
                <div class="text-caption text-medium-emphasis mb-2">Average Deal Size</div>
                <div class="text-h5 font-weight-bold">${{ formatCurrency(analytics?.avg_deal_size || 0) }}</div>
                <v-progress-linear
                  :model-value="getAvgDealProgress()"
                  color="primary"
                  height="8"
                  rounded
                  class="mt-2"
                ></v-progress-linear>
              </v-col>
              <v-col cols="12" md="6">
                <div class="text-caption text-medium-emphasis mb-2">Largest Deal</div>
                <div class="text-h5 font-weight-bold">${{ formatCurrency(analytics?.largest_deal || 0) }}</div>
                <v-progress-linear
                  :model-value="100"
                  color="success"
                  height="8"
                  rounded
                  class="mt-2"
                ></v-progress-linear>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <!-- Activity & Tasks -->
        <v-row>
          <v-col cols="12" md="6">
            <v-card elevation="2">
              <v-card-title class="bg-warning pa-4">
                <v-icon class="mr-2">mdi-checkbox-marked-circle</v-icon>
                Task Activity
              </v-card-title>
              <v-card-text class="pa-4">
                <div class="mb-4">
                  <div class="d-flex justify-space-between align-center mb-2">
                    <span class="text-body-2">Completed Tasks</span>
                    <span class="text-h6 font-weight-bold text-success">{{ analytics?.completed_tasks || 0 }}</span>
                  </div>
                  <v-progress-linear
                    :model-value="getTaskCompletionRate()"
                    color="success"
                    height="8"
                    rounded
                  ></v-progress-linear>
                </div>

                <div class="mb-4">
                  <div class="d-flex justify-space-between align-center mb-2">
                    <span class="text-body-2">Pending Tasks</span>
                    <span class="text-h6 font-weight-bold text-warning">{{ analytics?.pending_tasks || 0 }}</span>
                  </div>
                  <v-progress-linear
                    :model-value="getPendingTaskRate()"
                    color="warning"
                    height="8"
                    rounded
                  ></v-progress-linear>
                </div>

                <div>
                  <div class="d-flex justify-space-between align-center mb-2">
                    <span class="text-body-2">Overdue Tasks</span>
                    <span class="text-h6 font-weight-bold text-error">{{ analytics?.overdue_tasks || 0 }}</span>
                  </div>
                  <v-progress-linear
                    :model-value="getOverdueTaskRate()"
                    color="error"
                    height="8"
                    rounded
                  ></v-progress-linear>
                </div>

                <v-divider class="my-4"></v-divider>

                <div class="text-center">
                  <div class="text-h3 font-weight-bold mb-1">{{ getTaskCompletionRate() }}%</div>
                  <div class="text-caption text-medium-emphasis">Completion Rate</div>
                </div>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" md="6">
            <v-card elevation="2">
              <v-card-title class="bg-purple pa-4">
                <v-icon class="mr-2">mdi-chart-box-outline</v-icon>
                Deal Pipeline
              </v-card-title>
              <v-card-text class="pa-4">
                <div 
                  v-for="stage in dealStages" 
                  :key="stage.key"
                  class="mb-3"
                >
                  <div class="d-flex justify-space-between align-center mb-2">
                    <div class="d-flex align-center">
                      <v-chip 
                        :color="stage.color" 
                        size="x-small" 
                        class="mr-2"
                      ></v-chip>
                      <span class="text-body-2">{{ stage.label }}</span>
                    </div>
                    <span class="text-body-1 font-weight-bold">
                      {{ analytics?.deals_by_stage?.[stage.key] || 0 }}
                    </span>
                  </div>
                  <v-progress-linear
                    :model-value="getStagePercentage(stage.key)"
                    :color="stage.color"
                    height="6"
                    rounded
                  ></v-progress-linear>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Recent Activity -->
        <v-card elevation="2" class="mt-4">
          <v-card-title class="bg-blue-grey pa-4">
            <v-icon class="mr-2">mdi-clock-outline</v-icon>
            Recent Achievements
          </v-card-title>
          <v-card-text class="pa-4">
            <v-timeline side="end" density="compact">
              <v-timeline-item
                v-for="(achievement, index) in achievements"
                :key="index"
                :dot-color="achievement.color"
                size="small"
              >
                <template v-slot:icon>
                  <v-icon size="small">{{ achievement.icon }}</v-icon>
                </template>
                <div class="mb-4">
                  <div class="font-weight-bold">{{ achievement.title }}</div>
                  <div class="text-caption text-medium-emphasis">{{ achievement.description }}</div>
                </div>
              </v-timeline-item>
            </v-timeline>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { crmService } from '@/services/api'

const profile = ref(null)
const analytics = ref(null)
const loading = ref(true)
const editMode = ref(false)

const editForm = ref({
  phone: '',
  avatar: ''
})

const dealStages = [
  { key: 'lead', label: 'Lead', color: 'blue-grey' },
  { key: 'qualified', label: 'Qualified', color: 'blue' },
  { key: 'proposal', label: 'Proposal', color: 'purple' },
  { key: 'negotiation', label: 'Negotiation', color: 'orange' },
  { key: 'won', label: 'Won', color: 'success' },
  { key: 'lost', label: 'Lost', color: 'error' }
]

const achievements = computed(() => {
  const result = []
  
  if (analytics.value?.won_deals > 0) {
    result.push({
      title: `${analytics.value.won_deals} Deals Won`,
      description: 'Successfully closed deals',
      icon: 'mdi-trophy',
      color: 'success'
    })
  }
  
  if (analytics.value?.completed_tasks > 10) {
    result.push({
      title: 'Task Master',
      description: `Completed ${analytics.value.completed_tasks} tasks`,
      icon: 'mdi-checkbox-marked-circle',
      color: 'primary'
    })
  }
  
  if (analytics.value?.win_rate >= 50) {
    result.push({
      title: 'High Performer',
      description: `${analytics.value.win_rate}% win rate`,
      icon: 'mdi-star',
      color: 'warning'
    })
  }
  
  if (analytics.value?.pipeline_value > 100000) {
    result.push({
      title: 'Pipeline Builder',
      description: `$${formatCurrency(analytics.value.pipeline_value)} in pipeline`,
      icon: 'mdi-chart-line',
      color: 'purple'
    })
  }
  
  return result
})

onMounted(async () => {
  loading.value = true
  try {
    const [profileData, dealsData, tasksData] = await Promise.all([
      crmService.getMyProfile(),
      crmService.getDeals(),
      crmService.getTasks()
    ])
    
    profile.value = profileData
    editForm.value = {
      phone: profileData.phone || '',
      avatar: profileData.avatar || ''
    }
    
    // Calculate analytics
    const myDeals = dealsData
    const myTasks = tasksData.filter(t => t.assigned_to === profileData.user)
    
    const wonDeals = myDeals.filter(d => d.stage === 'won')
    const activeDeals = myDeals.filter(d => !['won', 'lost'].includes(d.stage))
    const totalClosed = myDeals.filter(d => ['won', 'lost'].includes(d.stage))
    
    const dealsByStage = {}
    myDeals.forEach(deal => {
      dealsByStage[deal.stage] = (dealsByStage[deal.stage] || 0) + 1
    })
    
    analytics.value = {
      total_deals: myDeals.length,
      won_deals: wonDeals.length,
      active_deals: activeDeals.length,
      win_rate: totalClosed.length > 0 ? Math.round((wonDeals.length / totalClosed.length) * 100) : 0,
      total_won_value: wonDeals.reduce((sum, d) => sum + parseFloat(d.amount), 0),
      pipeline_value: activeDeals.reduce((sum, d) => sum + parseFloat(d.amount), 0),
      avg_deal_size: myDeals.length > 0 ? myDeals.reduce((sum, d) => sum + parseFloat(d.amount), 0) / myDeals.length : 0,
      largest_deal: myDeals.length > 0 ? Math.max(...myDeals.map(d => parseFloat(d.amount))) : 0,
      completed_tasks: myTasks.filter(t => t.status === 'completed').length,
      pending_tasks: myTasks.filter(t => t.status === 'pending').length,
      overdue_tasks: myTasks.filter(t => t.status === 'pending' && new Date(t.due_date) < new Date()).length,
      total_tasks: myTasks.length,
      deals_by_stage: dealsByStage
    }
    
  } catch (error) {
    console.error('Failed to load profile data:', error)
  } finally {
    loading.value = false
  }
})

async function saveProfile() {
  try {
    await crmService.updateMyProfile(editForm.value)
    profile.value = await crmService.getMyProfile()
    editMode.value = false
  } catch (error) {
    console.error('Failed to update profile:', error)
  }
}

function getInitials() {
  if (profile.value?.full_name) {
    const names = profile.value.full_name.split(' ')
    if (names.length >= 2) {
      return (names[0].charAt(0) + names[names.length - 1].charAt(0)).toUpperCase()
    }
    return names[0].charAt(0).toUpperCase()
  }
  return profile.value?.username?.charAt(0).toUpperCase() || 'U'
}

function getRoleColor(role) {
  const colors = {
    admin: 'error',
    manager: 'warning',
    sales_rep: 'primary',
    viewer: 'info'
  }
  return colors[role] || 'default'
}

function getRoleIcon(role) {
  const icons = {
    admin: 'mdi-shield-crown',
    manager: 'mdi-account-tie',
    sales_rep: 'mdi-account',
    viewer: 'mdi-eye'
  }
  return icons[role] || 'mdi-account'
}

function formatDate(date) {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

function formatCurrency(value) {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value)
}

function getTaskCompletionRate() {
  if (!analytics.value || analytics.value.total_tasks === 0) return 0
  return Math.round((analytics.value.completed_tasks / analytics.value.total_tasks) * 100)
}

function getPendingTaskRate() {
  if (!analytics.value || analytics.value.total_tasks === 0) return 0
  return Math.round((analytics.value.pending_tasks / analytics.value.total_tasks) * 100)
}

function getOverdueTaskRate() {
  if (!analytics.value || analytics.value.total_tasks === 0) return 0
  return Math.round((analytics.value.overdue_tasks / analytics.value.total_tasks) * 100)
}

function getAvgDealProgress() {
  if (!analytics.value || analytics.value.largest_deal === 0) return 0
  return Math.round((analytics.value.avg_deal_size / analytics.value.largest_deal) * 100)
}

function getStagePercentage(stage) {
  if (!analytics.value || analytics.value.total_deals === 0) return 0
  const count = analytics.value.deals_by_stage[stage] || 0
  return Math.round((count / analytics.value.total_deals) * 100)
}
</script>

<style scoped>
.profile-card {
  background: linear-gradient(135deg, #ffffff 0%, #f5f7fa 100%);
}

.avatar-gradient {
  background: linear-gradient(135deg, #1976D2 0%, #0D47A1 100%);
}

.edit-avatar-btn {
  position: absolute;
  bottom: 0;
  right: 0;
}

.bg-gradient-primary {
  background: linear-gradient(90deg, #1976D2 0%, #1565C0 100%);
  color: white;
}

.bg-gradient-success {
  background: linear-gradient(90deg, #43A047 0%, #2E7D32 100%);
  color: white;
}

.border-e {
  border-right: 1px solid rgba(0, 0, 0, 0.12);
}

.border-b {
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
}

@media (max-width: 959px) {
  .border-e {
    border-right: none;
  }
}
</style>
