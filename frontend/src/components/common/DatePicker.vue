<template>
  <div class="date-picker-wrapper">
    <VueDatePicker
      v-model="localDate"
      :dark="true"
      :enable-time-picker="false"
      :format="format"
      :max-date="maxDate"
      :min-date="minDate"
      :placeholder="placeholder"
      :auto-apply="true"
      :clearable="clearable"
      :required="required"
      :teleport="true"
      month-name-format="long"
      :year-range="yearRange"
      @update:model-value="handleUpdate"
    >
      <template #dp-input="{ value }">
        <div class="custom-date-input input flex items-center justify-between cursor-pointer">
          <span v-if="value" class="text-dark-100">{{ value }}</span>
          <span v-else class="text-dark-400">{{ placeholder }}</span>
          <svg class="w-5 h-5 text-dark-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
          </svg>
        </div>
      </template>
    </VueDatePicker>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { VueDatePicker } from '@vuepic/vue-datepicker'
import '@vuepic/vue-datepicker/dist/main.css'

const props = defineProps({
  modelValue: {
    type: [String, Date, null],
    default: null
  },
  placeholder: {
    type: String,
    default: 'Selecciona una fecha'
  },
  format: {
    type: String,
    default: 'dd/MM/yyyy'
  },
  maxDate: {
    type: [Date, String],
    default: null
  },
  minDate: {
    type: [Date, String],
    default: null
  },
  yearRange: {
    type: Array,
    default: () => [1950, new Date().getFullYear()]
  },
  clearable: {
    type: Boolean,
    default: true
  },
  required: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue'])

const localDate = ref(props.modelValue ? new Date(props.modelValue) : null)

watch(() => props.modelValue, (newVal) => {
  localDate.value = newVal ? new Date(newVal) : null
})

function handleUpdate(date) {
  if (date) {
    // Convert to YYYY-MM-DD format for backend
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    const formattedDate = `${year}-${month}-${day}`
    emit('update:modelValue', formattedDate)
  } else {
    emit('update:modelValue', null)
  }
}
</script>

<style>
/* Custom dark theme styles for VueDatePicker */
.dp__theme_dark {
  --dp-background-color: #1a1d29;
  --dp-text-color: #e5e7eb;
  --dp-hover-color: #2d3548;
  --dp-hover-text-color: #ffffff;
  --dp-hover-icon-color: #959db3;
  --dp-primary-color: #999ae2;
  --dp-primary-text-color: #ffffff;
  --dp-secondary-color: #4f46e5;
  --dp-border-color: #374151;
  --dp-menu-border-color: #374151;
  --dp-border-color-hover: #6366f1;
  --dp-disabled-color: #4b5563;
  --dp-scroll-bar-background: #1f2937;
  --dp-scroll-bar-color: #4b5563;
  --dp-success-color: #10b981;
  --dp-success-color-disabled: #047857;
  --dp-icon-color: #9ca3af;
  --dp-danger-color: #ef4444;
  --dp-highlight-color: rgba(99, 102, 241, 0.1);
}

.date-picker-wrapper {
  width: 100%;
}

.custom-date-input {
  width: 100%;
  min-height: 42px;
}

/* Override input styles to match our design system */
.dp__input {
  display: none;
}

.dp__main {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.dp__menu {
  border: 1px solid #374151 !important;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 10px 10px -5px rgba(0, 0, 0, 0.4);
  border-radius: 12px;
}

.dp__calendar_header {
  font-weight: 600;
}

.dp__calendar_item {
  border-radius: 8px;
  transition: all 0.2s ease;
}

.dp__today {
  border: 1px solid #6366f1;
}

.dp__active_date {
  background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
  font-weight: 600;
}

.dp__cell_inner:hover {
  background: #2d3548;
  transform: scale(1.05);
}

.dp__overlay_cell_active {
  background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
}

.dp__button {
  border-radius: 8px;
  transition: all 0.2s ease;
}

.dp__button:hover {
  background: #2d3548;
  transform: translateY(-1px);
}
</style>
