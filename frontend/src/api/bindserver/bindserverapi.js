import request from '@/utils/request'

export function getServerList(params) {
  return request({
    url: '/api/bindserver/list',
    method: 'get',
    baseURL: 'http://127.0.0.1:8000',
    params
  })
}

export function addServer(data) {
  return request({
    url: '/api/bindserver/list',
    method: 'post',
    baseURL: 'http://127.0.0.1:8000',
    data
  })
}

export function delServer(id) {
  return request({
    url: `/api/bindserver/list/${id}`,
    baseURL: 'http://127.0.0.1:8000',
    method: 'delete'
  })
}

