<template>
<div style="background-color:#297fb8;height:100vh;"  @keyup.enter="signup()">
<el-row class="longlogo">
    <img src="../../static/images/longlogo.png" style="width:40%"/>
</el-row>
<el-row type="flex" justify="center">
  <el-col :span="5"><img src="../../static/images/gear1.png" class="gearimg"/></el-col>
  <el-col :span="10">
        <el-form label-width="80px" class="demo-ruleForm">
            <el-col :span="21">
              <el-form-item style="text-align:left"> 
                <el-row>
                  <el-col :span="8">
                    <el-upload
                  class="avatar-uploader"
                  action=""
                  :show-file-list="false"
                  :before-upload="beforeAvatarUpload">
                  <img v-if="imageUrl" :src="imageUrl" class="avatar">
                  <i v-else class="el-icon-plus avatar-uploader-icon"></i>
                  </el-upload>
                  </el-col>
                  <el-col :span='16'>
                     <el-input
                      type="textarea"
                      rows="4"
                      placeholder="这个人有点懒，什么都没有留下~"
                      v-model="information">
                    </el-input>
                  </el-col>
                </el-row>
                
                
              </el-form-item>
              <el-form-item>
                <el-input v-model="username" placeholder="用户名" @focus="usernameRule=''"></el-input>
                <div class="textlabel" v-html="usernameRule"></div>
              </el-form-item>
              
              <el-form-item>
                <el-input v-model="nickname" placeholder="昵称" @focus="nicknameRule=''"></el-input>
                <div class="textlabel" v-html="nicknameRule"></div>
              </el-form-item>

              <el-form-item>
                <el-input v-model="password1" :type="type1" placeholder="密码" @focus="password1Rule=''">
                  <el-button slot="append" icon="el-icon-view" @click="changeEyesight(0)"></el-button>
                </el-input>
                
                <div class="textlabel" v-html="password1Rule"></div>
              </el-form-item>

              <el-form-item>
                <el-input v-model="password2" :type="type2" placeholder="确认密码" @focus="password2Rule=''">
                  <el-button slot="append" icon="el-icon-view" @click="changeEyesight(1)"></el-button>
                </el-input>
                <div class="textlabel" v-html="password2Rule"></div>
              </el-form-item>

              <el-form-item>
                <el-input v-model="email" placeholder="邮箱" @focus="emailRule=''"></el-input>
                <div class="textlabel" v-html="emailRule"></div>
              </el-form-item>
              <el-form-item style="text-align:right">
                <el-button type='success' @click="signup()" >&nbsp;注册&nbsp;</el-button> 
                <el-button type='warning' @click="changepage('/login')">登录</el-button>
              </el-form-item>
            </el-col>
        </el-form>
  </el-col>
<el-col :span="5"><div style="height:100px;"></div><img src='../../static/images/gear2.png' class="gearimg"/></el-col>
</el-row>

</div>
</template>
<style scoped>
  .gearimg{
    width:200px;
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
  .avatar-uploader .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }
  .avatar-uploader .el-upload:hover {
    border-color: #409EFF;
  }
  .avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 100px;
    height: 100px;
    line-height: 100px;
    text-align: center;
  }
  .avatar {
    width: 100px;
    height: 100px;
    display: block;
  }
  .textlabel{
    height:10px;
    text-align:left;
  }
  .longlogo {
    text-align: left;
    padding-left:10%;
    padding-top:1%;
    padding-bottom: 1%
  }
</style>
<script>
var postdata = new FormData();
 export default{
   data(){
     return{
       information:'',
       username:"",
       nickname:'',
       password1:"",
       password2:"",
       email:"",
       usernameRule:'',
       nicknameRule:'',
       password1Rule:'',
       password2Rule:'',
       emailRule:'',
       imageUrl:'../../static/images/originavatar.jpg',
       type1:'password',
       type2:'password',
       file:''
     }
   },
   methods:{
     changepage(page)
     {
       this.$router.push(page);
     },
     signup()
     {
       var Rex=/\s/;
       var Rex1=/[^\sA-Za-z0-9_.@]/
       var flag=1;
       if(this.username=='')
       {
         flag=0;
         this.usernameRule='用户名<span style="color:#c43420">不能为空</span>';
       }
       else if(Rex1.test(this.username))
       {
         flag=0;
         this.usernameRule='用户名中含有<span style="color:#c43420">非法字符,只能含有字母数字下划线及邮箱中常用符号("@"".")</span>，换一个吧';
       }
       if(this.nickname=='')
       {
         flag=0;
         this.nicknameRule='昵称<span style="color:#c43420">不能为空</span>'
       }
       else if(Rex.test(this.nickname))
       {
         flag=0;
         this.nicknameRule='昵称中含有<span style="color:#c43420">非法字符(不能含有空格)</span>，换一个吧'
       }
       if(this.password1=='')
       {
         flag=0;
         this.password1Rule='密码<span style="color:#c43420">不能为空</span>';
       }
       else if(this.password1.length<6)
       {
         flag=0;
         this.password1Rule='密码长度<span style="color:#c43420">不能少于6位</span>';
       }
       if(this.password2=='')
       {
         flag=0;
         this.password2Rule='<span style="color:#c43420">请确认密码</span>';
       }
       else if(this.password2!=this.password1)
       {
         flag=0;
         this.password2Rule='确认密码与上述密码<span style="color:#c43420">不符</span>';
       }
       var Rex=new RegExp(/^([a-zA-Z0-9._-])+@([a-zA-Z0-9_-])+(\.[a-zA-Z0-9_-])+/);
       if( this.email!='' && !Rex.test(this.email))
       {
         flag=0;
         this.emailRule='<span style="color:#c43420">邮箱格式有误</span>';
       }
       if(flag)
       {
         postdata.append('username',this.username);
         postdata.append('nickname',this.nickname);
         postdata.append('password',this.password1);
         postdata.append('email',this.email);
         postdata.append('information',this.information)

         this.axios.request(
           {
             url:'/signup/',
             method:'POST',
             headers:{
							'Content-Type': 'multipart/form-data'
						 },
             data:postdata
           }
         ).then(response=>
         {
            postdata = new FormData();
            var data = response.data;
            this.$message({message:data.alert,type:'success'});
            if(data.check==1)
            {
              this.$router.push('/login');
            }
         }
         ).catch(error=>
         {
          
           if(error.message='Network Error')
           {
             this.$message({message:'服务器繁忙，稍后再试吧',type:'error'});
           }
           //别忘了以后修改一下这里！！！！
            else
            {
              this.$message({message:'服务器繁忙，稍后再试吧'});
            }
         })
       }
     },

      changeEyesight(num)
      {
        if(num)
        {
          if(this.type2=='text')this.type2='password';
          else this.type2='text';
        }
        else
        {
          if(this.type1=='text')this.type1='password';
          else this.type1='text';
        }
        
        
      },

      beforeAvatarUpload(file) {
        const isJPG = file.type === 'image/jpeg';
        const isLt2M = file.size / 1024 / 1024 < 2;
        if (!isLt2M) {
          this.$message.error('上传头像图片大小不能超过 2MB!');
          return;
        }
        if (!isJPG) {
          this.$message.error('上传头像图片只能是 JPG 格式!');
          return;
        }
        this.imageUrl=URL.createObjectURL(file);
        postdata.append('avatar',file);
      }
   },
   mounted()
   {
     if(localStorage.getItem('token')!=undefined)
          {
            this.$router.push('/homepage');
          }
   }
 }
</script>
