<template>
  <div class="app-container">
    <el-container>
      <el-header height="30px">
        <el-button type="primary" @click="addNewServer = true">新增服务器</el-button>
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
          <el-table-column align="center" sortable label="ID" prop="id" width="95">
          </el-table-column>
          <el-table-column align="center" sortable label="新增时间" prop="plat_server_createtime" width="250">
          </el-table-column>
          <el-table-column align="center" sortable label="主机名" prop="plat_server_hostname" width="150">
          </el-table-column>
          <el-table-column align="center" sortable label="主机IP" prop="plat_server_ip" fit="ture">
          </el-table-column>
          <el-table-column align="center" sortable label="通信端口" prop="plat_server_port" fit="ture">
          </el-table-column>
          <el-table-column align="center" sortable label="免密登录" prop="plat_server_nopass" fit="ture">
          </el-table-column>
          <el-table-column align="center" sortable label="角色" prop="plat_server_role" fit="ture">
          </el-table-column>
          <el-table-column align="center" sortable label="张晓萍" fit="ture"/>
          <el-table-column align="center" sortable label="操作" fit="ture">
            <template slot-scope="scope">
              <el-button type="danger" @click="SubmitDelServer(scope.row.id)">删除按钮</el-button>
            </template>
          </el-table-column>
    </el-table>
      </el-main>
    </el-container>
  </div>
</template>


<script>
import { getServerList, addServer, delServer } from '@/api/bindserver/bindserverapi'
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
        this.list = response.data
        console.log('ljpres', this.list)
        this.listLoading = false
      })
    },
    SubmitAddNewServer(){
      if(this.serverForm) {
        addServer(this.serverForm).then(res => {
          this.$notify({
            title: '添加成功',
            type: 'success',
            duration: 2500
          })
          this.addNewServer = false  //关闭弹框
          this.fetchData() //重新加载数据
        }).catch(err => {
          this.listLoading = false
          console.log(err.response.data)
        })
        }
    },
    SubmitDelServer(indexId){
      console.log("取值:", indexId)
      delServer(indexId).then(res => {
        this.$notify({
          title: "删除成功",
          type: "success",
          duration: "2500"
        })
        this.fetchData()
      }).catch(err => {
        this.listLoading =false
        console.log(err.response.data)
      })
    }
  }
}
</script>
