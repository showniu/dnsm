import request from '@/utils/request'
export function getOpLogList(params) {
    return request({
      url: '/api/oplog',
      method: 'get',
      baseURL: 'http://10.2.0.62:8000',
      params
    })
  }