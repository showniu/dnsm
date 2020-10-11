<template>
  <div class="app-container">
    <el-container>
      <el-header height="30px">
        <el-button type="primary" @click="addNewZoneDialog = true;">新增域名</el-button>
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
          <el-table-column align="center" sortable label="域名" prop="zone_name" width="aotu" min-width="60px" />
          <el-table-column align="center" sortable label="域名类型" prop="zone_type" width="120px" />
          <el-table-column align="left" sortable label="解析区域(线路)" prop="zone_from_view" width="auto" min-width="60px">
            <template slot-scope="scope">
              <el-tag
                v-for="(item, index) in scope.row.zone_from_view"
                :key="index"
                style="margin-left: 5px; margin-top: 2px; min-width: 100px"
              >{{ item }}</el-tag>
            </template>
          </el-table-column>
<!--          <el-table-column align="center" sortable label="域名记录文件" placeholder="当域名类型为fordwords时、此处为空" prop="zone_file" width="auto" min-width="60px" />-->
<!--          <el-table-column align="center" sortable label="域名转发目标" placeholder="当域名类型为master时、此处为空" prop="zone_forwarders" width="auto" min-width="60px" />-->
          <el-table-column align="center" sortable label="操作" fit="ture" width="200px">
            <template slot-scope="scope">
              <el-button size="mini" @click="editZoneDialog = true; handEditZone(scope.row)">编辑</el-button>
              <el-button type="danger" size="mini" @click="SubmitDelZone(scope.row.id)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-dialog title="新增域名" :visible.sync="addNewZoneDialog">
          <el-form v-loading="listLoading" :model="submitAddZoneForm">
            <el-form-item label="域名" label-width="formLabelWidth">
              <el-input v-model="submitAddZoneForm.zone_name" placeholder="定义一个域名" required="true" />
            </el-form-item>
            <el-form-item label="域名类型" label-width="formLabelWidth">
              <el-radio-group v-model="submitAddZoneForm.zone_type">
                <el-radio v-for="type_option in addZoneType" :key="type_option" :label="type_option" />
              </el-radio-group>
            </el-form-item>
            <el-form-item label="域名生效区域" label-width="formLabelWidth">
              <el-checkbox v-model="checkAll" :indeterminate="isIndeterminate" @change="handleCheckAllChange">全选</el-checkbox>
              <div style="margin: 15px 0;" />
              <el-checkbox-group v-model="submitAddZoneForm.zone_from_view" @change="handleCheckedViewNameChange">
                <el-checkbox v-for="view_option in addZoneView" :key="view_option" :label="view_option" border size="medium" />
              </el-checkbox-group>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button type="primary" @click="addNewZoneDialog = false">取消</el-button>
            <el-button type="primary" @click="SubmitAddNewZone">确定</el-button>
          </div>
        </el-dialog>
        <el-dialog title="编辑域名" :visible.sync="editZoneDialog">
          <el-form :model="submitEditZoneForm">
            <el-form-item label="域名" label-width="formLabelWidth">
              <el-input v-model="submitEditZoneForm.zone_name" placeholder="定义一个域名" disabled />
            </el-form-item>
            <el-form-item label="域名生效区域" label-width="formLabelWidth">
              <el-checkbox v-model="checkAll" :indeterminate="isIndeterminate" @change="handleCheckAllEditViewChange">全选</el-checkbox>
              <div style="margin: 15px 0;" />
              <el-checkbox-group v-model="submitEditZoneForm.zone_from_view" @change="handleCheckedEditViewChange">
                <el-checkbox v-for="viewItem in addZoneView" :key="viewItem" :label="viewItem">{{ viewItem }}</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button type="primary" @click="editZoneDialog = false">取消</el-button>
            <el-button type="primary" @click="SubmitEditZone">确定</el-button>
          </div>
        </el-dialog>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import { getAclViewList, getZoneList, addZone, delZone, editZone } from '@/api/bindservice/bindserviceapi'
