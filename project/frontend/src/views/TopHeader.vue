<template>
  
<rux-pop-up-menu id="popup-menu-1">
    <rux-menu-item>
      <router-link :to="{name: 'home'}">
        Dashboard
      </router-link>
    </rux-menu-item>
    <rux-menu-item-divider></rux-menu-item-divider>
    <rux-menu-item @click="logout">Sign Out</rux-menu-item>
</rux-pop-up-menu>

<rux-global-status-bar app-domain="Coding Challenge" 
          username="created by Darin Nickloy" 
          include-icon="true"
          menu-icon="developer-mode"
          app-version="0.72-delta">
    <rux-clock class="right"></rux-clock>
    <rux-icon icon="settings" label="Settings" color="#fff" @click="displayPopupMenu" aria-controls="popup-menu-1" aria-haspopup="true" class="icon"></rux-icon>
  </rux-global-status-bar>
</template>

<script>
// Import Astro controls.
import { RuxGlobalStatusBar } from '@astrouxds/astro-web-components/dist/components/rux-global-status-bar'
import { RuxClock } from '@astrouxds/astro-web-components/dist/components/rux-global-status-bar'

export default {
    name: 'TopHeader',
    setup(){
        const logout = () =>{
          localStorage.clear()
          window.location.href = '/login'
        }
        return {logout}
    }

}
</script>

<style>
.right{
  margin-left: auto;
  margin-right: 0px;
}
.icon{
  margin-left: 15px;
  margin-top: 5px;
}

</style>
