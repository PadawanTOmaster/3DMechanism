<template>
<div>
<el-row >
    <div style="top:15px;left:15px;z-index:1000;position:absolute;opacity:0.8;">
        <el-button type="success" round @click="Topage('/threed')">返回</el-button>
        <el-button @click="show2=!show2" type="success" round>看讲解</el-button>
        <el-button @click="show1=!show1" type="success" round>看图</el-button>
        &nbsp;&nbsp;&nbsp;
        <el-button type="info" circle @click="pause()" v-html="picture"></el-button>
    </div>
</el-row>
    <div id="webGL_container" style="position:absolute;z-index:0">
    </div>
    
     <el-collapse-transition>
         <div style="z-index:1000;position:absolute;right:20px;top:100px;">
        <el-container v-show="show1">
            <el-main>
                <div id="myecharts" style="width:400px;height:200px;"></div>
                <div id="myecharts1" style="width:400px;height:200px;"></div>
                <div id="myecharts2" style="width:400px;height:200px;"></div>
            </el-main>
        </el-container>
        </div>
     </el-collapse-transition>
     <el-collapse-transition>
        <el-card class="cardcss" v-show="show2" v-html="words">
        </el-card>
     </el-collapse-transition>
    <!--对话框-->
    <el-dialog
  title="请输入杆的长度"
  :visible.sync="dialogVisible"
  width="30%"
  :show-close=false
  :close-on-click-modal=false
  :close-on-press-escape=false
  >
  <span>
      <el-row>
        <el-col :span="10">
            原动件长度：
        </el-col>
        <el-col :span="14">
            <el-input
            placeholder="请输入原动件长度"
            v-model="input_left"
            clearable>
            </el-input>
        </el-col>
      </el-row>
<div style="height:10px"></div>

      <el-row>
        <el-col :span="10">
            连杆长度：
        </el-col>
        <el-col :span="14">
            <el-input
            placeholder="请输入连杆长度"
            v-model="input_middle"
            clearable>
            </el-input>
        </el-col>
      </el-row>
<div style="height:10px"></div>

      <el-row>
        <el-col :span="10">
            从动件长度：
        </el-col>
        <el-col :span="14">
            <el-input
            placeholder="请输入从动件长度"
            v-model="input_right"
            clearable>
            </el-input>
        </el-col>
      </el-row>
<div style="height:10px"></div>

      <el-row>
        <el-col :span="10">
           支架长度：
        </el-col>
        <el-col :span="14">
            <el-input
            placeholder="请输入支架长度"
            v-model="input_bottom"
            clearable>
            </el-input>
        </el-col>
      </el-row>
    
  </span>

  <span slot="footer" class="dialog-footer" >
    <el-button @click="reset()">重置</el-button>
    <el-button type="primary" @click="okay_fine()">确 定</el-button>
  </span>
</el-dialog>
</div>
</template>

<style scoped>
    .text {
            font-size: 14px;
        }
    .item {
    margin-bottom: 18px;
    }
    .cardcss {
        position:absolute;
        left:25px;
        top:100px;
        z-index:1000;
        user-select:none;
        opacity:0.4;
        height:400x;
        text-align:left;
        padding:20px;
        width:25%
    }
    .clearfix:before,
    .clearfix:after {
    display: table;
    content: "";
    }
    .clearfix:after {
    clear: both
    }
  
</style>

<script>
import * as THREE from 'three'
import {ViveController} from "three/examples/jsm/vr/ViveController.js"
import { WEBVR } from 'three/examples/jsm/vr/WebVR.js';
import dat from 'dat.gui'

