<template>
<div style="background-color:#297fb8;min-height:100vh;">
<Topbar activeindex='4'></Topbar>
<div style="height:50px;"></div>
<el-row type='flex' justify='center'>
  <el-col :span='20'>
    <el-container style='background:#ffffff'>
      <el-aside>
          <el-menu
            @select="handleSelect"
            default-active="2"
            class="el-menu-vertical-demo"
            style="min-height:1000px;"
            >
            <el-submenu index="1">
              <template slot="title">
                <i class="fa fa-rocket fa-lg"></i>
                <span>机械原理</span>
              </template>
              <el-menu-item-group>
                <el-menu-item index="1-1">必要常识</el-menu-item>
              </el-menu-item-group>
              <el-menu-item-group>
                <el-menu-item index="1-2">机构组成原理及机构结构分析</el-menu-item>
              </el-menu-item-group>
              <el-menu-item-group>
                <el-menu-item index="1-3">平面机构的运动分析</el-menu-item>
              </el-menu-item-group>
              <el-menu-item-group>
                <el-menu-item index="1-4">平面连杆机构及其设计</el-menu-item>
              </el-menu-item-group>
              <el-menu-item-group>
                <el-menu-item index="1-5">齿轮机构及其设计</el-menu-item>
              </el-menu-item-group>
              <el-menu-item-group>
                <el-menu-item index="1-6">轮系及其设计</el-menu-item>
              </el-menu-item-group>
              <el-menu-item-group>
                <el-menu-item index="1-7">其他常用机构</el-menu-item>
              </el-menu-item-group>
              <el-menu-item-group>
                <el-menu-item index="1-8">平面机构的受力分析</el-menu-item>
              </el-menu-item-group>
              <el-menu-item-group>
                <el-menu-item index="1-9"> 机器的机械效率</el-menu-item>
              </el-menu-item-group>
              <el-menu-item-group>
                <el-menu-item index="1-10"> 机械的平衡</el-menu-item>
              </el-menu-item-group>
              <el-menu-item-group>
                <el-menu-item index="1-11"> 机械的运转及其速度波动的调节</el-menu-item>
              </el-menu-item-group>
              <el-menu-item-group>
                <el-menu-item index="1-12"> 机械运动方案设计</el-menu-item>
              </el-menu-item-group>
            </el-submenu>
            <el-submenu index="2">
              <template slot="title">
                <i class="fa fa-road fa-lg"></i>
                <span>大学工程制图</span>
              </template>
              <el-menu-item-group>
                <el-menu-item index="2-1">大学工程制图100点</el-menu-item>
              </el-menu-item-group>
            </el-submenu>  
      </el-menu>
      </el-aside>
      <el-main>
        <div style='height:50px;'></div>
        <div style="text-align:left;padding-top:20px;padding-left:50px;padding-right:50px;line-height:40px;">
         <span v-html="filedata"></span>
        </div>
        
        <el-pagination v-if="openbar==1"
          @current-change='changepagination'
          :current-page="currentpage" 
          background
          layout="prev, pager, next"
          :total="pagetotal"
          :page-size='5'
          >
        </el-pagination>
      </el-main>
    </el-container>
  </el-col>
</el-row>
</div>
</template>
<style scoped>
  .el-tag {
    margin:2px;
  }
  .el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 300px;
  }
  .text {
    font-size: 14px;
  }

  .item {
    margin-bottom: 18px;
  }

  .clearfix:before,
  .clearfix:after {
    display: table;
    content: "";
  }
  .clearfix:after {
    clear: both
  }
  .el-header{
    background-color: #297fb8;
    color: #333;
    text-align: center;
    line-height: 60px;
  }
</style>
<script>
 export default{
  
   data(){
     return{
       isCollapse: false,
       filedata:'',
     }
   },
   methods:{
     ToTheOtherPage(page)
     {
       this.$router.push(page);
     },
     handleSelect(key) {
        this.axios.request({
         url:'/encyclopedia/',
         headers: {'Authorization':localStorage.getItem('token')},
         method:'GET',
       }).then(data=>
       {
         data=data.data;
         for(var i=0;i<data.length;i++)
         {
           if(data[i]['title']==key)
           {
             this.filedata=data[i]['context'];
             break;
           }
         }
       }
       )
      }

   },
   mounted(){
   }
 }

</script>
