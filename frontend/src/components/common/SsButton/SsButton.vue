<template>
  <button
    :class="buttonClasses"
    :disabled="disabled || loading"
    @click="handleClick"
  >
    <el-icon v-if="loading" class="ss-button__icon is-loading">
      <Loading />
    </el-icon>
    <span v-else class="ss-button__content">
      <el-icon v-if="icon" class="ss-button__icon">
        <component :is="icon" />
      </el-icon>
      <slot />
    </span>
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Component } from 'vue'
import { ElIcon } from 'element-plus'
import { Loading } from '@element-plus/icons-vue'

interface Props {
  type?: 'primary' | 'gold' | 'danger' | 'ghost' | 'default'
  size?: 'small' | 'medium' | 'large'
  disabled?: boolean
  loading?: boolean
  icon?: Component
  block?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  type: 'default',
  size: 'medium',
  disabled: false,
  loading: false,
  block: false,
})

const emit = defineEmits<{
  click: [event: MouseEvent]
}>()

const buttonClasses = computed(() => ({
  'ss-button': true,
  [`ss-button--${props.type}`]: true,
  [`ss-button--${props.size}`]: true,
  'ss-button--block': props.block,
  'ss-button--loading': props.loading,
}))

function handleClick(event: MouseEvent) {
  if (!props.disabled && !props.loading) {
    emit('click', event)
  }
}
</script>

<style scoped lang="scss">
.ss-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border: none;
  border-radius: var(--radius-md);
  font-family: var(--font-body);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s var(--ease-default);
  position: relative;
  overflow: hidden;

  &--medium {
    padding: 10px 24px;
    font-size: 14px;
    height: 40px;
  }

  &--small {
    padding: 6px 16px;
    font-size: 12px;
    height: 32px;
  }

  &--large {
    padding: 14px 32px;
    font-size: 16px;
    height: 48px;
  }

  &--primary {
    background: linear-gradient(135deg, var(--color-primary), var(--color-primary-light));
    color: var(--text-primary);
    border: 1px solid rgba(74, 139, 181, 0.5);

    &:hover:not(:disabled) {
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(45, 90, 123, 0.4);
    }
  }

  &--gold {
    background: linear-gradient(135deg, var(--color-secondary), var(--color-secondary-light));
    color: var(--text-primary);
    border: 1px solid rgba(212, 175, 55, 0.5);

    &:hover:not(:disabled) {
      box-shadow: var(--shadow-gold);
    }
  }

  &--danger {
    background: linear-gradient(135deg, #922B21, var(--color-danger));
    color: var(--text-primary);
    border: 1px solid rgba(231, 76, 60, 0.5);
  }

  &--ghost {
    background: transparent;
    color: var(--text-primary);
    border: 1px solid rgba(255, 255, 255, 0.2);

    &:hover:not(:disabled) {
      background: rgba(255, 255, 255, 0.05);
      border-color: rgba(255, 255, 255, 0.3);
    }
  }

  &--default {
    background: var(--bg-card);
    color: var(--text-primary);
    border: 1px solid var(--border-default);

    &:hover:not(:disabled) {
      background: var(--bg-hover);
    }
  }

  &--block {
    width: 100%;
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  &--loading {
    cursor: wait;
  }

  &__icon.is-loading {
    animation: spin 1s linear infinite;
  }
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>
