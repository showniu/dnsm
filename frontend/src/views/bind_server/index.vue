<template>
  <div class="app-container">
    <el-container>
      <el-header height="30px">
        <el-button type="primary" @click="addNewServer = true">新增服务器</el-button>
        <el-button type="primary" icon="el-icon-refresh" @click="refreshData" style="float: right">刷新</el-button>
      </el-header>
      <el-main>
        <el-dialog title="新增服务器" :visible.sync="addNewServer">
          <el-form :model="serverForm" ref="dataForm">
            <el-form-item label="主机名" :lable-width="formLabelWidth">
              <el-input v-model="serverForm.plat_server_hostname" auto-complete="off"></el-input>
            </el-form-item>
            <el-form-item label="主机IP" :lable-width="formLabelWidth">
              <el-input v-model="serverForm.plat_server_ip" auto-complete="off"></el-input>
            </el-form-item>
            <el-form-item label="通信端口" label-width="formLabelWidth">
              <el-input v-model="serverForm.plat_server_port" >
              </el-input>
            </el-form-item>

            <el-form-item label="是否免密登录">
              <el-radio-group v-model="serverForm.plat_server_nopass">
                <el-radio label="true" />
              </el-radio-group>
            </el-form-item>

            <el-form-item label="角色" label-width="formLabelWidth">
              <el-select v-model="serverForm.plat_server_role" placeholder="角色">
              </el-select>
            </el-form-item>

          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button type="primary" @click="addNewServer = false">取消</el-button>
            <el-button type="primary" @click="SubmitAddNewServer">确定</el-button>
          </div>
        </el-dialog>
        <el-table
          v-loading="listLoading"
          :data="list"
          element-loading-text="Loading"
          border
          fit
          stripe
          highlight-current-row>
          <el-table-column align="center" sortable label="ID" prop="id" width="60px">
          </el-table-column>
          <el-table-column align="center" sortable label="新增时间" prop="plat_server_createtime" width="150px">
          </el-table-column>
          <el-table-column align="center" sortable label="主机名" prop="plat_server_hostname" width="150px">
          </el-table-column>
          <el-table-column align="center" sortable label="主机IP" prop="plat_server_ip" fit="ture" width="130px">
          </el-table-column>
          <el-table-column align="center" sortable label="通信端口" prop="plat_server_port" fit="ture" width="110px">
          </el-table-column>
          <el-table-column align="center" sortable label="免密登录" prop="plat_server_nopass" fit="ture" width="110px">
          </el-table-column>
          <el-table-column align="center" sortable label="角色" prop="plat_server_role" fit="ture" width="100px">
          </el-table-column>
          <el-table-column align="center" sortable label="初始化" prop="plat_server_role" fit="ture">
            <template slot-scope="scope">
              <el-button v-if="scope.row.plat_server_init === '2'" type="success" size="mini" @click="SubInitServer(scope.row.plat_server_ip)" disabled>
                已初始化
              </el-button>
              <el-button v-else-if="(scope.row.plat_server_init === '1')" type="info" size="mini" @click="SubInitServer(scope.row.plat_server_ip)" disabled :loading="true">
                初始化中
              </el-button>
              <el-button v-else-if="(scope.row.plat_server_init === '3')" type="warning" size="mini" @click="SubInitServer(scope.row.plat_server_ip)" disabled>
                初始化失败
              </el-button>
              <!--  v-else-if="(scope.row.plat_server_init === null || scope.row.plat_server_init == '0')"-->
              <el-button v-else type="primary" size="mini" @click="SubInitServer(scope.row.plat_server_ip)">
                未初始化
              </el-button>
              <el-button v-if="(scope.row.plat_server_init === '3')" type="danger" size="mini" @click="RestServerState(scope.row.id)">重置状态</el-button>
            </template>
          </el-table-column>
          <el-table-column align="center" sortable label="操作" fit="ture" width="100px">
            <template slot-scope="scope">
              <el-button type="danger" size="mini" @click="SubmitDelServer(scope.row.id)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-main>
    </el-container>
  </div>
</template>
<script>
import { getServerList, addServer, delServer, initServer, restServerState } from '@/api/bindserver/bindserverapi'
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
      listLoading: true,
      addNewServer: false,
      serverForm: {
        plat_server_hostname: 'test-host01',
        plat_server_ip: '1.1.1.1',
        plat_server_port: '22',
        plat_server_nopass: 'true',
        plat_server_role: 'master'
      },
      formLabelWidth: '50px'
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.listLoading = true
      getServerList().then(response => {
        this.list = response
        this.listLoading = false
      })
    },
    refreshData() {
      this.listLoading = true
      this.fetchData()
      delay: 1
    },   
    SubmitAddNewServer() {
      if (this.serverForm) {
        addServer(this.serverForm).then(res => {
          this.$notify({
            title: '添加成功',
            type: 'success',
            duration: 2500
          })
          this.addNewServer = false
          this.fetchData()
        }).catch(err => {
          this.listLoading = false
          console.log(err.response.data)
        })
      }
    },
    SubmitDelServer(indexId) {
      console.log('取值:', indexId)
      delServer(indexId).then(res => {
        this.$notify({
          title: '删除成功',
          type: 'success',
          duration: '2500'
        })
        this.fetchData()
      }).catch(err => {
        this.listLoading = false
        console.log(err.response.data)
      })
    },
    SubInitServer(serverIP) {
      const serverIPlist = []
      serverIPlist.push(serverIP)
      console.log(serverIPlist)
      initServer(serverIPlist).then(res => {
        this.$notify({
          title: '任务添加成功',
          type: 'success',
          duration: 2500
        })
        this.fetchData()
      }).catch(err => {
        this.listLoading = false
        console.log(err.response.data)
      })
    },
    RestServerState(obj_id) {
      restServerState(obj_id).then(res => {
        this.$notify({
          title: '重置成功',
          type: 'success',
          duration: '2500'
        })
        this.fetchData()
      }).catch(err => {
        this.listLoading = false
        console.log(err.response.data)
      })
    },
    BulkSubInitServer() {
      console.log(this.subInitServers)
    }
  }
}
</script>
