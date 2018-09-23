$(function () {
    var url = "http://localhost:5000";
   $('#table').bootstrapTable({
        method:'post',
        contentType:'application/x-www-form-urlencoded',
        url:url + '/get',
        toolbar:'#toolbar',
        striped: false,
        pageNumber:1,
        pageSize:15,
        pageList:[15,25,35],
        pagination: true,
        queryParamsType:'',
        queryParams:queryParams,
        sidePagination:'server',
        showColumns:true,
        showRefresh:true,
        clickToSelect:true,
        toolbarAlign: 'right',
        buttonsAlign: 'right',
        columns:[{
            title:'全选',
            field:'select',
            checkbox:'true',
            align:'center',
            valign:'middle'
        },{
            title:'id',
            field:'id',
            visible: false
        },{
            title:'标题',
            field:'title',
            formatter:formatUrl
        },{
            title:'href',
            field:'href',
            visible:false
        },{
            title:'更新时间',
            field:'update_time',
            formatter:updateTimeFormat
        }],
        locale:'zh_CN'
    });

    function updateTimeFormat(value, row, index) {
        return dateFormat(value);
    }

    function queryParams(params) {
        let param = {
            pageSize:params.pageSize,
            pageNumber:params.pageNumber
        };
        let status = $("#status").val();
        param.status = status;
        let select = $("#type").val();
        if(select == '') {

        } else if(select == 2){
            param.collection = 1;
        } else {
            param.type = select;
        }
        return param;
    }

    function dateFormat(timestamp){
        let time = new Date(timestamp * 1000);
        let y = time.getFullYear();
        let m = time.getMonth()+1;
        let d = time.getDate();
        let h = time.getHours();
        let mm = time.getMinutes();
        let s = time.getSeconds();
        return y+'-'+add0(m)+'-'+add0(d)+' '+add0(h)+':'+add0(mm)+':'+add0(s);
    }

    function add0(m){return m<10?'0'+m:m }

    function formatUrl(value, row, index){
        return "<a href='"+ row.href +"' target='_blank'>"+ value+"</a>"
    }

    $('#btn_delete').click(function () {
        var dataArr = $('#table').bootstrapTable('getSelections');
        if (dataArr.length<1){
            alert("请选择数据");
            return false;
        }
        var ids = [];
        for (let i = 0; i < dataArr.length; i++) {
            ids[i] = dataArr[i].id;
        }
        console.log(ids.join(","));
        $.get(url + "/delete?ids="+ids.join(","),function(){
                refresh();
        })
    });

    $('#btn_collection').click(function () {
        var dataArr = $('#table').bootstrapTable('getSelections');
        if (dataArr.length<1){
            alert("请选择数据");
            return false;
        }
        var ids = [];
        for (let i = 0; i < dataArr.length; i++) {
            ids[i] = dataArr[i].id;
        }
        console.log(ids.join(","));
        $.get(url + "/collection?ids="+ids.join(","),function(){
                console.log('delete success')
        })
    });

    $("#type").change(function () {
        refresh();
    });

    $("#status").change(function () {
        refresh();
    });

    function refresh(){
        $("#table").bootstrapTable('refresh');
    }
});