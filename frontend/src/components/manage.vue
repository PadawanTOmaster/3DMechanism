<template>
<div style="height:100vh;">
<!--从这里开始复制导航栏-->
<Topbar activeindex='8'></Topbar>
<div style="height:80px;"></div>
<el-row type="flex" justify="center">
  <el-col :span="15">
			<el-collapse @change="handleChange">
  <el-collapse-item title="资源下载" name="1">
    <el-row>
      <el-col :span="12">
        <el-card>
          <div slot="header" class="clearfix">
            <span>已有文件</span>
          </div>
          <div class="text item" v-for="i in filelist" :key="i['id']">
            <el-row>
              <el-col :span="12">
                {{i['filename']}}
              </el-col>
              <el-col :span="12">
                <el-button size='small' type="info" @click="deletefile(i['id'])">删除</el-button>
                <div style="height:5px;"></div>
              </el-col>
            </el-row>
            
          </div>
        </el-card>
      </el-col>
      <el-col :span='12'>
        <el-card>
           <div slot="header" class="clearfix">
            <span>新增文件</span>
          </div>
          <div class="text item" style="text-align:left;">
            <span style="font-size: 14px;color:#c43420;font-weight:bold">1.上传文件(filepath)</span>
            <el-upload
              class="upload-file"
              drag
              action=""
              :http-request="beforeUploadfile"
              :limit="1"
              :on-exceed="handleExceed"
              ref="uploader"
              >
              <el-button size="small" type="primary">点击上传</el-button>
              <i class="el-icon-upload"></i>
              <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
            </el-upload>
          </div>
          <div class="text item" style="text-align:left;">
            <span style="font-size: 14px;color:#c43420;font-weight:bold">2.上传文件对应图片(imgpath)</span>
            <el-upload
              class="avatar-uploader"
              action=""
              :show-file-list="false"
              :before-upload="beforeUploadimg"
              >
              <img v-if="imageUrl" :src="imageUrl" class="imgclass">
              <i v-else class="el-icon-plus avatar-uploader-icon"></i>
            </el-upload>
          </div>
          <div class="text item" style="text-align:left;">
            <span style="font-size: 14px;color:#c43420;font-weight:bold">3.文件名,将会显示在下载页面文件图片下(filename)</span>
            <el-input v-model="filename" placeholder="请输入文件名"></el-input>
            <div style="height:30px;"></div>
          </div>
          <div class="text item" style="text-align:left;">
            <span style="font-size: 14px;color:#c43420;font-weight:bold">4.文件描述(description)</span>
            <el-input 
            v-model="description" 
            type="textarea"
            :rows="2"
            placeholder="请输入文件描述">
            </el-input>
            <div style="height:10px;"></div>
          </div>
          <div style="text-align:right;">
            <el-button type="primary" size="medium" @click="postnewfile">提交</el-button>
          </div>
          
        </el-card>
      </el-col>
    </el-row>
  </el-collapse-item>
  <el-collapse-item title="学生管理" name="2">
    <el-row>
      
        <el-table :data="tableData"
        style="width:80%">
          <el-table-column
          label="现有班级"
          prop="class"
          >
          </el-table-column>
          <el-table-column
          >
          <template slot="header" slot-scope="scope">
            <el-button>新增班级</el-button>
          </template>
          <template slot-scope="scope">
            <el-button type="danger">删除</el-button>
            <el-button type="warning">查看班级信息</el-button>
          </template>
          </el-table-column>
        </el-table>
      
    </el-row>
    
   
  </el-collapse-item>
  <el-collapse-item title="机械小课堂" name="3">
    <div>简化流程：设计简洁直观的操作流程；</div>
    <div>清晰明确：语言表达清晰且表意明确，让用户快速理解进而作出决策；</div>
    <div>帮助用户识别：界面简单直白，让用户快速识别而非回忆，减少用户记忆负担。</div>
  </el-collapse-item>
  <el-collapse-item title="刷题平台" name="4">
    <div>用户决策：根据场景可给予用户操作建议或安全提示，但不能代替用户进行决策；</div>
    <div>结果可控：用户可以自由的进行操作，包括撤销、回退和终止当前操作等。</div>
  </el-collapse-item>
