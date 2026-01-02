<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authService } from '../services/api'

const router = useRouter()
const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  if (!username.value || !password.value) {
    error.value = 'Please enter both username and password'
    return
  }

  loading.value = true
  error.value = ''

  try {
    const data = await authService.login(username.value, password.value)
    localStorage.setItem('token', data.token)
    localStorage.setItem('user', JSON.stringify(data.user))
    router.push('/')
  } catch (err) {
    error.value = err.response?.data?.error || 'Login failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <v-container fluid class="fill-height navy-gradient">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="5" lg="4">
        <v-card elevation="12" rounded="lg">
          <v-card-text class="pa-8">
            <div class="text-center mb-6">
              <v-icon size="64" color="primary" class="mb-3">mdi-office-building</v-icon>
              <h1 class="text-h4 font-weight-bold text-navy mb-2">Mini CRM</h1>
              <p class="text-subtitle-1 text-grey">Sign in to continue</p>
            </div>

            <v-form @submit.prevent="handleLogin">
              <v-text-field
                v-model="username"
                label="Username"
                prepend-inner-icon="mdi-account"
                variant="outlined"
                color="primary"
                class="mb-3"
                :disabled="loading"
              ></v-text-field>

              <v-text-field
                v-model="password"
                label="Password"
                prepend-inner-icon="mdi-lock"
                type="password"
                variant="outlined"
                color="primary"
                class="mb-4"
                :disabled="loading"
              ></v-text-field>

              <v-alert
                v-if="error"
                type="error"
                variant="tonal"
                class="mb-4"
                closable
                @click:close="error = ''"
              >
                {{ error }}
              </v-alert>

              <v-btn
                type="submit"
                color="primary"
                size="large"
                block
                :loading="loading"
                class="mb-4"
              >
                Sign In
              </v-btn>

              <v-divider class="my-4"></v-divider>

              <v-alert type="info" variant="tonal" density="compact">
                <div class="text-caption">
                  <strong>Demo Credentials:</strong><br>
                  Admin: admin / admin123<br>
                  Manager: john.smith / password123<br>
                  Sales Rep: sarah.johnson / password123<br>
                  Viewer: viewer.user / password123
                </div>
              </v-alert>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
