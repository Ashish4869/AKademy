<template>
  <span class="badge" :class="['badge--' + mode, { nml: noMarginLeft }]">
    <slot></slot>
  </span>
</template>

<script>
export default {
  props: ['mode', 'noMarginLeft'],
};
</script>

<style scoped>
.badge {
  display: inline-block;
  padding: 0.15rem 1.25rem;
  background-color: #ccc;
  color: #000000;
  margin: 0 0.75rem;
  border-radius: 50px;
}

.nml {
  margin-left: 0;
}

.badge--highlight {
  background-color: #171717;
  color: #f8f8ff;
}

.badge--elegant {
  background-color: #45006d;
  color: white;
}
</style>
