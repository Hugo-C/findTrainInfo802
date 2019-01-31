import Vue from 'vue';
import Router from 'vue-router';
import Ping from '@/components/Ping';
import Books from '@/components/Books';
import Trains from '@/components/Trains';
import NotFound from '@/components/NotFound';


Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/Ping',
      name: 'Ping',
      component: Ping,
    },
    {
      path: '/Books',
      name: 'Books',
      component: Books,
    },
    {
      path: '/Trains',
      name: 'Trains',
      component: Trains,
    },
    {
      path: '*',
      name: 'NotFound',
      component: NotFound,
    }
  ]
});
