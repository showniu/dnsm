import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },

  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: { title: '首页', icon: 'dashboard' }
    }]
  },

  {
    path: '/bindserver',
    component: Layout,
    children: [{
      path: '/bindserver',
      name: 'DNS服务器',
      component: () => import('@/views/bind_server/index'),
      meta: { title: 'DNS服务器', icon: 'dashboard' }
    }]
  },

  {
    path: '/bindservice',
    component: Layout,
    redirect: '/bindservice/lineregion',
    name: 'Bind服务',
    meta: { title: 'Bind服务', icon: 'el-icon-s-help' },
    children: [
      {
        path: '/lineregion',
        name: '区域和线路',
        component: () => import('@/views/bind_service/line_region'),
        meta: { title: '区域和线路', icon: 'form' }
      },
      {
        path: '/domain',
        name: '域名管理',
        component: () => import('@/views/bind_service/domain'),
        meta: { title: '域名管理', icon: 'form' }
      },
      {
        path: '/record',
        name: '记录管理',
        component: () => import('@/views/bind_service/record'),
        meta: { title: '记录管理', icon: 'form' }
      }
    ]
  },
  {
    path: '/configmanager',
    component: Layout,
    redirect: '/configmanager',
    name: 'Bind配置管理',
    meta: { title: 'Bind配置管理', icon: 'el-icon-s-help' },
    children: [
      {
        path: '/configsync',
        name: '配置同步',
        component: () => import('@/views/config_manager/config_sync'),
        meta: { title: '配置同步', icon: 'form' }
      }
    ]
  },
  {
    path: '/operationlog',
    component: Layout,
    redirect: '/operationlog',
    name: '操作日志',
    meta: { title: '操作日志', icon: 'el-icon-s-help' },
    children: [
      {
        path: '/bindlog',
        name: 'Bind操作日志',
        component: () => import('@/views/operation_log/index'),
        meta: { title: 'Bind操作日志', icon: 'form' }
      }
    ]
  },
  {
    path: '/example',
    component: Layout,
    redirect: '/example/table',
    name: 'Example',
    meta: { title: 'Example', icon: 'el-icon-s-help' },
    children: [
      {
        path: 'table',
        name: 'Table',
        component: () => import('@/views/table/index'),
        meta: { title: 'Table', icon: 'table' }
      },
      {
        path: 'tree',
        name: 'Tree',
        component: () => import('@/views/tree/index'),
        meta: { title: 'Tree', icon: 'tree' }
      }
    ]
  },
  {
    path: 'external-link',
    component: Layout,
    children: [
      {
        path: 'https://panjiachen.github.io/vue-element-admin-site/#/',
        meta: { title: 'External Link', icon: 'link' }
      }
    ]
  },

  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
