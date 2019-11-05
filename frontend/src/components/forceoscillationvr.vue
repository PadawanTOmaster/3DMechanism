<template>
<div>
    <el-row >
        <div style="top:15px;left:15px;z-index:1000;position:absolute;opacity:0.8;">
            <el-button type="success" round @click="toPage('/threed')">返回</el-button>
            <!-- <el-button @click="show1=!show1" type="success" round>看图</el-button>
            <el-button @click="show2=!show2" type="success" round>看讲解</el-button> -->
        </div>
    </el-row>
    <div id="webGL_container" style="position:absolute;z-index:0">
    </div>
    <div :style= "styleObject">
        <div class="block">
            <el-tooltip class="item" effect="dark" content="确定" placement="bottom">
                <el-button type="success" circle :disabled="button1type" @click="play"><i class="fa fa-check"></i></el-button>                
            </el-tooltip>
            <el-tooltip class="item" effect="dark" :content="button2text" placement="bottom">
                <el-button type="warning" circle :disabled="button2type" @click="pause"><i :class="button2"></i></el-button>              
            </el-tooltip>
            <el-tooltip class="item" effect="dark" content="重置" placement="bottom">
                <el-button type="danger" circle @click="stop"><i class="fa fa-refresh"></i></el-button>              
            </el-tooltip>
        </div>
    </div>
    <el-card
    v-show='showtable'
    :body-style="{ padding: '5px' }"
    class="container"
    >
        <div slot="header" class="clearfix">
            <el-button style="float: right; padding: 3px 0;" type="text" @click="closeTable()"><i class = 'fa fa-close'></i></el-button>
        </div>
        <el-row>
            <el-col :span="12">
                <div style="font-family:PingFang SC;float: left;color:grey;" >
                    周期×10:
                </div>
            </el-col>
            <el-col :span="12">
                <div  style="font-family:PingFang SC;float: left;color:grey;">
                    {{T10}} 
                </div>
            </el-col>
        </el-row>
        <br>
        <el-table
        stripe
        :data="tableData"
        height = 250px
        border
        >
        <el-table-column
        prop="id"
        label="序号"
        >
        </el-table-column>
        <el-table-column
        prop="A"
        label="振幅(°)"
        >
        </el-table-column>
    </el-table> 
    </el-card>
    <div style="z-index:1000;position:absolute;left:20px;top:100px;" v-show="showGraphs">
        <el-container>
            <el-main>
                <div id="echarts1" style="width:450px;height:300px;"></div>
            </el-main>
        </el-container>
    </div>
    
</div>
</template>

<style scoped>
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
  .container {
        position:absolute;
        z-index: 1000;
        left:25px;
        top:100px;
        width:30%;
        
    }
    .block {
        text-align:right;
    }
    .bottom {
      clear: both;
      text-align: center;
    }
    .item {
      margin: 4px;
      
    }
 
</style>

