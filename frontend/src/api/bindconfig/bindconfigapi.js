import request from '@/utils/request'

export function getGitConfTag(params) {
  return request({
    url: '/api/bindconfig/confsync',
    method: 'get',
    baseURL: 'http://10.2.0.62:8000',
    params
  })
}

export function syncConfToServer(data) {
  return request({
    url: '/api/bindconfig/confsync',
    method: 'post',
    baseURL: 'http://10.2.0.62:8000',
    data
  })
}

export function buildPushGitlab(data) {
  return request({
    url: '/api/bindconfig/generate',
    method: 'post',
    baseURL: 'http://10.2.0.62:8000',
    data
  })
}

export function tagRelatedServer(data) {
  return request({
    url: '/api/bindconfig/relatedserver',
    method: 'post',
    baseURL: 'http://10.2.0.62:8000',
    data
  })
}