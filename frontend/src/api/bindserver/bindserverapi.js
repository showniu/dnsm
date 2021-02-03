import request from '@/utils/request'

export function getServerList(params) {
  return request({
    url: '/api/bindserver/list',
    method: 'get',
    baseURL: 'http://10.2.0.62:8000',
    params
  })
}

export function getServerIpList(params) {
  return request({
    url: '/api/bindserver/list/ip',
    method: 'get',
    baseURL: 'http://10.2.0.62:8000',
    params
  })
}

export function addServer(data) {
  return request({
    url: '/api/bindserver/list',
    method: 'post',
    baseURL: 'http://10.2.0.62:8000',
    data
  })
}

export function delServer(id) {
  return request({
    url: `/api/bindserver/list/${id}`,
    baseURL: 'http://10.2.0.62:8000',
    method: 'delete'
  })
}

export function initServer(data) {
  return request({
    url: '/api/bindserver/init',
    baseURL: 'http://10.2.0.62:8000',
    method: 'post',
    data
  })
}

export function restServerState(obj_id) {
  return request({
    url: `/api/bindserver/reststate/${obj_id}/`,
    baseURL: 'http://10.2.0.62:8000',
    method: 'patch'
  })
}