<script>
import * as THREE from 'three'
import dat from 'dat.gui'
import {ViveController} from "three/examples/jsm/vr/ViveController.js"
import { WEBVR } from 'three/examples/jsm/vr/WebVR.js';
import {MTLLoader, OBJLoader} from 'three-obj-mtl-loader'
import GLTFLoader from 'three-gltf-loader';
import {Lensflare , LensflareElement} from '@zosma/three-lensflare-ts'
export default {
    data(){
        return{
            scene:null,
            camera:null,
            renderer:null,
            axis:null,
            size:10,
            shortbar:null,
            longbar:null,
            swingblock:null,
            myChart:null,
            myChart1:null,
            myChart2:null,
            show:true,
            show1:true,
            show2:true,
            slidertype:false,
            button1type:false,
            controls:null,//GUI界面
            floor:null,
            plate180:null,
            cylindergroup:null,
            stringmesh:null,
            polegroup:null,
            photogate:null,
            gategroup:null,
            plategroup:null,
            platepolegroup:null,
            light1:null,
            light1mesh:null,
            light2:null,
            light2mesh:null,
            light3:null,
            light3mesh:null,
            group_trans:null,
            rodmesh:null,
            theta_last:0,
            w_last:0,
            T:0,//周期
            wf:0,//固有频率
            powerw:0,
            m:0,
            t:0,
            flag:0,
            theta_degree:0,//角度制
            theta_rad:0,//弧度制
            theta1:0,
            theta2:0,
            alpha:0,
            phase:Math.PI/2,//相位
            maxtheta1:170,
            mintheta1:-170,
            theta_end:0,
            thetaright:-Math.PI/2,
            rodtheta:0,
            thetaleft:Math.PI/2,
            is_pause:false,
            button2:'fa fa-pause',
            button2text:'暂停',
            button2type:false,
            showtable:false,
            tableData:[],
            count:1,
            value2:false,
            maxT:17,
            minT:15,
            sliderT:15,
            styleObject:{
                position:'absolute',
                zIndex: '1000',
                right:'25px',
                top:'0px',
                width:'30%'
                },
            AWW0:new Map(),
            PhiWW0:new Map(),
            last_powerv:0,
            showGraphs:false,
            change_gui:0,
            A1array:[],
            A2array:[],
            A3array:[],
            Phi1array:[],
            Phi2array:[],
            Phi3array:[],
            polegroup_rotation:0,
            rodmesh_rotation:0,
            group_trans_rotation:0,
            openflash:0,
            plate180graph_array:[],
            powergraph_array:[],
            T10:0,
            }
    },
    methods:{
        
        init()
        {
            this.T = Math.random()*(1.62-1.55)+1.55
            this.damping = Math.random()*0.1 //查阻尼系数
            this.wf = 2*Math.PI/this.T//固有频率
            this.m=170/180*Math.PI*2*this.wf*0.0543
            this.last_powerv = this.wf/2/Math.PI-0.1
            this.addScene();
            this.addRender();
            this.addCamera();
            this.addFloor();
            this.add180();
            this.addCylinder();
            this.addHelix(6.5*Math.PI,-Math.PI/2-this.theta_rad);
            this.addPole()
            this.addTransparentPlate()
            this.addFlask()
            this.addPlate()
            this.addRod()
            this.addStand()
            this.addLight()
            //X red Z blue Y green	
            this.addAxis();
            this.addGui();
            this.addGui_group1();
            this.addListener();
            window.addEventListener( 'resize', this.onWindowResize, false );
            this.renderer.setAnimationLoop(this.animate);    
        },
        onWindowResize() {
            this.camera.aspect = window.innerWidth / window.innerHeight;
            this.camera.updateProjectionMatrix();
            this.renderer.setSize( window.innerWidth, window.innerHeight );
        },
        animate() 
        {    
            {
                switch (this.controls.vibration_type) {
                    case '自由振动':
                        this.closeTable;
                        this.count = 1;
                        this.closeEcharts();
                        break;
                    case '阻尼振动':
                        this.closeEcharts();
                        break;
                    case '受迫振动':
                        this.closeTable;
                        this.count = 1;
                        break;
                    default:
                        break;
                }
            }
            //更改css
            {
                var text = this.gui.domElement.getElementsByClassName("title")[0].innerText;
                var dict = {'自由振动':this.gui_group1,'阻尼振动':this.gui_group2,'受迫振动':this.gui_group3};
                switch (this.controls.vibration_type) {
                    case '自由振动':
                        if(text!='自由振动' && this.gui.domElement.getElementsByClassName("closed").length==0){
                            this.gui.removeFolder(dict[text])
                            this.addGui_group1();
                        }
                        break;
                    case '阻尼振动':
                        if(text!='阻尼振动' && this.gui.domElement.getElementsByClassName("closed").length==0){
                            this.gui.removeFolder(dict[text])
                            this.addGui_group2();
                        }
                        break;
                    case '受迫振动':
                        if(text!='受迫振动' && this.gui.domElement.getElementsByClassName("closed").length==0){
                            this.gui.removeFolder(dict[text])
                            this.addGui_group3();
                        }
                        break;
                    default:
                        break;
                }
                var str = document.getElementsByClassName("dg main a")[0].children[0].style.height;
                this.styleObject['top'] = parseInt(str.substring(0,str.length-2))+20+'px';
                //更改css
            }
            //对于自由振动和阻尼振动 在点开始按钮之前可以调节圆盘角度 随着gui更改角度以及更改弹簧位置
            if((this.controls.vibration_type == '自由振动' || this.controls.vibration_type == '阻尼振动')
             && this.button1type==false && this.plate180!=null){
                this.theta_rad=this.controls.theta_degree*Math.PI/180
                this.plate180.rotateY(this.theta_rad-this.theta_last)
                this.scene.remove(this.stringmesh)
                this.addHelix(6.5*Math.PI,-Math.PI/2+this.theta_rad)
                this.theta_last=this.theta_rad
            }
            //自由振动
            if(this.controls.vibration_type == '自由振动' && this.button1type==true && this.is_pause!=true){
                var dt = this.T/40
                var e_coefficient = Math.pow(Math.E,-0.01*this.t)
                this.theta_last = this.theta_rad*e_coefficient*Math.cos(this.wf*this.t)
                this.t+=dt
                e_coefficient = Math.pow(Math.E,-0.01*this.t)
                this.theta_end = this.theta_rad*e_coefficient*Math.cos(this.wf*this.t)
                this.changeGateColor();
                var thetabuf = this.theta_end - this.theta_last
                this.controls.amplitude = parseInt(this.theta_rad*e_coefficient*180/Math.PI)+''
                this.plate180.rotateY(thetabuf)
                this.scene.remove(this.stringmesh)
                this.addHelix(6.5*Math.PI,-Math.PI/2+this.theta_end)
            }
            //阻尼振动
            else if(this.controls.vibration_type == '阻尼振动' && this.button1type==true && this.is_pause!=true){
                var dt = this.T/40
                var e_coefficient = Math.pow(Math.E,-this.controls.beta*this.t)//e的系数 -e的beta*this.t次方
                this.theta_last = this.theta_rad*e_coefficient*Math.cos(this.wf*this.t)
                this.t+=dt
                e_coefficient =  Math.pow(Math.E,-this.controls.beta*this.t)
                this.theta_end = this.theta_rad*e_coefficient*Math.cos(this.wf*this.t)
                this.changeGateColor();
                //table
                if(this.t-this.count*this.T<0.1 && this.t-this.count*this.T>0){
                    if(this.showtable == true && this.tableData.length<10 ){
                        this.tableData.push({id: this.tableData.length+1,A:parseInt(Math.abs(this.theta_end)*180/Math.PI)})
                        this.T10+=dt*40;
                        this.T10 = parseInt(this.T10*10000)/10000;
                    }
                    this.count++
                }
                var thetabuf = this.theta_end - this.theta_last
                this.plate180.rotateY(thetabuf)
                this.scene.remove(this.stringmesh)
                this.addHelix(6.5*Math.PI,-Math.PI/2+this.theta_end)
            }
            else if(this.controls.vibration_type == '受迫振动' && this.button1type==true && this.is_pause!=true){
                this.powerw=2*Math.PI*this.controls.powerv
               
                var Phi=Math.atan(-2*this.controls.beta*this.powerw/(this.wf*this.wf-this.powerw*this.powerw))+Math.PI/2
                this.theta2 = this.m/Math.sqrt(Math.pow(this.wf*this.wf-this.powerw*this.powerw,2)+4*this.controls.beta*this.controls.beta*this.powerw*this.powerw)
                //theta2振幅
                this.controls.amplitude = parseInt(this.theta2*180/Math.PI)+''
                var dt = this.T/40
                var wwf = Math.sqrt(this.wf*this.wf-this.controls.beta*this.controls.beta) 
                if(this.last_powerv!=this.controls.powerv || this.t == 0){
                    this.t = 0 
                    this.alpha = Math.atan(-(this.w_last+this.powerw*this.theta2*Math.sin(Phi))/wwf/(this.theta_last-this.theta2*Math.cos(Phi)))
                    this.theta1 = (this.theta_last-this.theta2*Math.cos(Phi))/Math.cos(this.alpha)
                }
                this.t+=dt
                
                this.theta_end = this.theta1*Math.exp(-this.controls.beta*this.t)*Math.cos(wwf*this.t+this.alpha) + this.theta2*Math.cos(this.powerw*this.t+Phi) 
                this.changeGateColor();
                var dtheta=Math.PI-Math.abs(wwf*this.t+this.alpha-this.powerw*this.t-Phi)              
                this.controls.amplitude = parseInt(Math.sqrt(this.theta1*Math.exp(-this.controls.beta*this.t*2)*this.theta1+this.theta2*this.theta2-2*this.theta1*Math.exp(-this.controls.beta*this.t)*this.theta2*Math.cos(dtheta))*180/Math.PI)
                var thetabuf = this.theta_end - this.theta_last

                if(this.theta_end*this.theta_last<0 && this.openflash == 1){
                    this.changeLightColor(0xc4342d, 0xc4342d)
                }
                else this.changeLightColor(0x000000, 0x424242)
                this.theta_last = this.theta_end
                this.w_last = -this.controls.beta*this.theta1*Math.exp(-this.controls.beta*this.t)*Math.cos(wwf*this.t+this.alpha)
                              -wwf*this.theta1*Math.exp(-this.controls.beta*this.t)*Math.sin(wwf*this.t+this.alpha)
                              -this.powerw*this.theta2*Math.sin(this.powerw*this.t+Phi)

                //pole
                this.thetaright += dt * this.powerw
                this.plate180graph_array.push(this.theta_end*180/Math.PI)
                this.powergraph_array.push(100*Math.cos(this.thetaright-parseInt(this.thetaright/(2*Math.PI))*2*Math.PI))
                if(this.plate180graph_array.length>120){
                    this.plate180graph_array.shift();
                    this.powergraph_array.shift();
                }
                var xright=300+10*Math.cos(this.thetaright)
                var yright=-80+10*Math.sin(this.thetaright)
                
                var distanceXZ=Math.sqrt(Math.pow(xright,2)+Math.pow(yright,2));
                var leftlong=(Math.pow(300,2)+distanceXZ*distanceXZ-Math.pow(90,2))/2/distanceXZ;
                //右面圆
                //两个圆心连线与两个圆交点连线的中点坐标
                var bufx=xright*(distanceXZ-leftlong)/distanceXZ;
                var bufz=yright*(distanceXZ-leftlong)/distanceXZ;
                var bufUPdistance=Math.sqrt(Math.pow(300,2)-leftlong*leftlong);
                var vx=yright/distanceXZ;
                var vz=-xright/distanceXZ;
                var finalX1=bufx+vx*bufUPdistance;
                var finalX2=bufx-vx*bufUPdistance;
                var finalY1=bufz+vz*bufUPdistance;
                var finalY2=bufz-vz*bufUPdistance;
                if(finalY1>finalY2)
                {
                    finalY1=finalY2
                    finalX1=finalX2
                }
                var xleft=finalX1
                var yleft=finalY1
                var xmid=(xleft+xright)/2
                var ymid=(yleft+yright)/2
                var newrodtheta=-Math.atan((yright-yleft)/(xright-xleft))
                var newlefttheta=Math.acos(xleft/Math.sqrt(xleft*xleft+yleft*yleft))
                this.polegroup.rotateZ(this.thetaleft-newlefttheta)
                this.polegroup_rotation += this.thetaleft-newlefttheta
                this.rodmesh.rotateZ(this.rodtheta-newrodtheta)
                this.rodmesh_rotation += this.rodtheta-newrodtheta
                this.rodtheta=newrodtheta
                this.group_trans.rotateZ(dt * this.powerw)
                this.group_trans_rotation += dt*this.powerw
                this.rodmesh.position.set(xmid,ymid,60)
                this.thetaleft=newlefttheta
                this.plate180.rotateY(thetabuf)
                this.scene.remove(this.stringmesh)
                this.addHelix(7*Math.PI-this.thetaleft,-Math.PI/2-this.theta_end)
                //绘图
                {
                    this.showGraphs=true
                    this.echarts1.setOption(this.setEcharts(this.plate180graph_array,this.powergraph_array,'电机摆轮相位曲线'));
                    //this.echarts2.setOption(this.setEcharts(this.Phi1array,this.Phi2array,this.Phi3array,'相频特征曲线'))  
                }
                this.last_powerv = this.controls.powerv;
            }
            this.renderer.render( this.scene, this.camera );
        },
        addScene()
        {
            this.scene=new THREE.Scene();
        },
        addCamera()
        {
            this.camera=new THREE.PerspectiveCamera( 50, window.innerWidth/window.innerHeight,0.1,10000);
            var user = new THREE.Group();
            user.add( this.camera );
            user.position.set(100,-10,700)
            this.scene.add(user);
        },
        addRender()
        {
            this.renderer=new THREE.WebGLRenderer({antialias : true});
            this.renderer.setClearColor(0x000000);
            this.renderer.setPixelRatio( window.devicePixelRatio );
            this.renderer.setSize(window.innerWidth,window.innerHeight);
            document.getElementById("webGL_container").appendChild(this.renderer.domElement)
            this.renderer.vr.enabled = true;
            document.body.appendChild( WEBVR.createButton(this.renderer ) );
        },
        addOrbitControls()
        {
            var OrbitControls = require('three-orbit-controls')(THREE);
            var obcontrol = new OrbitControls(this.camera,this.renderer.domElement);
        },
        addAxis()
        {
            this.axis=new THREE.AxesHelper(200);
            this.scene.add(this.axis);
        },
        addLight()
        {
            var bulblight=[];
            for(var i=0;i<=5;i++)
            {
                bulblight[i]=new THREE.PointLight( 0xffffff, 3, 100, 1 );
            }
            bulblight[0].position.set(50,-50,80)
            bulblight[1].position.set(50,50,80)
            bulblight[2].position.set(-50,-50,80)
            bulblight[3].position.set(-50,50,80)
            bulblight[4] = new THREE.PointLight( 0xffffff, 3, 300, 1 )
            bulblight[4].position.set(200,0,50)
            bulblight[5] = new THREE.PointLight( 0xffffff, 3, 300, 1 )
            bulblight[5].position.set(300,-90,0)
            this.scene.add(bulblight[0])
            this.scene.add(bulblight[1])
            this.scene.add(bulblight[2])
            this.scene.add(bulblight[3])
            this.scene.add(bulblight[4])
            this.scene.add(bulblight[5])
        },
        
        addFloor()
        {
            var LoadTexture = (src,repeatx,repeaty)=>{
                var floorMat = new THREE.MeshBasicMaterial( {
                    color: 0xffffff,
                    side:THREE.BackSide
                })
                var textureLoader = new THREE.TextureLoader()
                textureLoader.load(src, function ( map ) {
                    map.wrapS = THREE.RepeatWrapping;
                    map.wrapT = THREE.RepeatWrapping;
                    map.anisotropy = 4;
                    map.repeat.set(repeatx,repeaty);
                    floorMat.map = map;
                    floorMat.needsUpdate = true;
                })
                return floorMat
            };
            var boxTexture=[]
            boxTexture[3]=LoadTexture("../../static/images/hardwood2_diffuse.jpg",8,8)
            for(var i=0;i<=5;i++){
                if(i==3) continue;
                boxTexture[i]=LoadTexture("../../static/images/woodtexture.jpg",2,2)
            }
            var boxH = 5000
            var box=new THREE.BoxBufferGeometry(boxH,boxH,boxH)
            this.floor=new THREE.Mesh(box,boxTexture);
            this.floor.position.x=0;
            this.floor.position.y=1/2*boxH-300;
            this.floor.position.z=0;
            this.scene.add(this.floor);
        },
        addStand(){
            //支架 最大
            var loadermodel = new OBJLoader().load("../../static/models/stand.obj",(obj)=>{
                obj.scale.set(50,50,50)
                obj.position.set(40,-160,-8)
                var box = new THREE.BoxGeometry( 2, 2 ,0.5 );
                this.light3 = new THREE.PointLight( 0x000000, 2, 20);
                this.light3mesh = new THREE.Mesh( box, new THREE.MeshBasicMaterial( { color: 0x424242} ) )
                this.light3.add( this.light3mesh );
                this.light3.position.set(3,95,18)
                this.scene.add(this.light3)
                this.scene.add(obj)
            })
        },
        add180()
        {
            var loadermodel = new OBJLoader()
            loadermodel.load('../../static/models/180.obj',(obj)=>{
                obj.traverse(function(child){
                    child.material=new THREE.MeshPhongMaterial({color: 0x010101});
                })
                obj.children[0].geometry.center()
                obj.rotateX(Math.PI/2)
                this.scene.add(obj)
                this.plate180 = obj
                })
        },
        
        //右边轴
        addCylinder(){
            //轴 右轴
            this.cylindergroup = new THREE.Group()
            var cylinder1=new THREE.CylinderGeometry(15, 15 ,30,40)
            var cylinder2=new THREE.CylinderGeometry(5, 5 ,65,40)
            var cylinderMat = new THREE.MeshPhongMaterial({
                color:0x63686a,
                wireframe:false
            })
            var cylindermesh1 = new THREE.Mesh(cylinder1,cylinderMat)
            var cylindermesh2 = new THREE.Mesh(cylinder2,cylinderMat)
            this.cylindergroup.add(cylindermesh1)
            this.cylindergroup.add(cylindermesh2)
            cylindermesh2.position.set(0,8,0)
            this.cylindergroup.position.set(0,0,20);
            this.cylindergroup.rotation.x = Math.PI/2
            this.scene.add(this.cylindergroup)
        },
        addHelix(angle1,angle2)
        {
            var extrudeSettings = {
                bevelEnabled: false, 
                steps: 1,
                depth: 20, //extrusion depth, don't define an extrudePath
                material:0, //material index of the front and back face
                extrudeMaterial : 1 //material index of the side faces            
            }
            var spring=new THREE.Shape();
            var H=60;
            spring.moveTo(-H*Math.sin(angle1-6.5*Math.PI),H*Math.cos(angle1-6.5*Math.PI));
            var i = angle1;
            var r = H;
            while(i>=angle2)
            {
                i-=Math.PI/20;
                r-=H/160*7*Math.PI/(angle1-angle2);
                spring.lineTo(r*Math.cos(i),r*Math.sin(i));
            }
            r+=1;
            while(i<=angle1)
            {
                i+=Math.PI/20;
                r+=H/160*7*Math.PI/(angle1-angle2);
                spring.lineTo(r*Math.cos(i),r*Math.sin(i));
            }
            spring.lineTo(-H*Math.sin(angle1-6.5*Math.PI),H*Math.cos(angle1-6.5*Math.PI));
            var stretched=new THREE.ExtrudeGeometry(spring,extrudeSettings);
            var springmat = new THREE.MeshPhongMaterial({color:0x918e8c})
            this.stringmesh=new THREE.Mesh(stretched,springmat)
            this.stringmesh.position.set(0,0,10)
            this.stringmesh.rotateZ(1/6*Math.PI)
            this.scene.add(this.stringmesh)
        },
        //this.polegroup
        addPole(){
            var drawShape = ()=>
            {
                var shape1=new THREE.Shape();
                shape1.moveTo(-5,0);
                shape1.lineTo(5,0);
                shape1.lineTo(5,6);
                shape1.lineTo(0,22);
                shape1.lineTo(-5,6)
                shape1.lineTo(-5,0);
                var extrudeSettings = {
                    bevelEnabled: false, 
                    steps: 1,
                    depth: 2, //extrusion depth, don't define an extrudePath
                    material:0, //material index of the front and back face
                    extrudeMaterial : 1 //material index of the side faces            
                }
                var shape11=new THREE.ExtrudeGeometry(shape1,extrudeSettings);
                return shape11;
            }
            this.polegroup=new THREE.Group() 
            //竖
            var pole1 = new THREE.CubeGeometry(15,5,202)
            var streched = new THREE.MeshPhongMaterial({color:0xd2d4c3})
            var polemesh1 = new THREE.Mesh(pole1,streched)
            polemesh1.position.set(0,-40,57)
            polemesh1.rotation.x = Math.PI/2
            this.polegroup.add(polemesh1)
            //横上
            var pole2 = new THREE.CubeGeometry(15,5,50)
            var polemesh2 = new THREE.Mesh(pole2,streched)
            polemesh2.position.set(0,63,35)
            this.polegroup.add(polemesh2)
            //横下
            var pole3 = new THREE.CubeGeometry(10,5,25)
            var streched3 = new THREE.MeshPhongMaterial({color:0x010101})
            var polemesh3 = new THREE.Mesh(pole3,streched3)
            polemesh3.position.set(0,58,30)
            this.polegroup.add(polemesh3)
            //指针
            var triangle = drawShape()
            var tristrech = new THREE.MeshPhongMaterial({color:0xfc9303})
            var trimesh = new THREE.Mesh(triangle,tristrech)
            trimesh.position.set(0,65,10)
            this.polegroup.add(trimesh)
            //this.polegroup.rotation.z = Math.PI/2
            this.scene.add(this.polegroup)
        },
        addPlate()
        {
            this.plategroup = new THREE.Group()
            var platemtl = new MTLLoader()
            platemtl.load('../../static/models/plate1.mtl',(mtl)=>{
                mtl.preload()
                var loadermodel = new OBJLoader()
                loadermodel.load('../../static/models/plate1.obj',(obj)=>{
                obj.material=mtl
                obj.rotation.x =Math.PI/2
                obj.position.set(300,-70,0)
                this.plategroup.add(obj)
                })
            })
            this.platepolegroup =  new THREE.Group()
            var cylinder1=new THREE.CylinderGeometry(30, 30,20,40)
            var cylinder2=new THREE.CylinderGeometry(15, 15,40,40)
            var cylinderMat = new THREE.MeshPhongMaterial({
                color:0x63686a,
                wireframe:false
            })
            var cylindermesh1 = new THREE.Mesh(cylinder1,cylinderMat)
            var cylindermesh2 = new THREE.Mesh(cylinder2,cylinderMat)
            this.platepolegroup.add(cylindermesh1)
            this.platepolegroup.add(cylindermesh2)
            cylindermesh2.position.set(0,10,0)
            this.platepolegroup.rotation.x = Math.PI/2
            this.platepolegroup.position.set(300,-90,0);
            this.plategroup.add(this.platepolegroup)
            this.plategroup.position.set(0,10,30)
            this.scene.add(this.plategroup)
        },
        addRod(){
            var rod = new THREE.CylinderGeometry(3, 3,300,20)
            var cylinderMat = new THREE.MeshPhongMaterial({
                color:0x63686a,
                wireframe:false
            })
            this.rodmesh = new THREE.Mesh(rod,cylinderMat)
            this.rodmesh.rotation.z=Math.PI/2
            this.rodmesh.position.set(150,-90,60)
            this.scene.add(this.rodmesh)
        },
        //this.group_trans
        addTransparentPlate(){
            this.group_trans = new THREE.Group();
            var obj = new THREE.CylinderGeometry(60,60,2,40,40);
            var material = new THREE.MeshBasicMaterial({color:'white',transparent:true,opacity:0.3});
            var mesh = new THREE.Mesh(obj,material);
            mesh.rotation.x = Math.PI/2;
         
            var box = new THREE.BoxGeometry( 14, 0.5 ,2 );
            this.light1 = new THREE.PointLight( 0x000000, 1, 25);
            this.light1mesh = new THREE.Mesh( box, new THREE.MeshBasicMaterial( { color: 0x424242} ) )
            this.light1.add( this.light1mesh );
            this.light2 = new THREE.PointLight( 0x000000, 1, 25);
            this.light2mesh =  new THREE.Mesh( box, new THREE.MeshBasicMaterial( { color: 0x424242 } ) ) 
            this.light2.add(this.light2mesh);
            this.light1.position.set(-50,0,0);
            this.light2.position.set(50,0,0);//长条灯
            this.group_trans.add(mesh);
            this.group_trans.add(this.light1);
            this.group_trans.add(this.light2); 
            this.group_trans.position.set(300,-80,35);//透明盘结束
            this.scene.add(this.group_trans);
            
        },
        //闪光灯
        addFlask(){
            //添加闪光灯
            var geo = new THREE.BoxGeometry(50,70,50);
            var mater = new THREE.MeshPhongMaterial(({color:0x010101}));
            var mesh = new THREE.Mesh(geo,mater);
            mesh.position.set(292,-150,110)
            this.scene.add(mesh);
        },
        //改变闪光颜色
        changeLightColor(c1,c2){
            //不亮 this.changeLightColor(0x000000, 0x424242);
            //亮  this.changeLightColor(0xc4342d, 0xc4342d);
            this.light1.color.set(c1);
            this.light1mesh.material.color.set(c2);
            this.light2.color.set(c1);
            this.light2mesh.material.color.set(c2);
        },
        changeGateColor(){
            if(this.theta_end*this.theta_last<0){
                this.light3mesh.material.color.set(0xffffff);
                this.light3.color.set(0xc4342d);
            }
            else{
                this.light3mesh.material.color.set(0x424242);
                this.light3.color.set(0x000000);
            }
        },
        addListener(){
            var onWindowResize = ()=> {
                this.camera.aspect = window.innerWidth / window.innerHeight;
                this.camera.updateProjectionMatrix();
                this.renderer.setSize(window.innerWidth, window.innerHeight);
            }
            window.addEventListener('resize',onWindowResize);
        },
        
        // 添加window 的resize事件监听
        play(){
            this.disabledGui0();
            //点击确定后更改按钮状态
            {
                this.button1type = true
                this.button2type = false
                this.button2='fa fa-pause'
                this.button2text='暂停'
            }
            {
                switch (this.controls.vibration_type) {
                    case '自由振动':
                        this.disabledGuiGroup1();
                        this.count = 1;
                        break;
                    case '阻尼振动':
                        this.disabledGuiGroup2();
                        this.count = 1;
                        this.closeTable();
                        break;
                    case '受迫振动':
                        this.disabledGuiGroup3();
                        break;
                    default:
                        break;
                }
            }
        },
        pause(){
            if(this.is_pause == false){
                this.button2='fa fa-play'
                this.button2text='继续'
                this.is_pause=true
            }else{
                this.button2='fa fa-pause'
                this.button2text='暂停'
                this.is_pause=false
            }   
        },
        stop(){
            this.enabledGui0()
            //所有情况按钮都会这样变化
            this.button1type = false
            this.button2type=true
            this.button2='fa fa-pause'
            this.button2text='暂停'
            this.is_pause = false
            //所有情况弹簧归零都一样
            this.scene.remove(this.stringmesh)
            this.addHelix(6.5*Math.PI,-Math.PI/2-0);
            //转盘角度归0
            this.plate180.rotateY(-this.theta_end)
            this.theta_end=0
            this.t = 0
            this.theta_last = 0
            this.w_last=0
            this.controls.amplitude = '0'
            if(this.controls.vibration_type=='自由振动'){
                //gui回到原样
                {
                    this.controls.theta_degree = 0
                    this.enabledGuiGroup1();
                }   
            }   
            else if( this.controls.vibration_type == '阻尼振动'){
                //gui回到原样
                {
                    this.controls.theta_degree = 0
                    this.enabledGuiGroup2()
                }
                //清空图表
                {
                    this.closeEcharts()
                    this.showGraphs = 0
                }
                //清空表格
                {
                    this.closeTable()
                    this.count =1;
                }   
            }
            else if( this.controls.vibration_type == '受迫振动'){
                //杆件回正
                {
                    this.rodmesh.rotateZ(-this.rodmesh_rotation)
                    this.group_trans.rotateZ(-this.group_trans_rotation)
                    this.polegroup.rotateZ(-this.polegroup_rotation)
                    this.polegroup_rotation=0
                    this.rodmesh_rotation=0
                    this.group_trans_rotation=0
                    this.rodmesh.position.set(150,-90,60)
                }
                //gui回到原样
                {
                    this.controls.powerv = this.wf/2/Math.PI-0.1
                    this.enabledGuiGroup3()
                }
                {
                    this.AWW0 = new Map();
                    this.PhiWW0 = new Map();
                }
            }
            // this.theta_last=0 
            // this.theta2=0
        },
        addGui()
        {
            this.gui=new dat.GUI();
            this.controls=
            {
                vibration_type:'自由振动',//振动类别
                // damping:false,
                // power:false,
                beta:0.0543,
                theta_degree:0,//初始角度为0
                powerv:this.wf/2/Math.PI,//电机频率 this.wf/2/Math.PI-0.1
                phi0:Math.PI/2,//初相位
                amplitude:'0',
                measure:()=>{
                    if(this.button1type == true){
                        this.showtable = true;          
                    }
                },
                flash:()=>{
                    this.openflash = 1;
                }
            }
            this.gui0 = this.gui.add(this.controls,'vibration_type',['自由振动','阻尼振动','受迫振动']).name("振动类别");
        },
        addGui_group1(){
            this.gui_group1 = this.gui.addFolder("自由振动");
            this.theta_degree = this.gui_group1.add(this.controls,"theta_degree",-170,170).name("摆轮初始角度(°)").listen();
            this.amplitude = this.gui_group1.add(this.controls,"amplitude","0").name("振幅").listen()
            this.amplitude.domElement.style.pointerEvents = "none"
            this.gui_group1.open();
        },
        disabledGuiGroup1(){
            this.theta_degree.domElement.style.pointerEvents = "none"
            this.theta_degree.domElement.style.opacity = .5;
        },
        enabledGuiGroup1(){
            this.theta_degree.domElement.style.pointerEvents = "auto"
            this.theta_degree.domElement.style.opacity = 1;
        },
        addGui_group2(){
            this.gui_group2 = this.gui.addFolder("阻尼振动");
            this.theta_degree = this.gui_group2.add(this.controls,"theta_degree",-170,170).name("摆轮初始角度(°)").listen();
            this.beta = this.gui_group2.add(this.controls,"beta",{'阻尼1':0.0543,'阻尼2':0.0554,'阻尼3':0.0571}).name('阻尼系数');
            this.button_gui = this.gui_group2.add(this.controls,'measure').name('点击此处测量振幅').listen();
            this.gui_group2.open();
        },
        getController(gui,object, property)
        {
            for (var i = 0; i < gui.__controllers.length; i++)
            {
                var controller = gui.__controllers[i];
                if (controller.object == object && controller.property == property)
                    return controller;
            }
            return null;
        },
        disabledGuiGroup2(){
            this.theta_degree.domElement.style.pointerEvents = "none"
            this.theta_degree.domElement.style.opacity = .5;
            this.beta.domElement.style.pointerEvents = "none"
            this.beta.domElement.style.opacity = .5
        },
        enabledGuiGroup2(){
            this.theta_degree.domElement.style.pointerEvents = "auto"
            this.theta_degree.domElement.style.opacity = 1;
            this.beta.domElement.style.pointerEvents = "auto"
            this.beta.domElement.style.opacity = 1;
        },
        addGui_group3(){
            this.gui_group3 = this.gui.addFolder("受迫振动");
            this.gui_group3.add(this.controls,"powerv",this.wf/2/Math.PI-0.1,this.wf/2/Math.PI+0.1).name("电机频率").listen();
            this.beta = this.gui_group3.add(this.controls,"beta",{'阻尼1':0.0543,'阻尼2':0.0554,'阻尼3':0.0571}).name('阻尼系数').listen();
            this.amplitude = this.gui_group3.add(this.controls,"amplitude","0").name("振幅").listen()
            this.amplitude.domElement.style.pointerEvents = "none"
            this.button_gui = this.gui_group3.add(this.controls,'flash').name('开启闪光灯').listen();
            this.gui_group3.open();
        },
        disabledGuiGroup3(){
            this.beta.domElement.style.pointerEvents = "none"
            this.beta.domElement.style.opacity = .5;
        },
        enabledGuiGroup3(){
            this.beta.domElement.style.pointerEvents = "auto"
            this.beta.domElement.style.opacity = 1;
        },
        disabledGui0(){
            this.gui0.domElement.style.pointerEvents = "none"
            this.gui0.domElement.style.opacity = .5;
        },
        enabledGui0(){
            this.gui0.domElement.style.pointerEvents = "auto"
            this.gui0.domElement.style.opacity = 1;
        },
        closeTable(){
            this.showtable = false;
            this.tableData = [];
        },
        closeEcharts(){
            this.showGraphs = false
            this.AWW0=new Map()
            this.PhiWW0=new Map()
            this.A1array=[]
            this.A2array=[]
            this.A3array=[]
            this.Phi1array=[]
            this.Phi2array=[]
            this.Phi3array=[]
        },
        //speedFar 最大的圆自转速度 speedMiddle 最小圆转速 omegaH 公转速度 omega2 自转速度
        toPage(path)
        {
            this.$router.push(path);
        },
       
        setEcharts(array1,array2,text)
        {
            var option = {
                title: {
                    text: text,
                    textStyle: {//title字体的样式
                        color: '#fff',
                    }
                },
                tooltip: {
                    trigger: 'axis'
                },
                legend: {
                    data:['摆轮', '电机'],
                    textStyle:{
                        color: "#fff"
                    }
                },
                xAxis: {
                    type: 'category',
                },
                yAxis: {
                    type: 'value'
                },
                textStyle: {
                    color: "#fff"
                },
                series: [
                {
                    name:'摆轮',
                    data: array1,
                    type: 'line',
                    smooth: true,
                    color:'blue'
                },
                {
                    name:'电机',
                    data: array2,
                    type: 'line',
                    smooth: true,
                    color:'yellow'
                }]
            };
            return option;
        },
        },
        mounted(){
            this.init();
            // this.myChart=this.$echarts.init(document.getElementById('myecharts'));
            this.echarts1=this.$echarts.init(document.getElementById('echarts1'));
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