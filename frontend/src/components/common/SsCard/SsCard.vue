<template>
  <div :class="cardClasses">
    <div v-if="$slots.header || title" class="ss-card__header">
      <slot name="header">
        <h3 class="ss-card__title">{{ title }}</h3>
      </slot>
    </div>
    <div class="ss-card__body">
      <slot />
    </div>
    <div v-if="$slots.footer" class="ss-card__footer">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  title?: string
  hoverable?: boolean
  highlight?: boolean
  padding?: 'small' | 'medium' | 'large'
}

const props = withDefaults(defineProps<Props>(), {
  hoverable: true,
  highlight: false,
  padding: 'medium',
})

const cardClasses = computed(() => ({
  'ss-card': true,
  'ss-card--hoverable': props.hoverable,
  'ss-card--highlight': props.highlight,
  [`ss-card--padding-${props.padding}`]: true,
}))
</script>

<style scoped lang="scss">
.ss-card {
  background: linear-gradient(180deg, var(--bg-card), var(--bg-secondary));
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  transition: all 0.3s var(--ease-default);
  overflow: hidden;

  &--hoverable {
    &:hover {
      border-color: var(--border-gold);
      box-shadow: var(--shadow-lg);
    }
  }

  &--highlight {
    border-color: var(--border-gold);
    background: linear-gradient(180deg, var(--bg-hover), var(--bg-card));
  }

  &--padding-small {
    .ss-card__body {
      padding: var(--space-3);
    }
  }

  &--padding-medium {
    .ss-card__body {
      padding: var(--space-4);
    }
  }

  &--padding-large {
    .ss-card__body {
      padding: var(--space-6);
    }
  }

  &__header {
    padding: var(--space-4) var(--space-4) 0;
    border-bottom: 1px solid var(--border-default);
    padding-bottom: var(--space-3);
    margin-bottom: var(--space-3);
  }

  &__title {
    font-family: var(--font-title);
    font-size: var(--text-lg);
    font-weight: 600;
    color: var(--text-primary);
    margin: 0;
  }

  &__body {
    padding: var(--space-4);
  }

  &__footer {
    padding: var(--space-3) var(--space-4);
    border-top: 1px solid var(--border-default);
    background: rgba(0, 0, 0, 0.2);
  }
}
</style>
