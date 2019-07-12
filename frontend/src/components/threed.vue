<template>
<div style="background-color:#297fb8;min-height:100vh;">
<Topbar activeindex='2'></Topbar>
<div style="height:50px;"></div>
<el-row type='flex' justify='center'>
  <el-col :span='20'>
    <el-container>
      <div style="text-align:left">
        <span style="color:#fff">机构运动模型</span><br>
        <img src='../../static/images/line.png' style="width:150px;"/>

        <el-row :gutter="20">
          <el-col :span='8'>
            <el-card>
              <div slot="header" class="clearfix">
                <el-button style="float: right; padding: 3px 0" type="success" @click="Topage('/fourbar')">四杆机构</el-button>
              </div>
              <router-link to="/fourbar"><img src="../../static/images/fourbar.png" class="image"/></router-link>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card>
              <div slot="header" class="clearfix">
                <el-button style="float: right; padding: 3px 0" type="warning" @click="Topage('/forcebar')">杆件受力分析</el-button>
              </div>
              <router-link to="/forcebar"><img src="../../static/images/barforce.png" class="image"/></router-link>
            </el-card>
          </el-col>
          <el-col :span='8'>
            <el-card>
              <div slot="header" class="clearfix">
                <el-button style="float: right; padding: 3px 0" type="danger" @click="Topage('/gear')">差动轮系机构</el-button>
              </div>
              <router-link to="/gear"><img src="../../static/images/gear.png" class="image"/></router-link>
            </el-card>
          </el-col>
        </el-row>
        <div style="height:20px;"></div>
        <el-row :gutter="20">
          <el-col :span='8'>
            <el-card>
              <div slot="header" class="clearfix">
                <el-button style="float: right; padding: 3px 0" type="success" @click="Topage('/slidercrank')">曲柄滑块机构</el-button>
              </div>
              <router-link to="/slidercrank"><img src="../../static/images/slidercrank.png" class="image"/></router-link>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card>
              <div slot="header" class="clearfix">
                <el-button style="float: right; padding: 3px 0" type="warning" @click="Topage('/crankrocker')">曲柄摇块机构</el-button>
              </div>
              <router-link to="/crankrocker"><img src="../../static/images/crankrocker.png" class="image"/></router-link>
            </el-card>
          </el-col>
          <el-col :span='8'>
            <el-card>
              <div slot="header" class="clearfix">
                <el-button style="float: right; padding: 3px 0" type="danger" @click="Topage('/crankguide')">摆动导杆机构</el-button>
              </div>
              <router-link to="/crankguide"><img src="../../static/images/crankguide.png" class="image"/></router-link>
            </el-card>
          </el-col>
        </el-row>
        <div style="height:20px;"></div>
        <span style="color:#fff">大物实验</span><br>
        <img src='../../static/images/line.png' style="width:150px;"/>
        <el-row :gutter="20">
          <el-col :span='8'>
            <el-card>
              <div slot="header" class="clearfix">
                <el-button style="float: right; padding: 3px 0" type="danger" @click="Topage('/forceoscillation')">波尔共振仪</el-button>
              </div>
              <router-link to="/forceoscillation"><img src="../../static/images/dwsy.png" class="image"/></router-link>
            </el-card>
          </el-col>

          <el-col :span='8'>
            <el-card>
              <div slot="header" class="clearfix">
                <el-button style="float: right; padding: 3px 0" type="danger" @click="Topage('/spectrometer')">分光计</el-button>
              </div>
              <router-link to="/forceoscillation"><img src="../../static/images/dwsy.png" class="image"/></router-link>
            </el-card>
          </el-col>

        </el-row>
      </div>
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
  .box-card {
    width: 350px;
  }
  .bottom {
    margin-top: 13px;
    line-height: 12px;
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
  .image {
    width: 100%;
    display: block;
  }
  #footer{color:#555b5e;border-top:1px solid #871515; padding:10px 0 80px 0; width:100%}
  footer{ background:#555b5e;border-top:1px solid #000; padding:10px 0 80px 0; width:100%}
  .color-F00{ color:#F00}
</style>
<script>
 export default{
  
   data(){
     return{
       
     }
   },
   methods:{
     Topage(path)
        {
            this.$router.push(path);
        },
     

   },
   mounted(){
    
   }
 }

</script>
