<template>
  <div class="app-container">
    <el-container>
      <el-header height="30px">
        <el-form :inline="true">
          <el-form-item> 
            <el-button type="primary" icon="el-icon-refresh" @click="refreshData" style="float: left">刷新</el-button>
          </el-form-item>
          <el-form-item style="float: right">
            <el-button type="primary" @click="buildConf()">配置生成</el-button>
            <el-button type="primary" @click="relatedServerDialog = true;">配置关联</el-button>
          </el-form-item>
        </el-form>
      </el-header>
      <el-main>
        <el-table
          v-loading="listLoading"
          :data="list"
          element-loading-text="Loading"
          border
          fit
          stripe
          highlight-current-row
        >
          <el-table-column align="center" sortable label="版本标签" prop="tag_name" width="250" />
          <el-table-column align="center" sortable label="是否测试" prop="tag_test" width="150" /> 
          <el-table-column align="center" sortable label="关联服务器" prop="tag_related_server" fit="ture">
            <template slot-scope="scope">
              <el-tag
                v-for="(item, index) in scope.row.tag_related_server"
                :key="index"
                style="margin-left: 5px; margin-top: 2px; min-width: 100px"
              >{{ item }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column align="center" sortable label="当前状态" prop="tag_currentstatus" fit="ture">
            <template slot-scope="scope">
              <el-tag
                v-for="(item, index) in scope.row.tag_currentstatus"
                :key="index" :type="item.type" 
                style="margin-left: 5px; margin-top: 2px; min-width: 100px"
                effect="plain">{{item.info}}</el-tag>
            </template>
          </el-table-column>
          <el-table-column align="center" sortable label="操作" fit="ture">
            <template slot-scope="scope">
              <el-button v-loading="scope.row.syncLoading" type="primary" @click="syncToServer(scope.row)">配置下发</el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-dialog title=配置关联到服务器 :visible.sync="relatedServerDialog" label-position="right">
          <el-form :model="relatedServerFrom">
              <el-form-item label="选择配置标签" label-width="110px">
                <el-select  style="width: 300px" v-model="relatedServerFrom.tag_id" value-key="relatedServerFrom.tag_id" placeholder="选择配置标签">
                  <el-option v-for="item in list" :key="item.id" :label="item.tag_name" :value="item.id"></el-option>
                </el-select>                
              </el-form-item>
              <el-form-item label="选择关联服务器" label-width="110px">
                  <el-select style="width: 300px; higth: 100px" v-model="relatedServerFrom.servers" placeholder="选择关联服务器" clearable multiple filterable>
                    <el-option v-for="item in serverIPList" :key="item.plat_server_ip" :label="item.plat_server_ip" :value="item.plat_server_ip"></el-option>
                  </el-select>
              </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button type="primary" @click="relatedServerDialog=false">取消</el-button>
            <el-button type="primary" @click="submitTagRelatedServer">确定</el-button>
          </div>
        </el-dialog>
      </el-main>      
    </el-container>
  </div>
</template>

<script>
import { getGitConfTag, syncConfToServer, buildPushGitlab, tagRelatedServer } from '@/api/bindconfig/bindconfigapi'
import { getServerIpList } from '@/api/bindserver/bindserverapi'
import { Notification } from 'element-ui'
export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'gray',
        deleted: 'danger'
      }
      return statusMap[status]
    }
  },
  data() {
    return {
      list: null,
      slist: null,
      listLoading: true,
      mutipleSync: false,
      relatedServerDialog: false,
      syncToServerDialog: false,
      serverIPList: [], // API 返回的 Serverlist
      formLabelWidth: '50px',
      relatedServerFrom: {
        tag_id: null
      },
      syncToServerFrom: {
        tag_id: null,
        tag_name: null
      },
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.listLoading = true
      getGitConfTag().then(response => {
        this.slist = response
        this.slist.forEach((item, index) => {
          if (item.tag_related_server != null) {
            const currentstatus = item.tag_currentstatus
            const curt = eval('(' + currentstatus + ')')
            item.tag_currentstatus = curt
            const server = item.tag_related_server
            const sn = eval('(' + server + ')')
            item.tag_related_server = sn
          }
        })
        this.list = this.slist
        // 添加默认值  
        this.relatedServerFrom.tag_id = this.list[0].id
        this.listLoading = false
      })
      if (this.serverIPList.length > 0) {
        const x_none = []
        this.serverIPList = x_none
      }
      getServerIpList().then(response => {
        this.serverIpData = response
        this.serverIPList = this.serverIpData
      })
    },
    refreshData() {
      this.listLoading = true
      this.fetchData()
      delay: 1
    },  
    buildConf() {
      buildPushGitlab().then(response => {
       this.$notify({
          title: '任务已创建',
          type: 'success',
          duration: '2500'
        })
        this.fetchData()
      }).catch(err => {
        this.listLoading = false
        console.log(err.response)
      })
    },
    submitTagRelatedServer() {
      // console.log('服务器关联', this.relatedServerFrom)
      tagRelatedServer(this.relatedServerFrom).then(response => {
        this.$notify({
          title: '任务已经创建',
          type: 'success',
          duration: '2500'
        })
        this.fetchData()
        }).catch(err => {
          this.listLoading = false
      })
      this.relatedServerDialog = false
    },
    syncToServer(row) {
      this.syncToServerFrom.tag_id = row.id
      this.syncToServerFrom.tag_name = row.tag_name

      syncConfToServer(this.syncToServerFrom).then(res => {
        this.$notify({
          title: '任务下发成功',
          type: 'success',
          duration: '2500'
        })
        this.fetchData()
      }).catch(err => {
        console.log(err.response.data)
      })  
    } 
  }
}
</script>