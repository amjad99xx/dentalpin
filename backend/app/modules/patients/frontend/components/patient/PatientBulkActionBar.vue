<script setup lang="ts">
/**
 * PatientBulkActionBar — sticky bar shown on /patients while selection
 * mode is active and at least one row is checked. Presentational only;
 * the host page (pages/patients/index.vue) owns selection state and
 * wires up handlers. Actions offered here are gated by the host on
 * real capabilities (permission + whether a channel adapter is actually
 * configured for this clinic) — this bar never assumes an action works.
 */
defineProps<{
  count: number
  canDelete: boolean
  canWhatsapp: boolean
}>()

const emit = defineEmits<{
  cancel: []
  delete: []
  whatsapp: []
}>()

const { t } = useI18n()
</script>

<template>
  <nav
    class="fixed inset-x-0 bottom-0 z-40 bg-surface/95 backdrop-blur border-t border-default px-3 py-2"
    :style="{ paddingBottom: 'calc(0.5rem + env(safe-area-inset-bottom))' }"
    :aria-label="t('patients.bulk.ariaLabel')"
  >
    <div class="max-w-5xl mx-auto flex items-center gap-2">
      <UButton
        variant="ghost"
        color="neutral"
        icon="i-lucide-x"
        :aria-label="t('patients.bulk.cancel')"
        @click="emit('cancel')"
      />
      <span class="text-ui text-default font-medium shrink-0">
        {{ t('patients.bulk.selectedCount', { count }) }}
      </span>
      <div class="flex-1" />
      <UButton
        v-if="canWhatsapp"
        variant="soft"
        color="primary"
        icon="i-lucide-message-circle"
        @click="emit('whatsapp')"
      >
        {{ t('patients.bulk.whatsappAction') }}
      </UButton>
      <UButton
        v-if="canDelete"
        variant="soft"
        color="error"
        icon="i-lucide-trash-2"
        @click="emit('delete')"
      >
        {{ t('patients.bulk.deleteAction') }}
      </UButton>
    </div>
  </nav>
</template>
