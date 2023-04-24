<template>
    <div id="live2d_canvas">
    </div>
</template>

<script lang="ts">
import { at_start } from '../static/bundle'

export default {
    asyncData() {
        at_start()
    }
}
</script>

<style>
canvas {
  position: absolute;
  top: 0;
  left: -180px;
  z-index: -1;
}
</style>