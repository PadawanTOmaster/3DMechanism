<template>
<div>
    <el-row >
        <div style="top:15px;left:15px;z-index:1000;position:absolute;opacity:0.8;">
            <el-button type="success" round @click="Topage('/threed')">返回</el-button>
            <!-- <el-button @click="show1=!show1" type="success" round>看图</el-button>
            <el-button @click="show2=!show2" type="success" round>看讲解</el-button> -->
        </div>
    </el-row>
    <div id="webGL_container" style="position:absolute;z-index:0">
    </div>
    <div class = 'container'>
        <div class="block">
            <span style="color:#ffffff">摆轮初始角度(不得超过±170°)</span>
            <el-slider 
            v-model="theta1du"
            :max='maxtheta1'
            :min='mintheta1'
            :disabled="slidertype"
            show-input
            ></el-slider>
            <el-tooltip class="item" effect="dark" content="确定" placement="bottom">
                <el-button type="success" circle :disabled="buttontype" @click="play"><i class="fa fa-check"></i></el-button>                
            </el-tooltip>
            <el-tooltip class="item" effect="dark" :content="button2text" placement="bottom">
                <el-button type="warning" circle :disabled="button2type" @click="pause"><i :class="button2"></i></el-button>              
            </el-tooltip>
            <el-tooltip class="item" effect="dark" content="重置" placement="bottom">
                <el-button type="danger" circle @click="stop"><i class="fa fa-refresh"></i></el-button>              
            </el-tooltip>
        </div>
        <el-collapse-transition>
            <div v-show='showtable'>
                <el-table
                :data="tableData"
                border
                width="40%"
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
            </div> 
        </el-collapse-transition>
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
  .box-card {
    width: 480px;
  }
  .container {
        position:absolute;
        z-index: 1000;
        left:25px;
        top:100px;
        width:30%;
        
    }
    .container2{
        position:absolute;
        z-index: 1000;
        right:25px;
        top:100px;
        width:30%;
    }
    .block {
        text-align:left;
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
import {MTLLoader, OBJLoader} from 'three-obj-mtl-loader'


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
            buttontype:false,
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
            rodmesh:null,
            lasttheta:0,
            T:0,
            wf:0,
            powerw:0,
            m:0,
            t:0,
            flag:0,
            theta1du:0,//角度制
            theta1:0,//弧度制
            theta2:0,
            phase:Math.PI/2,//相位
            maxtheta1:170,
            mintheta1:-170,
            thetaend:0,
            thetaright:-Math.PI/2,
            rodtheta:0,
            thetaleft:Math.PI/2,
            ispause:false,
            button2:'fa fa-pause',
            button2text:'暂停',
            button2type:false,
            damping:null,
            showtable:false,
            tableData:[],
            count:1,
            value2:false,
            maxT:17,
            minT:15,
            sliderT:15,
            }
    },
    methods:{
        
        init()
        {
            this.T = Math.random()*(1.62-1.55)+1.55
            this.damping = Math.random()*0.1 //查阻尼系数
            this.wf = 2*Math.PI/this.T
            this.m=280/180*Math.PI*this.damping*this.wf
            this.AddScene();
            this.AddCamera();
            this.AddRender();
            this.AddOrbitControls();
            this.Addfloor();
            this.Add180();
            this.AddCylinder();
            this.AddHelix(6.5*Math.PI,-Math.PI/2-this.theta1);
            this.AddPole()
        
            this.AddPlate()
            this.AddRod()
            this.Addstand()
            this.Addlight()
            //X red Z blue Y green	
            this.AddAxis();
            this.AddGui()
            this.animate();
            
        },
         
        AddScene()
        {
            this.scene=new THREE.Scene();
        },

        AddCamera()
        {
            this.camera=new THREE.PerspectiveCamera( 50, window.innerWidth/window.innerHeight,0.1,10000);
            this.camera.position.x=400;
            this.camera.position.y=800;
            this.camera.position.z=400;//40 40 40 //0 150 400
            this.camera.lookAt(0,0,0);
        },

        AddRender()
        {
            this.renderer=new THREE.WebGLRenderer({antialias : true});
            this.renderer.setClearColor(0x000000);
            this.renderer.setSize(window.innerWidth,window.innerHeight);
            document.getElementById("webGL_container").appendChild(this.renderer.domElement)
        },

        AddOrbitControls()
        {
            var OrbitControls = require('three-orbit-controls')(THREE);
            var obcontrol = new OrbitControls(this.camera,this.renderer.domElement);
        },

        AddAxis()
        {
            this.axis=new THREE.AxesHelper(200);
            this.scene.add(this.axis);
        },
        
        Addfloor()
        {
            var boxTexture=[]
            boxTexture[3]=this.LoadTexture("../../static/images/hardwood2_diffuse.jpg",8,8)
            for(var i=0;i<=5;i++){
                if(i==3) continue;
                boxTexture[i]=this.LoadTexture("../../static/images/woodtexture.jpg",2,2)
            }
            var boxH = 5000
            var box=new THREE.BoxBufferGeometry(boxH,boxH,boxH)
            this.floor=new THREE.Mesh(box,boxTexture);
            this.floor.position.x=0;
            this.floor.position.y=1/2*boxH-300;
            this.floor.position.z=0;
            this.scene.add(this.floor);
        },
        LoadTexture(src,repeatx,repeaty){
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
        },
        Addstand(){
            var loadermodel = new OBJLoader().load("../../static/models/stand.obj",(obj)=>{
                obj.scale.set(50,50,50)
                obj.position.set(35,-210,19)
                this.scene.add(obj)
            })
        },
        Add180()
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
        AddCylinder(){
            //轴
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
        AddHelix(angle1,angle2)
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
        drawShape()
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
        },
        AddPole(){
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
            var triangle = this.drawShape()
            var tristrech = new THREE.MeshPhongMaterial({color:0xfc9303})
            var trimesh = new THREE.Mesh(triangle,tristrech)
            trimesh.position.set(0,65,10)
            this.polegroup.add(trimesh)
            //this.polegroup.rotation.z = Math.PI/2
            this.scene.add(this.polegroup)
        },
        AddPlate()
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
        AddRod(){
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
        Addlight()
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
        turnGrey(){
            this.buttontype = true
            this.slidertype = true
            this.button2type = false
            this.showtable=false
        },
        animate() 
        {   
            if(this.buttontype==false && this.plate180!=null){
                this.button2type = true
                this.theta1=this.theta1du*Math.PI/180
                this.plate180.rotateY(-this.lasttheta)
                this.plate180.rotateY(this.theta1)
                this.scene.remove(this.stringmesh)
                this.AddHelix(6.5*Math.PI,-Math.PI/2+this.theta1)
                this.lasttheta=this.theta1
            }
            if(this.buttontype==true && this.plate180!=null && this.ispause==false){
                if(this.controls['power']==true){
                    
                    this.controls['damping']=true
                    this.turnGrey()
                    if(this.powerw!=2*Math.PI*this.controls['powerv'])
                    {
                        this.powerw=2*Math.PI*this.controls['powerv']
                        this.t=0 
                        this.phase=Math.atan(2*this.damping*this.powerw/(this.wf*this.wf-this.powerw*this.powerw))
                    }
                    this.theta2 = this.m/Math.sqrt(Math.pow(this.wf*this.wf-this.powerw*this.powerw,2)+4*this.damping*this.damping*this.wf*this.wf)

                }
                var bt = 1
                this.button2type = false
                var dt = this.T/25
                this.t+=dt
                if(this.controls['damping']==true){
                    bt = Math.pow(Math.E,-this.damping*this.t)
                }
                var thetabuf = this.theta1*bt*Math.cos(this.wf*this.t)+this.theta2*Math.cos(this.powerw*this.t+Math.PI/2)-this.thetaend
                this.thetaend= this.theta1*bt*Math.cos(this.wf*this.t)+this.theta2*Math.cos(this.powerw*this.t+Math.PI/2)
                //this.thetaend= this.thetaend*2
                //var thetabuf=this.theta1*bt*(this.damping*Math.cos(this.wf*this.t)+this.wf*Math.sin(this.wf*this.t))+this.theta2*this.powerw*Math.sin(this.powerw*this.t+this.phase)
                //thetabuf/=5
                //this.thetaend+=thetabuf
                //table
                if(this.t-this.count*this.T<0.1 && this.t-this.count*this.T>0 && this.controls['power']==false){
                    this.tableData.push({id:this.count,A:parseInt(this.thetaend*180/Math.PI)})
                    this.count++
                    if(this.count==11)this.count=1
                }
                if(this.thetaend <=0.04 && this.thetabuf<=0.04)this.stop()
                //pole
                this.thetaright += dt * this.powerw
                
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

                this.rodmesh.rotateZ(this.rodtheta-newrodtheta)
                this.rodtheta=newrodtheta
                this.polegroup.rotateZ(this.thetaleft-newlefttheta)
                this.rodmesh.position.set(xmid,ymid,60)
                this.thetaleft=newlefttheta

                this.plate180.rotateY(thetabuf)
                //居然是y在转
                this.scene.remove(this.stringmesh)
                this.AddHelix(7*Math.PI-this.thetaleft,-Math.PI/2-this.thetaend)
            }
            // if(this.value2==true){
                
            // }
            this.renderer.render( this.scene, this.camera );
            requestAnimationFrame(this.animate);
        },
        play(){
            //点击确定
            this.buttontype = true
            this.slidertype = true
            this.button2type = false
            this.showtable=true
            this.button2='fa fa-pause'
            this.button2text='暂停'
            this.ispause=false
        },
        pause(){
            if(this.ispause == false){
                this.button2='fa fa-play'
                this.button2text='继续'
                this.ispause=true
            }else{
                this.button2='fa fa-pause'
                this.button2text='暂停'
                this.ispause=false
            }   
        },

        stop(){
            //还原到最初样子
            //开始按钮  slider可用 角度为0 theta1du=0 thetaend=0 t =0 弹簧回0 摆轮回0 lasttheta=0
            this.plate180.rotateY(-this.thetaend)
            this.thetaend=0
            this.theta1du = 0
            this.t = 0
            this.scene.remove(this.stringmesh)
            this.AddHelix(6.5*Math.PI,-Math.PI/2-0);
            this.button2type=true
            this.ispause=false
            this.button2='fa fa-pause'
            this.button2text='暂停'
            this.buttontype = false
            //这个！！！害我查了两个小时bug
            this.lasttheta=0 
            this.slidertype = false
            this.theta2=0
        },
        AddGui()
        {
            this.controls=
            {
                damping:false,
                power:false,
                powerv:this.wf/2/Math.PI,
                phi0:Math.PI/2,
            }
            var gui=new dat.GUI();
            var group1 = gui.addFolder("阻尼振动")
            var group2 = gui.addFolder("受迫振动")
            
            //LongestPole为长度
            group1.add(this.controls,"damping").name("是否添加阻尼").listen()
            group1.open()
            group2.add(this.controls,'power').name("是否添加策动力").listen()
            group2.add(this.controls,'phi0',0,Math.PI).name("初相位")
            group2.add(this.controls,"powerv",0,1).name("电机频率")
            group2.open()
        },
        //speedFar 最大的圆自转速度 speedMiddle 最小圆转速 omegaH 公转速度 omega2 自转速度
        Topage(path)
        {
            this.$router.push(path);
        },

       
        setEcharts(buffList,linecolor,text)
        {
            var option = {
                title: {
                    text: text,
                    textStyle: {
	        	        color: '#faf0e6'
	      	        }
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
        },
        mounted(){
            this.init();
            // this.myChart=this.$echarts.init(document.getElementById('myecharts'));
            // this.myChart1=this.$echarts.init(document.getElementById('myecharts1'));
            // this.myChart2=this.$echarts.init(document.getElementById('myecharts2'));
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