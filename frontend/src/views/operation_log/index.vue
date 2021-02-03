<template>
    <div class="app-container">
        <el-container>
            <el-header height="30px" />
            <el-main>
                <el-table
                v-loading="listLoading"
                :data="list"
                element-loading-text="Loading"
                border
                fit
                stripe
                highlight-current-row>
                <el-table-column align="center" sortable label="操作时间" prop="time" width="250"></el-table-column>
                <el-table-column align="left" sortable label="操作行为" prop="msg" width=auto></el-table-column>
                </el-table>
            </el-main>
        </el-container>
    </div>
</template>

<script>
import { Notification } from 'element-ui'
import { getOpLogList } from '@/api/operation_log/oplog'

export default {
    name: "OpLog",
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
        formLabelWidth: '50px',
        }
    },
    created() {
        this.fetchData()
    },
    methods: {
        fetchData() {
        this.listLoading = true
        getOpLogList().then(response => {
            this.list = response.data
            this.listLoading = false
        })
        }
    }
}    
</script>