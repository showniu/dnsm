<template>
  <div class="app-container">
    <el-container>
      <el-header height="30px">
        <el-button type="primary" @click="addNewAclView = true">新增区域和线路</el-button>
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
          <el-table-column align="center" sortable label="ID" prop="id" width="80px" />
          <el-table-column align="center" sortable label="区域" prop="view_name" width="90px" />
          <el-table-column align="center" sortable label="区域对应线路" prop="acl_name" width="130px" />
          <el-table-column align="left" sortable label="线路范围" prop="acl_value" width="auto">
            <template slot-scope="scope">
              <el-tag
                v-for="(item, index) in scope.row.acl_value"
                :key="index"
                style="margin-left: 5px; margin-top: 2px; min-width: 100px"
              >{{ item }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column align="center" sortable label="操作" fit="ture" width="200px">
            <template slot-scope="scope">
              <el-button size="mini" @click="editAclViewDialog = true; handEditAclView(scope.row.id, scope.row)">编辑</el-button>
              <el-button type="danger" size="mini" @click="SubmitDelAclView(scope.row.id)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-dialog title="新增区域和线路" :visible.sync="addNewAclView">
          <el-form ref="dataForm" :model="AclViewForm">
            <el-form-item label="区域" :lable-width="formLabelWidth">
              <el-input v-model="AclViewForm.view_name" placeholder="定义一个区域" />
            </el-form-item>
            <el-form-item label="线路范围" :lable-width="formLabelWidth">
              <el-input v-model="AclViewForm.acl_value" type="textarea" placeholder="网段信息、换行符分割; 192.168.1.0/24" />
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button type="primary" @click="addNewAclView = false">取消</el-button>
            <el-button type="primary" @click="SubmitAddNewAclView">确定</el-button>
          </div>
        </el-dialog>
        <el-dialog title="编辑数据" :visible.sync="editAclViewDialog">
          <el-form :model="editAclViewForm">
            <el-form-item label="线路范围">
              <el-input v-model="editAclViewForm.acl_value" :autosize="{minRows:2}" type="textarea" auto-complete="off" />
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button type="primary" @click="editAclViewDialog = false">取消</el-button>
            <el-button type="primary" @click="SubmitEditAclView">确定</el-button>
          </div>
        </el-dialog>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import { getAclViewList, addAclView, delAclView, editAclView } from '@/api/bindservice/bindserviceapi'
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
      addNewAclView: false,
      editAclViewDialog: false,
      AclViewForm: {
        acl_value: '',
        view_name: ''
      },
      editAclViewForm: {},
      formLabelWidth: '50px'
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.listLoading = true
      getAclViewList().then(response => {
        const aclview = response.data
        for (const item of aclview) {
          const acl_value = item.acl_value
          const format_acl_value = acl_value.split(',')
          item.acl_value = format_acl_value
        }
        // response.data.forEach((item, index) => {
        //   const acl_value =  item.acl_value
        //   const format_acl_value = acl_value.split(" ")
        //   item.acl_value = format_acl_value
        // })

        this.list = response.data
        this.listLoading = false
      })
    },
    SubmitAddNewAclView() {
      console.log('新增的参数', this.AclViewForm)
      if (this.AclViewForm) {
        addAclView(this.AclViewForm).then(res => {
          this.$notify({
            title: '添加成功',
            type: 'success',
            duration: 2500
          })
          this.addNewAclView = false // 关闭弹框
          this.fetchData() // 重新加载数据
        }).catch(err => {
          this.listLoading = false
          console.log(err.response.data)
        })
      }
    },
    SubmitDelAclView(indexId) {
      console.log('取值:', indexId)
      delAclView(indexId).then(res => {
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
    handEditAclView(indexID, params) {
      const aclValue = Object.values(params.acl_value)
      const aclValueStr = aclValue.join(',')

      this.editAclViewForm = {
        id: indexID,
        acl_value: aclValueStr
      }
    },
    SubmitEditAclView() {
      if (this.editAclViewForm) {
        const obj_id = this.editAclViewForm.id
        editAclView(obj_id, this.editAclViewForm).then(res => {
          this.$notify({
            title: '修改成功',
            type: 'success',
            duration: 2500
          })
          this.editAclViewDialog = false // 关闭弹框
          this.fetchData() // 重新加载数据
        }).catch(err => {
          this.listLoading = false
          console.log(err.response.data)
        })
      }
      console.log('提交的参数:', this.editAclViewForm)
    }

  }
}
</script>
<style>

</style>
