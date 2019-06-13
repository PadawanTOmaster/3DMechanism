import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/Index'
import homepage from '@/components/Homepage'
import fourbar from '@/components/fourbar'
import forcebar from '@/components/forcebar'
import gear from '@/components/gear'
import login from '@/components/login'
import signup from '@/components/signup'
import download from '@/components/download'
import practice from '@/components/practice'
import encyclopedia from '@/components/encyclopedia'
import crankrocker from "@/components/crankrocker"
import slidercrank from '@/components/slidercrank'
import crankguide from '@/components/crankguide'
import threed from '@/components/threed'
import news from '@/components/news'
import other from '@/components/other'
import manage from '@/components/manage'
import forceoscillation from '@/components/forceoscillation'
import points from '@/components/points'
Vue.use(Router)

const router =  new Router({
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index
    },
    {
	  path:'/homepage',
	  name:'homepage',
	  component:homepage
    },
    {
      path:'/fourbar',
      name:'fourbar',
      component:fourbar
    },
    {
      path:'/gear',
      name:'gear',
      component:gear
    },
    {
      path:'/signup',
      name:'signup',
      component:signup,
    },
    {
      path:'/login',
      name: 'login',
      component: login,
    },
    {
      path:'/practice',
      name:'practice',
      component:practice
    },
    {
      path:'/encyclopedia',
      name: 'encyclopedia',
      component: encyclopedia,
    },
    {
      path:'/download',
      name:'download',
      component:download,
    },
    {
      path:'/forcebar',
      name:'forcebar',
      component:forcebar,
    },
    {
      path: '/crankrocker',
      name: 'crankrocker',
      component: crankrocker,
    },
    {
      path: '/slidercrank',
      name:'slidercrank',
      component:slidercrank,
    },
    {
      path: '/crankguide',
      name: 'crankguide',
      component: crankguide,
    },
    {
      path:'/threed',
      name:'threed',
      component:threed,
    },
    {
      path:'/manage',
      name:'manage',
      component:manage,
    },
    {
      path:'/news',
      name:'news',
      component:news,
    },
    {
      path: '/other',
      name: 'other',
      component: other,
    },
    {
      path: '/forceoscillation',
      name: 'forceoscillation',
      component: forceoscillation
    },
    {
      path:'/points',
      name:'points',
      component:points
    }
  ]
})

router.beforeEach((to, from, next) => {
  next();
  if(localStorage.getItem("token")!=undefined)
  {
    next();
  }
  else
  {
    if(to.name == 'signup') 
    {
      next();
    } 
    else {
      next();
      next('/login');
    }
  }
})
export default router;
