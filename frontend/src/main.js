// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

import ElementUI from 'element-ui'
import axios from 'axios'
import Qs from 'qs'
import echarts from 'echarts'
import $ from 'jquery'
import 'font-awesome/css/font-awesome.min.css'
import 'element-ui/lib/theme-chalk/index.css'
import Topbar from './components/topbar/index'

Vue.use(Topbar)
Vue.use(ElementUI)
axios.defaults.baseURL = 'http://3d1.top/api'
Vue.config.productionTip = false;
Vue.prototype.axios = axios;
Vue.prototype.qs = Qs;
Vue.prototype.$=$;
Vue.prototype.$echarts=echarts
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})


