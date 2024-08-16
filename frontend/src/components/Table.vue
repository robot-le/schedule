<script>

import apiClient from '@/services/axios';

export default {
  data() {
    return {
        resp: null
    }
  },
  methods: {
    async sendSchedule() {
        const response = await apiClient.post('/schedules', {
            person: 'Bryan',
            subject: 'geography',
        })
        this.resp = response.data
    }
  }
}
</script>

<template>
    <button @click="sendSchedule()">click me</button>
    <p>{{ resp }}</p>
</template>