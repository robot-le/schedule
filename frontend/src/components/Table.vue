<template>
  <!-- <div class="schedule-table">
    <table class="table table-bordered">
      <thead>
        <tr>
          <th>Person</th>
          <th v-for="day in weekDays" :key="day">{{ day }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="person in people" :key="person">
          <td>{{ person }}</td>
          <td
            v-for="(day, index) in weekDays"
            :key="day"
            :class="{ 'bg-light': isWeekend(index) }"
            @mousedown="startDrag(person, index)"
            @mousemove="drag(person, index)"
            @mouseup="endDrag"
          >
            <div
              v-if="hasSchedule(person, index)"
              class="schedule-block"
              :style="getBlockStyle(person, index)"
            >
              {{ getScheduleSubject(person, index) }}
            </div>
          </td>
        </tr>
      </tbody>
    </table>
    <ScheduleModal
      v-if="showModal"
      :person="modalData.person"
      :startDate="modalData.startDate"
      :endDate="modalData.endDate"
      @save="saveSchedule"
      @close="closeModal"
    />
  </div> -->

  <div class="schedule-table">
    <div class="schedule-grid">
      <div class="schedule-header">
        <div class="header-cell person-header">Person</div>
        <div
          v-for="day in weekDays"
          :key="day"
          class="header-cell day-header"
        >
          {{ day }}
        </div>
      </div>
      <div
        v-for="person in people"
        :key="person"
        class="schedule-row"
      >
        <div class="person-cell">{{ person }}</div>
        <div
          v-for="(day, index) in weekDays"
          :key="day"
          class="day-cell"
          :class="{ 'weekend': isWeekend(index) }"
          @mousedown="startDrag(person, index)"
          @mousemove="drag(person, index)"
          @mouseup="endDrag"
        >
        </div>

          <div
            v-if="hasSchedule(person, index)"
            class="schedule-block"
            :style="getBlockStyle(person, index)"
          >
            {{ getScheduleSubject(person, index) }}
          </div>

      </div>
    </div>
    <ScheduleModal
      v-if="showModal"
      :person="modalData.person"
      :startDate="modalData.startDate"
      :endDate="modalData.endDate"
      @save="saveSchedule"
      @close="closeModal"
    />
  </div>

</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import ScheduleModal from './ScheduleModal.vue';
import apiClient from '@/services/axios';

const weekDays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
const people = ref([]);
const schedules = ref([]);
const isDragging = ref(false);
const dragStart = ref({ person: null, day: null });
const showModal = ref(false);
const modalData = ref({ person: '', startDate: null, endDate: null });

const isWeekend = (index) => index >= 5;

const hasSchedule = (person, day) => {
  return schedules.value.some(
    (s) => s.person === person && s.start_day <= day && s.end_day >= day
  );
};

const getScheduleSubject = (person, day) => {
  const schedule = schedules.value.find(
    (s) => s.person === person && s.start_day <= day && s.end_day >= day
  );
  return schedule ? schedule.subject : '';
};

const getBlockStyle = (person, day) => {
  const schedule = schedules.value.find(
    (s) => s.person === person && s.start_day <= day && s.end_day >= day
  );
  // console.log(person)
  if (!schedule) return {};
  // const width = `${(schedule.end_day - schedule.start_day + 1) * 100}%`;
  return {
    width: `${(schedule.end_day - schedule.start_day + 1) * 100}%`,
    left: `${(schedule.start_day - day) * 100}%`,
    // left: '27%',
    // width: '73%',
    backgroundColor: getRandomColor(schedule.subject),
  };
};

const getRandomColor = (subject) => {
  // Generate a consistent color based on the subject
  let hash = 0;
  for (let i = 0; i < subject.length; i++) {
    hash = subject.charCodeAt(i) + ((hash << 5) - hash);
  }
  const hue = hash % 360;
  return `hsl(${hue}, 70%, 80%)`;
};

const startDrag = (person, day) => {
  // console.log('starting drag')
  if (isWeekend(day)) return;
  isDragging.value = true;
  dragStart.value = { person, day };
};

const drag = (person, day) => {
  // console.log('drag')
  if (!isDragging.value || isWeekend(day)) return;
};

const endDrag = () => {
  // console.log('ending drag')
  if (!isDragging.value) return;
  isDragging.value = false;
  const endDay = Math.min(dragStart.value.day, 4); // Ensure it doesn't go into the weekend
  showModal.value = true;
  modalData.value = {
    person: dragStart.value.person,
    startDate: weekDays[dragStart.value.day],
    endDate: weekDays[endDay],
  };
};

const saveSchedule = async (scheduleData) => {
  try {
    await apiClient.post('/api/schedules', scheduleData);
    await fetchSchedules();
    closeModal();
  } catch (error) {
    console.error('Error saving schedule:', error);
  }
};

const closeModal = () => {
  showModal.value = false;
  modalData.value = { person: '', startDate: null, endDate: null };
};

const fetchSchedules = async () => {
  try {
    const response = await apiClient.get('/api/schedules');
    schedules.value = response.data['schedules'];
  } catch (error) {
    console.error('Error fetching schedules:', error);
  }
};

const fetchPeople = async () => {
  try {
    const response = await apiClient.get('/api/people');
    people.value = response.data;
  } catch (error) {
    console.error('Error fetching people:', error);
  }
};

onMounted(async () => {
  await fetchPeople();
  await fetchSchedules();
});
</script>

<style scoped>

.schedule-table {
  /* position: relative; */
  position: absolute;
  width: 100%;
  overflow-x: auto;
}

.schedule-grid {
  display: flex;
  flex-direction: column;
  border: 1px solid #dee2e6;
}

.schedule-header, .schedule-row {
  display: flex;
  width: 100%;
}

.header-cell, .person-cell, .day-cell {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #dee2e6;
  text-align: center;
  min-width: 100px;
}

.person-header, .person-cell {
  flex: 0 0 150px;
  font-weight: bold;
}

.day-cell {
  position: relative;
  height: 50px;
}

.weekend {
  background-color: #f8f9fa;
}

.schedule-block {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #007bff;
  border-radius: 4px;
  overflow: hidden;
  cursor: move;
  z-index: 1;
}

/* .schedule-table {
  position: relative;
}

.schedule-block {
  position: absolute;
  top: 0;
  height: 100%;
  height: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #007bff;
  border-radius: 7px;
  overflow: hidden;
  cursor: move;
} */
</style>