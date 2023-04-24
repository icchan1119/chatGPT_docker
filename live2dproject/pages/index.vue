<template>
  <div>
    <Live2dVue />
    <ChatInput @outputmessage="renderout($event)"/>
    <div class="caption">
      {{ data }}
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
  name: 'IndexPage',
  data() {
    return {
      data: ""
    }
  },
  methods: {
    renderout(render: string) {
      this.data = render
    }
  }
})
</script>

<style>
body {
  position: relative;
  background-color: rgb(255, 240, 206);
  user-select: none;
}
.caption{
  background-color: #000;
  color: #fff;
  font-size: 32px;
  position: absolute;
  top: 30px;
  text-align: center;
}
</style>