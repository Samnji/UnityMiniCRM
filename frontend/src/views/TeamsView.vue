<template>
  <v-container fluid class="pa-6">
    <v-row>
        <v-col cols="12">
            <div class="d-flex justify-space-between align-center mb-6 flex-wrap gap-3">
                <div>
                    <h1 class="text-h3 font-weight-bold text-navy mb-2">Teams</h1>
                    <p class="text-h6 text-grey-darken-1">Organize your sales force</p>
                </div>
                <v-btn
                    color="primary"
                    prepend-icon="mdi-plus"
                    size="large"
                    elevation="2"
                    @click="showCreateDialog = true"
                >
                    New Team
                </v-btn>
            </div>
        </v-col>
    </v-row>

    <!-- Loading State -->
    <v-row v-if="loading">
      <v-col v-for="i in 4" :key="i" cols="12" md="6" lg="4">
        <v-skeleton-loader type="card"></v-skeleton-loader>
      </v-col>
    </v-row>

    <!-- Teams Grid -->
    <v-row v-else>
      <v-col
        v-for="team in teams"
        :key="team.id"
        cols="12"
        md="6"
        lg="4"
      >
        <v-card
          elevation="2"
          hover
          class="team-card"
          @click="viewTeamDetails(team)"
        >
          <v-card-title class="d-flex align-center">
            <v-icon color="primary" class="mr-3" size="32">mdi-account-group</v-icon>
            <div class="flex-grow-1">
              <div class="text-h6">{{ team.name }}</div>
              <div class="text-caption text-medium-emphasis">{{ team.member_count }} members</div>
            </div>
            <v-menu>
              <template v-slot:activator="{ props }">
                <v-btn
                  icon="mdi-dots-vertical"
                  variant="text"
                  v-bind="props"
                  @click.stop
                ></v-btn>
              </template>
              <v-list>
                <v-list-item @click="editTeam(team)">
                  <template v-slot:prepend>
                    <v-icon>mdi-pencil</v-icon>
                  </template>
                  <v-list-item-title>Edit</v-list-item-title>
                </v-list-item>
                <v-list-item @click="confirmDelete(team)">
                  <template v-slot:prepend>
                    <v-icon color="error">mdi-delete</v-icon>
                  </template>
                  <v-list-item-title class="text-error">Delete</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </v-card-title>

          <v-divider></v-divider>

          <v-card-text>
            <p class="text-body-2 mb-4">{{ team.description || 'No description' }}</p>
            
            <div class="d-flex justify-space-between text-caption text-medium-emphasis">
              <span>Created {{ formatDate(team.created_at) }}</span>
            </div>
          </v-card-text>

          <v-card-actions>
            <v-btn
              variant="tonal"
              prepend-icon="mdi-account-multiple"
              @click.stop="viewMembers(team)"
            >
              View Members
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn
              variant="tonal"
              color="purple"
              prepend-icon="mdi-chart-line"
              @click.stop="viewInsights(team)"
            >
              AI Insights
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Create/Edit Team Dialog -->
    <v-dialog v-model="showCreateDialog" max-width="600">
      <v-card>
        <v-card-title class="bg-primary">
          <span class="text-h5">{{ editingTeam ? 'Edit Team' : 'New Team' }}</span>
        </v-card-title>

        <v-card-text class="pt-6">
          <v-text-field
            v-model="teamForm.name"
            label="Team Name"
            prepend-inner-icon="mdi-account-group"
            variant="outlined"
            :rules="[v => !!v || 'Name is required']"
          ></v-text-field>

          <v-textarea
            v-model="teamForm.description"
            label="Description"
            prepend-inner-icon="mdi-text"
            variant="outlined"
            rows="3"
          ></v-textarea>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="showCreateDialog = false">Cancel</v-btn>
          <v-btn color="primary" @click="saveTeam">
            {{ editingTeam ? 'Update' : 'Create' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Team Members Dialog -->
    <v-dialog v-model="showMembersDialog" max-width="800">
      <v-card v-if="selectedTeam">
        <v-card-title class="bg-primary">
          <span class="text-h5">{{ selectedTeam.name }} - Members</span>
        </v-card-title>

        <v-card-text class="pa-0">
          <v-list>
            <v-list-item
              v-for="member in teamMembers"
              :key="member.id"
              :subtitle="member.email"
            >
              <template v-slot:prepend>
                <v-avatar color="primary" size="40">
                  <v-icon>mdi-account</v-icon>
                </v-avatar>
              </template>
              
              <v-list-item-title>{{ member.full_name }}</v-list-item-title>
              <v-list-item-subtitle>{{ member.role_display }} • {{ member.phone }}</v-list-item-subtitle>

              <template v-slot:append>
                <v-chip :color="getRoleColor(member.role)" size="small">
                  {{ member.role_display }}
                </v-chip>
              </template>
            </v-list-item>
          </v-list>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="showMembersDialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Team Insights Dialog -->
    <v-dialog v-model="showInsightsDialog" max-width="900">
      <v-card v-if="selectedTeam && teamInsights">
        <v-card-title class="bg-purple">
          <span class="text-h5">{{ selectedTeam.name }} - AI Insights</span>
        </v-card-title>

        <v-card-text class="pt-6">
          <v-row>
            <v-col cols="12" md="3">
              <v-card variant="tonal" color="primary">
                <v-card-text class="text-center">
                  <div class="text-h4 font-weight-bold">{{ teamInsights.active_deals }}</div>
                  <div class="text-caption">Active Deals</div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" md="3">
              <v-card variant="tonal" color="success">
                <v-card-text class="text-center">
                  <div class="text-h4 font-weight-bold">{{ teamInsights.team_win_rate }}%</div>
                  <div class="text-caption">Win Rate</div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" md="6">
              <v-card variant="tonal" color="purple">
                <v-card-text class="text-center">
                  <div class="text-h4 font-weight-bold">${{ formatCurrency(teamInsights.total_pipeline_value) }}</div>
                  <div class="text-caption">Pipeline Value</div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <v-divider class="my-6"></v-divider>

          <h3 class="text-h6 mb-4">Team Performance</h3>
          <v-table>
            <thead>
              <tr>
                <th>Member</th>
                <th>Active Deals</th>
                <th>Win Rate</th>
                <th>Pipeline Value</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="member in teamInsights.members" :key="member.user_id">
                <td>{{ member.username }}</td>
                <td>{{ member.active_deals }}</td>
                <td>{{ member.win_rate }}%</td>
                <td>${{ formatCurrency(member.total_value) }}</td>
              </tr>
            </tbody>
          </v-table>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="showInsightsDialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="showDeleteDialog" max-width="500">
      <v-card>
        <v-card-title class="text-h5">Confirm Delete</v-card-title>
        <v-card-text>
          Are you sure you want to delete <strong>{{ teamToDelete?.name }}</strong>?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="showDeleteDialog = false">Cancel</v-btn>
          <v-btn color="error" @click="deleteTeam">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { crmService } from '@/services/api'

const teams = ref([])
const loading = ref(false)
const showCreateDialog = ref(false)
const showMembersDialog = ref(false)
const showInsightsDialog = ref(false)
const showDeleteDialog = ref(false)
const editingTeam = ref(null)
const selectedTeam = ref(null)
const teamMembers = ref([])
const teamInsights = ref(null)
const teamToDelete = ref(null)

const teamForm = ref({
  name: '',
  description: ''
})

onMounted(() => {
  loadTeams()
})

async function loadTeams() {
  loading.value = true
  try {
    teams.value = await crmService.getTeams()
  } catch (error) {
    console.error('Failed to load teams:', error)
  } finally {
    loading.value = false
  }
}

async function saveTeam() {
  try {
    if (editingTeam.value) {
      await crmService.updateTeam(editingTeam.value.id, teamForm.value)
    } else {
      await crmService.createTeam(teamForm.value)
    }
    await loadTeams()
    showCreateDialog.value = false
    resetForm()
  } catch (error) {
    console.error('Failed to save team:', error)
  }
}

function editTeam(team) {
  editingTeam.value = team
  teamForm.value = { ...team }
  showCreateDialog.value = true
}

function confirmDelete(team) {
  teamToDelete.value = team
  showDeleteDialog.value = true
}

async function deleteTeam() {
  try {
    await crmService.deleteTeam(teamToDelete.value.id)
    await loadTeams()
    showDeleteDialog.value = false
    teamToDelete.value = null
  } catch (error) {
    console.error('Failed to delete team:', error)
  }
}

async function viewMembers(team) {
  selectedTeam.value = team
  try {
    teamMembers.value = await crmService.getTeamMembers(team.id)
    showMembersDialog.value = true
  } catch (error) {
    console.error('Failed to load team members:', error)
  }
}

async function viewInsights(team) {
  selectedTeam.value = team
  try {
    teamInsights.value = await crmService.getTeamInsights(team.id)
    showInsightsDialog.value = true
  } catch (error) {
    console.error('Failed to load team insights:', error)
  }
}

function viewTeamDetails(team) {
  viewMembers(team)
}

function resetForm() {
  teamForm.value = { name: '', description: '' }
  editingTeam.value = null
}

function formatDate(date) {
  return new Date(date).toLocaleDateString()
}

function formatCurrency(value) {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value)
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
</script>

<style scoped>
.team-card {
  transition: all 0.3s ease;
  cursor: pointer;
}

.team-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15) !important;
}
</style>