</el-collapse>
  </el-col>
</el-row>

</div>
</template>
<script>
var postdata=new FormData();
export default {
    data(){
        return{
          imageUrl:'',
          description:'',
          filename:'',
          filelist:[],
        }
    },
    methods:{
      beforeUploadfile(param)
      {
        postdata.append('filepath',param.file);
      },

      beforeUploadimg(img)
      {
        const isJPG = img.type === 'image/jpeg';
        const isLt2M = img.size / 1024 / 1024 < 2;
        if (!isLt2M) {
          this.$message.error('上传头像图片大小不能超过 2MB!');
          return;
        }
        if (!isJPG) {
          this.$message.error('上传头像图片只能是 JPG 格式!');
          return;
        }
        this.imageUrl=URL.createObjectURL(img);
        postdata.append('imgpath',img)
      },

      deletefile(id)
      {
        this.$confirm('此操作将永久删除该文件, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(()=>
        {
          this.axios.request(
          {
            url:'/filedownload/',
            method:'DELETE',
            data:{
              'id':id,
            },
            headers:{
              'Authorization':localStorage.getItem('token'),
            }
          }
          ).then(
          data=>
          {
            data=data.data;
            this.$message({message:data['alert']});
          }
         ).then(()=>
           {
             this.getdownloadfiles();
           }
         )
        })
        
      },
      refreshnews()
      {
        this.axios.request(
          {
            url:'/news/',
            method:'POST',
            headers:{
              'Authorization':localStorage.getItem('token'),
            },
            data:{
              'event':'refresh'
            }
          }
        ).then(
          data=>
          {
            data=data.data;
            this.$message({message:data['alert'],type:'success'});
          }
        )
      },

      handleChange(activearray)
      {
        for(var i=0;i<activearray.length;i++)
        {
          if(activearray[i]==1)
          {
            this.getdownloadfiles();
          }
        }
      },
      getdownloadfiles()
      {
        this.axios.request(
              {
                url:'/filedownload/',
                method:'GET',
                headers:{
               'Authorization':localStorage.getItem('token'),
						   },
              }
            ).then(data=>
            {
              data=data.data;
              this.filelist=data;

            })
      },

      handleExceed(files, fileList) {
        this.$message.warning("只能上传一个文件哦，多个文件上传请放入压缩包");
      },
      postnewfile()
      {
        postdata.append('filename',this.filename);
        postdata.append('description',this.description);
        if(postdata.get('filename')=='' || postdata.get('description')=='' ||
         postdata.get('filepath')==null || postdata.get('imgpath')==null)
         {
           console.log(postdata.get('filepath'))
           this.$message({message:'此表单任何位置不能为空',type:"error"});
         }
        else
        {
          this.axios.request(
            {
              url:'/filedownload/',
              method:'POST',
              headers:{
              'Content-Type': 'multipart/form-data',
              'Authorization':localStorage.getItem('token'),
						  },
              data:postdata
            }
          ).then(data=>
          {
            data=data.data;
            this.$message({message:'提交成功',type:"success"});
            postdata=new FormData();
            this.filename='';
            this.description='';
            this.imageUrl='';
            this.$refs.uploader.clearFiles();
            this.getdownloadfiles();
          }
          ).catch(error=>
         {
           this.$message({message:'服务器繁忙，稍后再试吧'});
         })
        }
      }
        
    },
    
}

</script>

<style scoped>
.imgclass {
    width: 178px;
    height: 178px;
    display: block;
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
    width: 178px;
    height: 178px;
    line-height: 178px;
    text-align: center;
  }
</style>