export default {
  filter: {
    statusFilter(status) {
      const statusMap = {
        published: 'succcess',
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
      addNewZoneDialog: false,
      editZoneDialog: false,
      addZoneType: ['master', 'forward'],
      addZoneView: [],
      submitAddZoneForm: {
        zone_from_view: []
      },
      submitEditZoneForm: {},
      checkAll: false,
      isIndeterminate: true,
      formLabelWidth: '50px'
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.listLoading = true
      getZoneList().then(respone => {
        const zone_from_view_data = respone.data
        for (const item of zone_from_view_data) {
          const zone_from_view = item.zone_from_view
          const format_zone_from_view = zone_from_view.split(',')
          item.zone_from_view = format_zone_from_view
        }
        this.list = respone.data
        this.listLoading = false
      })
      if (this.addZoneView.length > 0) {
        this.addZoneView.clear() // 清理对象数据、否则会出现重复的选项
      }
      getAclViewList().then(response => {
        this.getViewData = response.data
        this.getViewData.forEach((item, index) => {
          this.addZoneView.push(item.view_name)
          this.listLoading = false
        })
      })
    },
    handleCheckAllChange(val) {
      this.submitAddZoneForm.zone_from_view = val ? this.addZoneView : []
      this.isIndeterminate = false
    },
    handleCheckedViewNameChange(value) {
      const checkedCount = value.length
      this.checkAll = checkedCount === this.addZoneView.length
      this.isIndeterminate = checkedCount > 0 && checkedCount < this.addZoneView.length
    },
    handleCheckAllEditViewChange(val) {
      this.submitEditZoneForm.zone_from_view = val ? this.addZoneView : []
      this.isIndeterminate = false
    },
    handleCheckedEditViewChange(value) {
      const checkedCount = value.length
      this.checkAll = checkedCount === this.addZoneView.length
      this.isIndeterminate = checkedCount > 0 && checkedCount < this.addZoneView.length
    },
    SubmitAddNewZone() {
      // console.log('原始数据', this.submitAddZoneForm)
      if (this.submitAddZoneForm.zone_from_view) {
        addZone(this.submitAddZoneForm).then(res => {
          this.$notify({
            title: '添加成功',
            type: 'success',
            duration: 2500
          })

          this.addNewZoneDialog = false // 关闭弹框
          this.fetchData() // 重新加载数据
        }).catch(err => {
          this.listLoading = false
          console.log(err.response)
        })
      }
    },
    SubmitDelZone(indexId) {
      console.log('取值:', indexId)
      delZone(indexId).then(res => {
        this.$notify({
          title: '删除成功',
          type: 'success',
          duration: '2500'
        })
        this.fetchData()
      }).catch(err => {
        this.listLoading = false
        console.log(err.response)
      })
    },
    handEditZone(params) {
      // params 获取当前操作行的数据
      const zoneId = params.id
      const zoneFromViewList = params.zone_from_view
      const zoneName = params.zone_name
      // 向submitEditZoneForm dict赋值已经被选中的选项、
      this.$set(this.submitEditZoneForm, 'id', zoneId)
      this.$set(this.submitEditZoneForm, 'zone_name', zoneName)
      this.$set(this.submitEditZoneForm, 'zone_from_view', zoneFromViewList)
    },
    SubmitEditZone() {
      if (this.submitEditZoneForm) {
        const obj_id = this.submitEditZoneForm.id
        const obj_zoneFromView_values = Object.values(this.submitEditZoneForm.zone_from_view) // 获取list对象值
        const obj_zoneFromView_str = obj_zoneFromView_values.join(',') // 将list 转换为str、传到后端处理
        this.$set(this.submitEditZoneForm, 'zone_from_view', obj_zoneFromView_str)
        editZone(obj_id, this.submitEditZoneForm).then(res => {
          this.$notify({
            title: '修改成功',
            type: 'success',
            duration: 2500
          })
          this.editZoneDialog = false // 关闭弹框
          this.fetchData() // 重新加载数据
        }).catch(err => {
          this.listLoading = false
          console.log(err.response.data)
        })
      }
      console.log('提交的参数:', this.submitEditZoneForm)
    }
  }
}
</script>