export default {

    data(){
        return{
            dialogVisible:true,
            picture:'<i class="fa fa-pause"></i>',
            words:this.constwords,
            input_left:80,
            input_right:140,
            input_bottom:200,
            input_middle:200, 
            scene:null,
            camera:null,
            renderer:null,
            axis:null,
            setpath:'../../static/images/',
            format:'.jpg',
            array1:['px','nx','py','ny','pz','nz'],
            skybox:null,
            texture:[],
            mesh:null,
            geometry:null,
            material:null,
            cubeone:null,
            //设置立体图形变量
            shapeLeft:null,
            shapeRight:null,
            notmovePole:null,
            //左杠杆上面的半圆
            LeftUpCircle:null,
            LeftDownCircle:null,
            RightUpCircle:null,
            MidUpCircle:null,
            group1:null,
            group2:null,
            group3:null,
            shapemiddle:null,
            middleUpCircle:null,
            myChart:null,
            myChart1:null,
            myChart2:null,
            show1:true,
            show2:true,
            size:10,

            controls:null,//GUI界面
            extrudeSettings : {
                            bevelEnabled: false, 
                            steps: 1,
                            depth: 5, //extrusion depth, don't define an extrudePath
                            material:0, //material index of the front and back face
                            extrudeMaterial : 1 //material index of the side faces            
                        },
            Forleverage2:new THREE.MeshBasicMaterial({map:new THREE.TextureLoader().load('../../static/images/crate.gif'),side:THREE.DoubleSide}),          
            //this.angleA是左杆转的角度
            angleA:0 ,
            //angleB是右杆转的角度
            angleB:0,
            angleC:0,
            group1X:0,
            group1Z:0,
            group2X:0,
            group2Z:0,
            alist:[],
            xlist:[],
            vlist:[],
            flag:1,
            AllpoleTypeflag:[0,0,0],
            leftPole:80,
            bottomPole:140,
            MidPole:200,
            MidPole:200,
            distanceY:0,
            constwords:'<span style="color:#0047ab;">四杆机构分为：<br>1.曲柄连杆机构<br>2.双曲柄机构<br>3.双摇杆机构<br><br>机架：固定不动的构件。<br>摇杆：只能在某一角度范围内往复摆动的构件<br>曲柄：能够做整周回转的构件<br>连架杆：直接与机架链接的构件<br>连杆：不直接与机架连接的构件<br><br></span>'
            }
    },
    methods:{
        
        init()
        {            
            this.Gui();
            this.scene=new THREE.Scene();
            
            this.group1X=-this.bottomPole/2;
            this.group2X=this.bottomPole/2;
            //render set
            this.renderer=new THREE.WebGLRenderer({antialias : true});
            this.renderer.setClearColor(0xc7c7bf);
            this.renderer.setSize(window.innerWidth,window.innerHeight);

            //camera set 
            this.camera=new THREE.PerspectiveCamera( 50, window.innerWidth/window.innerHeight,0.1,10000);
            var user = new THREE.Group();
            user.add( this.camera );
            user.position.set(50,50,300)
            this.scene.add(user);
            document.getElementById("webGL_container").appendChild(this.renderer.domElement)
            this.renderer.setPixelRatio( window.devicePixelRatio );
            document.body.appendChild( WEBVR.createButton(this.renderer ) );
            this.renderer.vr.enabled = true;
            
            //fileurl 纹理图位置 '../../static/images/crate.gif'
            this.notmovePole=this.Cubiod(1,this.size,this.size,'../../static/images/crate.gif')
            this.notmovePole.position.x = 0;
            this.notmovePole.position.y = 0;
            this.notmovePole.position.z = 0
            this.scene.add(this.notmovePole);//其中 long是可以通过gui界面更改的值
            //添加一个group组合对象，封装左杆和上半圆
            this.group1=new THREE.Group();                                       
            //加左杆上半圆                                                        
            this.LeftUpCircle=this.DrawHalfCircle(1/2*this.size)
            //加左杆
            this.shapeLeft=this.drawShape(1);
            this.LeftDownCircle=this.DrawHalfCircle(1/2*this.size);
            this.LeftDownCircle.rotateZ(Math.PI);
            this.group1.add(this.LeftDownCircle);
            this.group1.add(this.LeftUpCircle)
            this.group1.add(this.shapeLeft);
            this.group1.rotateZ(-1/2*Math.PI);
            this.group1.position.set(-this.bottomPole/2,this.distanceY,1/2*this.size);
            this.scene.add(this.group1);
            // end group1
            
            //添加一个group2
            this.group2=new THREE.Group();
            //下半圆
            var rightDownCircle=this.DrawHalfCircle(1/2*this.size);
            rightDownCircle.rotateZ(Math.PI);
            this.shapeRight=this.drawShape(1);
            this.RightUpCircle=this.DrawHalfCircle(1/2*this.size);
            this.group2.add(rightDownCircle);
            this.group2.add(this.shapeRight);
            this.group2.add(this.RightUpCircle);
            this.scene.add(this.group2);
            this.group2.position.set(this.bottomPole/2,this.distanceY,1/2*this.size);
            this.group2.rotateZ(-1/2*Math.PI);
            //end group2 
            //group3
            this.group3=new THREE.Group();
            var middleDownCircle=this.DrawHalfCircle(1/2*this.size);
            middleDownCircle.rotateZ(Math.PI);
            this.shapemiddle=this.drawShape(1);
            this.middleUpCircle=this.DrawHalfCircle(1/2*this.size);
            this.group3.add(middleDownCircle);
            this.group3.add(this.shapemiddle);
            this.group3.add(this.middleUpCircle);
            this.scene.add(this.group3);
            this.group3.position.set(0,this.distanceY,0);
            this.group3.rotateZ(-1/2*Math.PI);

            while(true)
            {
                if(this.angleA>2*Math.PI)
                {
                    break;
                }
                this.angleA+=0.01;
                var PoX=this.leftPole*Math.cos(this.angleA)+this.group1X;
                var PoZ=this.leftPole*Math.sin(this.angleA)+this.group1Z;
                var distanceXZ=Math.sqrt(Math.pow(PoX-this.group2X,2)+Math.pow(PoZ-this.group2Z,2));
                var leftlong=(Math.pow(100,2)+distanceXZ*distanceXZ-Math.pow(200,2))/2/distanceXZ;
                if(100>Math.abs(leftlong))
                {
                    this.group1.rotateZ(this.angleA);
                    break;
                }
            }
            //skybox set
            for(var i=0;i<=5;i++){
                this.array1[i]=this.setpath+this.array1[i]+this.format;
            }
            //set the size of skybox
            this.skybox=new THREE.BoxBufferGeometry(5000,5000,5000);//5000 5000 5000
            for(i=0;i<=5;i++){
                this.texture[i]=new THREE.MeshBasicMaterial({map:new THREE.TextureLoader().load(this.array1[i]),side:THREE.BackSide});
            }
            this.mesh=new THREE.Mesh(this.skybox,this.texture);
            this.mesh.position.x=0;
            this.mesh.position.y=0;
            this.mesh.position.z=0;
            this.scene.add(this.mesh);
            //skybox end        
            window.addEventListener( 'resize', this.onWindowResize, false );
            this.renderer.setAnimationLoop(this.animate);     
        },
        onWindowResize() {
            this.camera.aspect = window.innerWidth / window.innerHeight;
            this.camera.updateProjectionMatrix();
            this.renderer.setSize( window.innerWidth, window.innerHeight );
        },
        Gui()
        {
            this.controls=
            {
                rightPole:this.MidPole,
                //注意，这个rotatespeed是个角度
                rotatespeed:0, 
                middlePole:this.MidPole,

            }
            var gui=new dat.GUI();
            //LongestPole为长度
            gui.add(this.controls,'rightPole',Math.abs(this.bottomPole-this.leftPole)/2,this.bottomPole+this.leftPole).name("从动件长度");
            gui.add(this.controls,'middlePole',Math.abs(this.bottomPole-this.leftPole)/2,this.bottomPole+this.leftPole).name("连杆长度");
            gui.add(this.controls,'rotatespeed',-0.5,0.5).name("转速");

        },
        
        animate() 
        {   
            this.angleA+=this.controls.rotatespeed*this.flag;
            
            if(this.angleA>2*Math.PI)
            {
                this.angleA-=2*Math.PI;
            }
            else if(this.angleA<0)
            {
                this.angleA+=2*Math.PI;
            }  
            //PoX PoZ是左杆旋转点坐标
            
            var PoX=this.leftPole*Math.cos(this.angleA)+this.group1X;
            var PoZ=this.leftPole*Math.sin(this.angleA)+this.group1Z;
            var distanceXZ=Math.sqrt(Math.pow(PoX-this.group2X,2)+Math.pow(PoZ-this.group2Z,2));
            var leftlong=(Math.pow(this.controls.middlePole,2)+distanceXZ*distanceXZ-Math.pow(this.controls.rightPole,2))/2/distanceXZ;
            if(this.controls.middlePole<Math.abs(leftlong))
            {
                this.angleA-=this.controls.rotatespeed*this.flag;
                this.flag=-this.flag;
                
                
                return;
            }
           //右面圆
           //两个圆心连线与两个圆交点连线的中点坐标
            var bufx=(-this.group2X+PoX)*(distanceXZ-leftlong)/distanceXZ+this.group2X;
            var bufz=(-this.group2Z+PoZ)*(distanceXZ-leftlong)/distanceXZ+this.group2Z;
            var bufUPdistance=Math.sqrt(Math.pow(this.controls.middlePole,2)-leftlong*leftlong);
            var vx=-(this.group2Z-PoZ)/distanceXZ;
            var vz=(this.group2X-PoX)/distanceXZ;
            var finalX1=bufx+vx*bufUPdistance;
            var finalX2=bufx-vx*bufUPdistance;
            var finalZ1=bufz+vz*bufUPdistance;
            var finalZ2=bufz-vz*bufUPdistance;
            
            var angleBB;
            angleBB=Math.PI-Math.acos((this.group2X-finalX1)/this.controls.rightPole);
            if(finalZ1<0)
            {
                angleBB=Math.PI+Math.acos((this.group2X-finalX1)/this.controls.rightPole);
            }
            
            var dx=finalX1-PoX;
            var angleCC=Math.PI-Math.acos(-dx/this.controls.middlePole);
            if(finalZ1<PoZ){
                angleCC=Math.PI+Math.acos(-dx/this.controls.middlePole);;
            }
            this.group3.rotateZ(angleCC-this.angleC);
            this.angleC=angleCC;
            //angleB算出来的是旋转角度
            this.xlist.push(angleBB);
            if(this.xlist.length>100)
            {
                this.xlist.splice(0, 1);
            }
            if(this.xlist.length>=2){
                this.vlist.push(angleBB-this.xlist[this.xlist.length-2]);
                if(this.vlist.length>100)
                {
                    this.vlist.splice(0, 1);
                }
            }

            if(this.vlist.length>=2){
                this.alist.push(this.vlist[this.vlist.length-1]-this.vlist[this.vlist.length-2]);
                if(this.alist.length>100)
                {
                    this.alist.splice(0, 1);
                }
            }
            this.myChart.setOption(this.setEcharts(this.xlist,'#dd0d29','从动件角位移'));
            this.myChart1.setOption(this.setEcharts(this.vlist,'#0e4bef','从动件角速度'));
            this.myChart2.setOption(this.setEcharts(this.alist,'#0b9909','从动件角加速度'));
            this.notmovePole.scale.x=this.bottomPole+this.size;
            this.shapeLeft.scale.y=this.leftPole;
            //给左杆上方半圆一个合适的位置,使这个组进行旋转
            this.LeftUpCircle.position.y=this.leftPole;
            this.group1.rotateZ(this.controls.rotatespeed*this.flag);
            this.group1.position.x=-1/2*this.bottomPole;
            //group2
            this.shapeRight.scale.y=this.controls.rightPole;
            this.RightUpCircle.position.y=this.controls.rightPole;
            this.group2.rotateZ(angleBB-this.angleB);
            this.angleB=angleBB;
            
            this.group3.position.set(PoX,PoZ,10);
            this.middleUpCircle.position.y=this.controls.middlePole;
            this.shapemiddle.scale.y=this.controls.middlePole;
            this.group2.position.x=1/2*this.bottomPole;
            /***********************************
             * 曲柄存在的条件
             ***********************************/
            if(this.SatisfyTwoConditions()==1 && this.AllpoleTypeflag[0]==0)//数组第0位代表双曲柄状态 值为1的话是双曲柄状态 为0则不是双曲柄状态
            {
                this.AllpoleTypeflag[2]=0;
                this.AllpoleTypeflag[1]=0;//把其他两类归0
                this.AllpoleTypeflag[0]=1;
                this.$message({
                    message: '现在是 双曲柄机构',
                    type: 'success'
                });
                var words='<b><h1>双曲柄机构</h1><span style="font-family:华文仿宋">在铰链四杆机构中，若两连架杆均为曲柄，此四连杆机构称为双曲柄机构<br>即两根杆都可以做整周转动。<br>它需要满足以下两个条件：<br>1. 最长杆长度+最短杆长度 <=其他两杆长度之和。<br>2.支架最短。<br>它的主要应用有：<br>天平机构、火车车轮机构、车坐斗机构、双曲柄插床、装载机铲斗升降机机构。<br><br></span></b>'
                this.words=words+this.constwords;
            }
            else if(this.SatisfyTwoConditions()==2 && this.AllpoleTypeflag[1]==0)//数组第1位：曲柄摇杆机构 值为1代表当前为曲柄摇杆 0就不用说了
            {
                this.AllpoleTypeflag[2]=0;
                this.AllpoleTypeflag[0]=0;//把其他两类归0
                this.AllpoleTypeflag[1]=1;
                this.$message({
                    message: '现在是 曲柄摇杆机构',
                    type: 'success'
                });
                var words='<b><h1>曲柄摇杆机构</h1><span style="font-family:华文仿宋">曲柄摇杆机构是指具有一个曲柄和一个摇杆的铰链四杆机构。<br>即其中有一根杆可以做整周转动。<br>它需要满足以下两个条件：<br>1. 最长杆长度+最短杆长度 <=其他两杆长度之和。<br>2.连杆（连接支架的两杆）的其中之一最短。<br>它的主要应用有：<br>牛头刨床进给机构、雷达调整机构、缝纫机脚踏机构、复摆式腭式破碎机、钢材输送机等<br><br></span></b>'
                this.words=words+this.constwords;
            }
            else if(this.SatisfyTwoConditions()==0 && this.AllpoleTypeflag[2]==0)//数组第2位：双摇杆机构
            {
                this.AllpoleTypeflag[1]=0;
                this.AllpoleTypeflag[0]=0;//把其他两类归0
                this.AllpoleTypeflag[2]=1;
                this.$message({
                    message: '现在是 双摇杆机构',
                    type: 'success'
                });
                var words='<b><h1>双摇杆机构</h1><span style="font-family:华文仿宋">双摇杆机构就是两连架杆均是摇杆的铰链四杆机构<br>双摇杆机构的两连架杆都不能作整周转动。<br>它的判别条件是：<br>最长杆长度+最短杆长度 >其他两杆长度之和 或 最长杆长度+最短杆长度 ≤ 其他两杆长度之和但连杆（机架的对杆）为最短杆。<br>双摇杆机构在机械中的应用也很广泛，如手动冲孔机。<br><br></span></b>'
                this.words=words+this.constwords;
            }
            //end grop2
            //天空盒
            this.mesh.rotation.y+=0.0003;
            //渲染
            this.renderer.render( this.scene, this.camera );
           
        },
        SatisfyTwoConditions()//是它下面两个函数的整合
        {
            if(this.PolemaxplusPoleminSmallThanOther(this.controls.middlePole,this.controls.rightPole,this.bottomPole,this.leftPole) && this.checkPoleType(this.controls.middlePole,this.controls.rightPole,this.bottomPole,this.leftPole))
            {
                if(this.checkPoleType(this.controls.middlePole,this.controls.rightPole,this.bottomPole,this.leftPole)==1)
                return 1;//双曲柄
                else if(this.checkPoleType(this.controls.middlePole,this.controls.rightPole,this.bottomPole,this.leftPole)==2)
                return 2;//曲柄摇杆
            }
            else return 0;//双摇杆
        }, 
        checkPoleType(mp,rp,bp,lp)
        {
            //看支架最短还是左杆最短？
            //var AllPole=[];
            var minPole=Math.min(mp,rp,bp,lp);
            if(minPole==bp)return 1;//双曲柄机构
            else if(minPole==lp)return 2;//曲柄摇杆机构
            else return 0;
        },
        PolemaxplusPoleminSmallThanOther(mp,rp,bp,lp)
        {
            var AllPole=[mp,rp,bp,lp];
            var sumfourPole=eval(AllPole.join('+'));//四杆长度求和
            var maxPole=Math.max(mp,rp,bp,lp);
            var minPole=Math.min(mp,rp,bp,lp);
            if(maxPole+minPole<=sumfourPole-(maxPole+minPole))
            return 1;
            else return 0;
        },
        pause()
        {
            if(this.controls.rotatespeed==0)
            {
                this.picture='<i class="fa fa-pause"></i>'
                this.controls.rotatespeed=0.1;
            }
            else 
            {
                this.picture='<i class="fa fa-play"></i>'
                this.controls.rotatespeed=0;
            }
        },
        //long 长度
        //wide 宽度
        //high 高
        //fileurl 纹理图位置 '../../static/images/crate.gif'
        //不转的杆
        Cubiod(long,wide,high,fileurl)
        {
            var geometry= new THREE.BoxGeometry(long,wide,high);
            var material=new THREE.MeshBasicMaterial({map:new THREE.TextureLoader().load(fileurl),side:THREE.DoubleSide});
            var cubeone=new THREE.Mesh(geometry,material);
            return cubeone;
        },
        
        //distance 两个圆心距离 设成1是为了下面gui界面调杆长是倍数增长。
        drawShape(distance)
        {
            var shape1=new THREE.Shape();
            var x1=1/2*this.size,y1=0;
            shape1.moveTo(x1,y1);
            shape1.lineTo(x1,y1+distance);
            shape1.lineTo(-x1,y1+distance);
            shape1.lineTo(-x1,y1);
            shape1.lineTo(x1,y1);
            var shape11=new THREE.ExtrudeGeometry(shape1,this.extrudeSettings);
            var shapeplus1=new THREE.Mesh(shape11,this.Forleverage2);
            return shapeplus1;
        },
        DrawHalfCircle(r)
        {
            var points1=[];
            var i=0;
            var shape1=new THREE.Shape();
            while(i<=Math.PI)
            {
                points1.push(new THREE.Vector2(r*Math.cos(i),r*Math.sin(i)));
                i+=0.1;
            }
            shape1.setFromPoints(points1);
            shape1.lineTo(r,0);
            var shape11=new THREE.ExtrudeGeometry(shape1,this.extrudeSettings);
            var shapeplus1=new THREE.Mesh(shape11,this.Forleverage2);
            return shapeplus1;
        },
        setEcharts(buffList,linecolor,text)
        {
            var option = {
                title: {
                    text: text
                },
                xAxis: {
                    type: 'category',
                    data: []
                },
                yAxis: {
                    type: 'value'
                },
                color:[linecolor],
                series: [
                    {
                        data: buffList,
                        type: 'line',
                        smooth: false,
                    },
                    ]
            };
            return option;
        },
        distance(x1,y1,x2,y2){
            return Math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2));
        },
        Topage(path)
        {
            this.$router.push(path);
        },
        
        checkPoleLong()
        {
            var fflag=1;
            if(this.input_left=='' || this.input_right=='' || this.input_bottom=='' || this.input_middle=='')
            {
                fflag=2;
                return fflag;
            }
            this.input_right=parseInt(this.input_right);
            this.input_left=parseInt(this.input_left);
            this.input_bottom=parseInt(this.input_bottom);
            this.input_middle=parseInt(this.input_middle);
            var sumFourPole=this.input_right+this.input_left+this.input_bottom+this.input_middle;
            if(sumFourPole-this.input_right<=this.input_right || sumFourPole-this.input_left<=this.input_left 
            || sumFourPole-this.input_bottom<=this.input_bottom || sumFourPole-this.input_middle<=this.input_middle)fflag=0;
            return fflag;
        },
        okay_fine()
        {
            if(this.checkPoleLong()==1)
            {
                this.leftPole=this.input_left;
                this.bottomPole=this.input_bottom;
                this.MidPole=this.input_middle;
                this.MidPole=this.input_right;
                this.dialogVisible=false;
                this.init();
            }
            else if(this.checkPoleLong()==2)
            {
                this.$message('不能不填哦');
            }  
            else if(this.checkPoleLong()==0)
            {
                this.$message('一杆不能超出其余三杆之和');
            }
        },
        reset()
        {
            this.input_left=80;
            this.input_middle=200;
            this.input_bottom=200;
            this.input_right=140;
        }
        },
        mounted(){
            this.myChart=this.$echarts.init(document.getElementById('myecharts'));
            this.myChart1=this.$echarts.init(document.getElementById('myecharts1'));
            this.myChart2=this.$echarts.init(document.getElementById('myecharts2'));
        },
        destroyed()
        {
            var classname='dg main a'
            var targetElem=document.getElementsByClassName(classname);
            while(targetElem.length>0)
            {
                document.getElementsByClassName('dg ac')[0].removeChild(targetElem[0]);
            }
        }
}

</script>
