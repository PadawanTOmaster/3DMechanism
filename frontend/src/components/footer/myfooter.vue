<template>
<el-menu
  class="el-menu-demo"
  mode="horizontal"
  background-color="#409EFF"
  text-color="#000"
  active-text-color="#fff"
  :default-active="activeindex"
  @select="changeselect"
  >
  	<el-menu-item index="1">主页</el-menu-item>
	  <el-menu-item index="2">3D机械机构</el-menu-item>
		<el-menu-item index="3">资源下载</el-menu-item>
  	<el-menu-item index="4">机械小课堂</el-menu-item>
  	<el-menu-item index="5">刷题平台</el-menu-item>
  	<el-menu-item index="6">机动新闻</el-menu-item>
		<el-menu-item v-if="isManager()" index='8' >后台管理</el-menu-item>
		<el-menu-item index="7">其他功能</el-menu-item>
		<el-submenu index="9" style="float:right">
    	<template slot="title"><i class="fa fa-address-card fa-lg"></i>&emsp;{{nickname}}</template>
    	<el-menu-item index="9-1">退出登录</el-menu-item>
    </el-submenu>

</el-menu>
</template>

<script>
export default {
	data(){
     return{
       nickname:'',
     }
    },
	props:['activeindex'],
	methods:{
		changeselect(index)
		{
			switch (index) {
				case '1':
					this.changepage('/homepage');
					break;
				case '2':
					this.changepage('/threed');
					break;
				case '3':
					this.changepage('/download');
					break;
				case '4':
					this.changepage('/encyclopedia');
					break;	
				case '5':
					this.changepage('/practice');
					break;
				case '6':
					this.changepage('/news');
					break;
				case '7':
					this.changepage('/other');
					break;
				case '8':
					this.changepage('/manage');
					break;
				case '9-1':
					localStorage.clear();
					this.changepage('/login');
				  break;
				default:
					break;
			}
		},

		isManager()
		{
			if(localStorage.getItem('flag')==0 || localStorage.getItem('flag')==1)
			{
				return 1;
			}
			return 0; 
		},
		changepage(path)
		{
			this.$router.push(path)
		}
	},
	mounted()
	{
		this.nickname=localStorage.getItem('nickname');
	}
}

</script>

<style>
</style>
