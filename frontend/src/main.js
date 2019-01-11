// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import VueYoutube from 'vue-youtube'
import VModal from 'vue-js-modal'
import VueCookies from 'vue-cookies'
import VueChatScroll from 'vue-chat-scroll'
import lodash from 'lodash'
import App from './App'
/* eslint-disable */

import '@/assets/styles/main.css'

Vue.use(VueChatScroll)
Vue.use(VueYoutube)
Vue.use(VueCookies)
Vue.use(VModal)

Vue.prototype.$_ = lodash

Vue.filter('truncate', function(text, stop, clamp) {
  return text.slice(0, stop) + (stop < text.length ? clamp || '...' : '')
})

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  components: { App },
  template: '<App/>'
})
