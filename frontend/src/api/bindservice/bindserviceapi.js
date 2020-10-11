import request from '@/utils/request'

export function getAclViewList(params) {
  return request({
    url: '/api/bindservice/aclview/list',
    method: 'get',
    baseURL: 'http://127.0.0.1:8000',
    params
  })
}

export function addAclView(data) {
  return request({
    url: '/api/bindservice/aclview/list',
    method: 'post',
    baseURL: 'http://127.0.0.1:8000',
    data
  })
}

export function delAclView(id) {
  return request({
    url: `/api/bindservice/aclview/list/${id}`,
    baseURL: 'http://127.0.0.1:8000',
    method: 'delete'
  })
}

export function editAclView(id, data) {
  return request({
    url: `/api/bindservice/aclview/list/${id}`,
    baseURL: 'http://127.0.0.1:8000',
    method: 'patch',
    data
  })
}

export function getZoneList(params) {
  return request({
    url: '/api/bindservice/zone/list',
    method: 'get',
    baseURL: 'http://127.0.0.1:8000',
    params
  })
}

export function addZone(data) {
  return request({
    url: '/api/bindservice/zone/list',
    method: 'post',
    baseURL: 'http://127.0.0.1:8000',
    data
  })
}

export function delZone(id) {
  return request({
    url: `/api/bindservice/zone/list/${id}`,
    baseURL: 'http://127.0.0.1:8000',
    method: 'delete'
  })
}

export function editZone(id, data) {
  return request({
    url: `/api/bindservice/zone/list/${id}`,
    baseURL: 'http://127.0.0.1:8000',
    method: 'patch',
    data
  })
}

export function getRecordList(params) {
  return request({
    url: '/api/bindservice/record/list',
    method: 'get',
    baseURL: 'http://127.0.0.1:8000',
    params
  })
}

export function addRecord(data) {
  return request({
    url: '/api/bindservice/record/list',
    method: 'post',
    baseURL: 'http://127.0.0.1:8000',
    data
  })
}

export function delRecord(id) {
  return request({
    url: `/api/bindservice/record/list/${id}`,
    baseURL: 'http://127.0.0.1:8000',
    method: 'delete'
  })
}

export function editRecord(id, data) {
  return request({
    url: `/api/bindservice/record/list/${id}`,
    baseURL: 'http://127.0.0.1:8000',
    method: 'patch',
    data
  })
}
