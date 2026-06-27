<template>
  <div class="weekday-picker">
    <div class="weekday-days">
      <button
        v-for="item in options"
        :key="item.value"
        type="button"
        class="weekday-btn"
        :class="{
          'is-active': selectedWeekday === item.value,
          'has-content': markedWeekdays.has(item.value)
        }"
        @click="$emit('select', item.value)"
      >
        <span class="weekday-label">{{ item.label }}</span>
        <span v-if="markedWeekdays.has(item.value)" class="weekday-dot" />
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { WEEKDAY_OPTIONS, type Weekday } from '~/utils/xhsWeekday'

defineProps<{
  selectedWeekday: Weekday
  markedWeekdays: Set<Weekday>
}>()

defineEmits<{
  select: [weekday: Weekday]
}>()

const options = WEEKDAY_OPTIONS
</script>

<style scoped>
.weekday-picker {
  width: 100%;
}

.weekday-days {
  display: grid;
  grid-template-columns: repeat(7, minmax(0, 1fr));
  gap: 0.5rem;
}

.weekday-btn {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 52px;
  padding: 0.65rem 0.35rem;
  border: 1px solid #e4e7ed;
  border-radius: 10px;
  background: #fff;
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s, box-shadow 0.2s;
}

.weekday-btn:hover {
  border-color: #c7cffb;
  background: #f7f8fc;
}

.weekday-btn.is-active {
  border-color: #667eea;
  background: #eef1ff;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.18);
}

.weekday-label {
  font-size: 0.95rem;
  font-weight: 600;
  color: #333;
}

.weekday-btn.is-active .weekday-label {
  color: #667eea;
}

.weekday-dot {
  position: absolute;
  top: 6px;
  right: 6px;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #ff2442;
}

@media (max-width: 768px) {
  .weekday-days {
    gap: 0.35rem;
  }

  .weekday-btn {
    min-height: 46px;
    padding: 0.5rem 0.2rem;
    border-radius: 8px;
  }

  .weekday-label {
    font-size: 0.82rem;
  }
}
</style>
