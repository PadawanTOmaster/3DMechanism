import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/Index'
// import homepage from '@/components/Homepage'
// import login from '@/components/login'
// import signup from '@/components/signup'
// import download from '@/components/download'
// import practice from '@/components/practice'
// import encyclopedia from '@/components/encyclopedia'
import fourbar from '@/components/fourbar'
import forcebar from '@/components/forcebar'
import gear from '@/components/gear'
import crankrocker from "@/components/crankrocker"
import slidercrank from '@/components/slidercrank'
import crankguide from '@/components/crankguide'
import forceoscillation from '@/components/forceoscillation'
import fourbarvr from '@/components/fourbarvr'
import forcebarvr from '@/components/forcebarvr'
import gearvr from '@/components/gearvr'
import crankrockervr from "@/components/crankrockervr"
import slidercrankvr from '@/components/slidercrankvr'
import crankguidevr from '@/components/crankguidevr'
import forceoscillationvr from '@/components/forceoscillationvr'
import threed from '@/components/threed'
// import news from '@/components/news'
// import other from '@/components/other'
// import manage from '@/components/manage'
import points from '@/components/points'
import spectrometer from '@/components/spectrometer'

Vue.use(Router)

const router =  new Router({
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index
    },
    // {
	  // path:'/homepage',
	  // name:'homepage',
	  // component:homepage
    // },
    {
      path:'/fourbar',
      name:'fourbar',
      component:fourbar
    },
    {
      path: '/fourbarvr',
      name: 'fourbarvr',
      component: fourbarvr
    },
    {
      path:'/gear',
      name:'gear',
      component:gear
    },
    {
      path: '/gearvr',
      name: 'gearvr',
      component: gearvr
    },
    // {
    //   path:'/signup',
    //   name:'signup',
    //   component:signup,
    // },
    // {
    //   path:'/login',
    //   name: 'login',
    //   component: login,
    // },
    // {
    //   path:'/practice',
    //   name:'practice',
    //   component:practice
    // },
    // {
    //   path:'/encyclopedia',
    //   name: 'encyclopedia',
    //   component: encyclopedia,
    // },
    // {
    //   path:'/download',
    //   name:'download',
    //   component:download,
    // },
    {
      path:'/forcebar',
      name:'forcebar',
      component:forcebar,
    },
    {
      path: '/forcebarvr',
      name: 'forcebarvr',
      component: forcebarvr,
    },
    {
      path: '/crankrocker',
      name: 'crankrocker',
      component: crankrocker,
    },
    {
      path: '/crankrockervr',
      name: 'crankrockervr',
      component: crankrockervr,
    },
    {
      path: '/slidercrank',
      name:'slidercrank',
      component:slidercrank,
    },
    {
      path: '/slidercrankvr',
      name: 'slidercrankvr',
      component: slidercrankvr,
    },
    {
      path: '/crankguide',
      name: 'crankguide',
      component: crankguide,
    },
    {
      path: '/crankguidevr',
      name: 'crankguidevr',
      component: crankguidevr,
    },
    {
      path:'/threed',
      name:'threed',
      component:threed,
    },
    // {
    //   path:'/manage',
    //   name:'manage',
    //   component:manage,
    // },
    // {
    //   path:'/news',
    //   name:'news',
    //   component:news,
    // },
    // {
    //   path: '/other',
    //   name: 'other',
    //   component: other,
    // },
    {
      path: '/forceoscillation',
      name: 'forceoscillation',
      component: forceoscillation
    },
    {
      path: '/forceoscillationvr',
      name: 'forceoscillationvr',
      component: forceoscillationvr
    },
    {
      path:'/points',
      name:'points',
      component:points
    },
    {
      path:'/spectrometer',
      name:'spectrometer',
      component: spectrometer
    }
  ]
})
export default router;
