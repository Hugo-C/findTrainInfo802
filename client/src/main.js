import 'bootstrap/dist/css/bootstrap.css';
import BootstrapVue from 'bootstrap-vue';
import moment from 'moment';

import Vue from 'vue';
import App from './App';
import router from './router';


Vue.config.productionTip = false;

Vue.use(BootstrapVue);


Vue.filter('formatDate', function(value) {
  if (value) {
    return moment(String(value)).format('MM/DD/YYYY hh:mm')
  }
});

Vue.filter('formatDuration', function(value) {
  value /= 60;  // we discard seconds
  if (value) {
    return Math.floor(value / 60) + "H" + value % 60 + "m";
  }
});

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',
});
