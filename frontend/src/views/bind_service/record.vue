<template>
  <div class="app-container">
    <el-container>
      <el-header>
        <el-form :inline="true">
          <el-form-item>
            <el-input v-model="search_key.search" placeholder="搜索主机记录" class="form-control" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" icon="el-icon-search" @click="fetchData">搜索</el-button>
          </el-form-item>
          <el-form-item style="float: right">
            <el-button type="primary" @click="fetchZoneList">新增记录</el-button>
          </el-form-item>
        </el-form>
      </el-header>
      <div style="margin: 1px;" />
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
          <el-table-column align="center" sortable label="ID" prop="id" width="60px" />
          <el-table-column align="center" sortable label="主机记录" prop="record_key" min-width="40px" />
          <el-table-column align="center" sortable label="记录类型" prop="record_type" min-width="25px" />
          <el-table-column align="center" sortable label="记录值" prop="record_value" min-width="50px" />
          <el-table-column align="center" sortable label="所属域名" prop="record_zone" min-width="60px" />
          <el-table-column align="center" sortable label="解析区域(线路)" prop="record_from_view" min-width="35px">
            <template slot-scope="scope">
              <el-tag>{{ scope.row.record_from_view }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column align="center" sortable label="备注" prop="record_remarks" min-width="40px" />
          <el-table-column align="center" sortable label="操作" width="200px">
            <template slot-scope="scope">
              <el-button size="mini" @click="handEditRecord(scope.row)">编辑</el-button>
              <el-button type="danger" size="mini" @click="SubmitDelRecord(scope.row.id)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-dialog title="新增记录" :visible.sync="addNewRecordDialog" width="40%">
          <el-form :model="addNewRecordForm" label-position="right">
            <el-form-item label="记录类型" label-width="80px">
              <el-radio-group v-model="addNewRecordForm.record_type">
                <el-radio v-for="type_option in recordTypeOption" :key="type_option" :label="type_option" border />
              </el-radio-group>
            </el-form-item>
            <el-form-item label="所属域名" label-width="80px">
              <el-select v-model="addNewRecordForm.record_zone" filterable placeholder="选择所属域名" style="width: 70%">
                <el-option v-for="zoneOption in recordZoneOption" :key="zoneOption.zone_name" :label="zoneOption.zone_name" :value="zoneOption.zone_name" />
              </el-select>
            </el-form-item>
            <el-form-item sort-table label="所属区域" prop="record_from_view" width="auto" label-width="80px">
              <el-checkbox v-model="checkAll" :indeterminate="isIndeterminate" @change="handleCheckAllRecordChange">全选</el-checkbox>
              <div style="margin: 15px 0;" />
              <el-checkbox-group v-model="addNewRecordForm.record_from_view" @change="handleCheckedRecordChange">
                <el-checkbox v-for="view_option in recordViewOption" :key="view_option" :label="view_option" size="medium" />
              </el-checkbox-group>
            </el-form-item>
            <el-form-item label="主机记录" label-width="80px">
              <el-input v-model="addNewRecordForm.record_key" placeholder="定义一个记录" />
            </el-form-item>
            <el-form-item label="记录值" label-width="80px">
              <el-input v-model="addNewRecordForm.record_value" placeholder="记录值" />
            </el-form-item>
            <el-form-item label="备注" label-width="80px">
              <el-input v-model="addNewRecordForm.record_remarks" placeholder="记录值" />
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button type="primary" @click="addNewRecordDialog=false">取消</el-button>
            <el-button type="primary" @click="SubmitAddNewRecord">确定</el-button>
          </div>
        </el-dialog>
        <el-dialog title="编辑记录" :visible.sync="editRecordDialog" width="40%">
          <el-form v-model="editRecordForm" label-position="right">
            <el-form-item label="记录类型" label-width="110px">
              <el-radio-group v-model="editRecordForm.record_type">
                <el-radio v-for="type_option in recordTypeOption" :key="type_option" :label="type_option" border />
              </el-radio-group>
            </el-form-item>
            <el-form-item label="解析区域(线路)" label-width="110px">
              <el-input v-model="editRecordForm.record_from_views" disabled />
            </el-form-item>
            <el-form-item label="所属域名" label-width="110px">
              <el-input v-model="editRecordForm.record_zone" disabled />
            </el-form-item>
            <el-form-item label="主机记录" label-width="110px">
              <el-input v-model="editRecordForm.record_key" placeholder="定义一个记录" disabled />
            </el-form-item>
            <el-form-item label="记录值" label-width="110px">
              <el-input v-model="editRecordForm.record_value" placeholder="记录值" />
            </el-form-item>
            <el-form-item label="备注" label-width="110px">
              <el-input v-model="editRecordForm.record_remarks" placeholder="备注" />
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button type="primary" @click="editRecordDialog=false">取消</el-button>
            <el-button type="primary" @click="SubmitEditRecord">确定</el-button>
          </div>
        </el-dialog>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import { addRecord, delRecord, editRecord, getAclViewList, getRecordList, getZoneList } from '@/api/bindservice/bindserviceapi'
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
      isIndeterminate: true,
      checkAll: false,
      search_key: {
        search: null
      },
      listLoading: true,
      addNewRecordDialog: false,
      editRecordDialog: false,
      addNewRecordForm: {
        record_key: '',
        record_type: '',
        record_value: '',
        record_zone: '',
        record_from_view: [],
        record_remarks: ''
      },
      recordZoneOption: null,
      recordTypeOption: ['A', 'CNAME'],
      recordViewOption: [],
      editRecordForm: {},
      formLabelWidth: '50px'
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.listLoading = true
      getRecordList(this.search_key).then(response => {
        const record_list_data = response
        // for (const item of record_list_data) {
        //   const record_from_view = item.record_from_view
        //   const format_record_from_view = record_from_view.split(',')
        //
        //   item.record_from_view = format_record_from_view.sort()
        // }
        this.list = record_list_data
        this.listLoading = false
      })
    },
    fetchZoneList() {
      getZoneList().then(response => {
        const zoneData = response.data
        this.recordZoneOption = zoneData
      })
      if (this.recordViewOption.length > 0) {
        const x_none = []
        this.recordViewOption = x_none // 清理对象数据、否则会出现重复的选项
      }
      getAclViewList().then(response => {
        this.viewData = response.data
        this.viewData.forEach((item, index) => {
          this.recordViewOption.push(item.view_name)
          this.listLoading = false
        })
      })
      setTimeout(() => {
        this.addNewRecordDialog = true
      }, 1000)
    },
    handleCheckAllRecordChange(val) {
      this.addNewRecordForm.record_from_view = val ? this.recordViewOption : []
      this.isIndeterminate = false
    },
    handleCheckedRecordChange(value) {
      const checkedCount = value.length
      this.checkAll = checkedCount === this.recordViewOption.length
      this.isIndeterminate = checkedCount > 0 && checkedCount < this.recordViewOption.length
    },
    SubmitAddNewRecord() {
      console.log('新增的参数', this.addNewRecordForm)
      if (this.addNewRecordForm) {
        addRecord(this.addNewRecordForm).then(res => {
          this.$notify({
            title: '添加成功',
            type: 'success',
            duration: 2500
          })
          this.addNewRecordDialog = false // 关闭弹框
          this.fetchData() // 重新加载数据
        }).catch(err => {
          this.listLoading = false
          console.log(err.response.data)
        })
      }
    },
    SubmitDelRecord(indexId) {
      delRecord(indexId).then(res => {
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
    handEditRecord(params) {
      const id = params.id
      const record_key = params.record_key
      const record_value = params.record_value
      const record_type = params.record_type
      const record_remarks = params.record_remarks
      const record_zone = params.record_zone
      const record_from_view = params.record_from_view

      this.$set(this.editRecordForm, 'id', id)
      this.$set(this.editRecordForm, 'record_key', record_key)
      this.$set(this.editRecordForm, 'record_value', record_value)
      this.$set(this.editRecordForm, 'record_type', record_type)
      this.$set(this.editRecordForm, 'record_zone', record_zone)
      this.$set(this.editRecordForm, 'record_remarks', record_remarks)
      this.$set(this.editRecordForm, 'record_from_views', record_from_view)

      this.editRecordDialog = true
    },
    SubmitEditRecord() {
      if (this.editRecordForm) {
        const obj_id = this.editRecordForm.id
        editRecord(obj_id, this.editRecordForm).then(res => {
          this.$notify({
            title: '修改成功',
            type: 'success',
            duration: 2500
          })
          this.editRecordDialog = false // 关闭弹框
          this.fetchData() // 重新加载数据
        }).catch(err => {
          this.listLoading = false
          console.log(err.response.data)
        })
      }
    }
  }
}
</script>
