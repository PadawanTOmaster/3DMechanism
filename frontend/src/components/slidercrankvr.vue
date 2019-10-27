<template>
<div>
    <el-row >
        <div style="top:15px;left:15px;z-index:1000;position:absolute;opacity:0.8;">
            <el-button type="success" round @click="Topage('/threed')">返回</el-button>
            <el-button @click="show1=!show1" type="success" round>看图</el-button>
            <el-button @click="show2=!show2" type="success" round>看讲解</el-button>
        </div>
    </el-row>
    <div id="webGL_container" style="position:absolute;z-index:0">
    </div>
    
     <el-collapse-transition>
         <div style="z-index:1000;position:absolute;left:20px;top:100px;">
        <el-container v-show="show1">
            <el-main>
                <div id="myecharts" style="width:400px;height:200px;"></div>
                <div id="myecharts1" style="width:400px;height:200px;"></div>
                <div id="myecharts2" style="width:400px;height:200px;"></div>
            </el-main>
        </el-container>
        </div>
     </el-collapse-transition>
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
 
</style>

<script>
import * as THREE from 'three'
import dat from 'dat.gui'
import { WEBVR } from 'three/examples/jsm/vr/WebVR.js';
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
            controls:null,//GUI界面
            barwide:1,
            angleA:-Math.PI/2,//原动件（匀速转动的杆）的夹角
            angleB:0,//另一杆的夹角 == 块的夹角
            xlist:[],
            vlist:[],
            alist:[],
            extrudeSettings : {
                bevelEnabled: false, 
                steps: 1,
                depth: 0.5, //extrusion depth, don't define an extrudePath
                material:0, //material index of the front and back face
                extrudeMaterial : 1 //material index of the side faces            
            }
            }
    },
    methods:{
        
        init()
        {
            
            this.AddScene();
            
            this.AddCamera();
            this.AddRender();
            this.Gui();
            this.Addfloor();
            this.Addlight();
            //X red Z blue Y green  
            this.AddAxis();
            this.AddLine();
            this.Addshortbar();
            this.Addlongbar();
            //滑块
            this.swingblock = this.Addswingblock(20*this.barwide,0,0);
            
            this.renderer.setAnimationLoop(this.animate);   
        },
         
        AddScene()
        {
            this.scene=new THREE.Scene();
        },
        AddCamera()
        {
            window.addEventListener( 'resize', this.onWindowResize, false );
            this.camera=new THREE.PerspectiveCamera( 50, window.innerWidth/window.innerHeight,0.1,1000);
            var user = new THREE.Group();
            user.add( this.camera );
            user.position.set(5,0,40);
            this.scene.add(user);
        },
        onWindowResize() {
            this.camera.aspect = window.innerWidth / window.innerHeight;
            this.camera.updateProjectionMatrix();
            this.renderer.setSize( window.innerWidth, window.innerHeight );
        },
        AddRender()
        {
            this.renderer=new THREE.WebGLRenderer({antialias : true});
            this.renderer.setClearColor(0x010101);
            this.renderer.setPixelRatio( window.devicePixelRatio );
            this.renderer.setSize(window.innerWidth,window.innerHeight);
            document.getElementById("webGL_container").appendChild(this.renderer.domElement)
            this.renderer.vr.enabled = true;
            document.body.appendChild( WEBVR.createButton(this.renderer ) );
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
            var floorMat = new THREE.MeshStandardMaterial( {
                roughness: 0.8,
                color: 0xffffff,
                metalness: 0.2,
                bumpScale: 0.0005
            } );
            var textureLoader = new THREE.TextureLoader();
            textureLoader.load( "../../static/images/hardwood2_diffuse.jpg", function ( map ) {
                map.wrapS = THREE.RepeatWrapping;
                map.wrapT = THREE.RepeatWrapping;
                map.anisotropy = 4;
                map.repeat.set( 10, 24 );
                floorMat.map = map;
                floorMat.needsUpdate = true;
            } );
            var floorGeometry = new THREE.PlaneBufferGeometry( 200, 200 );
            var floorMesh = new THREE.Mesh( floorGeometry, floorMat );
            floorMesh.receiveShadow = true;
            // floorMesh.rotation.x = - Math.PI / 2.0;
            floorMesh.position.set(0,0,-40)
            this.scene.add( floorMesh );
        },
        Addlight()
        {
            var bulbLight = new THREE.PointLight( 0xffee88, 3, 100, 2 );
            bulbLight.position.set(0,0, 20*this.barwide);
            bulbLight.castShadow = true;
            this.scene.add( bulbLight );
        },
        Addshortbar()
        {
            var groupbar=new THREE.Group(); 
            var bar=this.drawBarGeometry(10*this.barwide);                                                    
            var upFillet=this.DrawFillet(0.5*this.barwide);
            var downFillet=this.DrawFillet(0.5*this.barwide);
            upFillet.position.y=10*this.barwide;
            downFillet.rotateZ(Math.PI);
            this.short_bar=bar;
            this.shorthalfcircle=upFillet;
            groupbar.add(this.short_bar);
            groupbar.add(upFillet);
            groupbar.add(downFillet);
            groupbar.position.set(0,5*this.barwide,this.barwide/4);
            groupbar.rotateZ(-Math.PI);
            this.scene.add(groupbar);
            this.shortbar = groupbar;
        },
        Addlongbar()
        {
            var groupbar=new THREE.Group(); 
            var bar=this.drawBarGeometry(20*this.barwide);                                                    
            var upFillet=this.DrawFillet(0.5*this.barwide);
            var downFillet=this.DrawFillet(0.5*this.barwide);
            upFillet.position.y=20*this.barwide;
            downFillet.rotateZ(Math.PI);
            this.long_bar=bar;
            this.longhalfcircle=upFillet;
            groupbar.add(this.long_bar);
            groupbar.add(upFillet);
            groupbar.add(downFillet);
            groupbar.position.set(0,0,-this.barwide/4);
            groupbar.rotateZ(-Math.PI/2);
            this.scene.add(groupbar);
            this.longbar = groupbar;
        },
        drawBarGeometry(l)
        {
            var geometry=new THREE.Shape();
            var x=0.5*this.barwide;
            geometry.moveTo(x,0);
            geometry.lineTo(x,l);
            geometry.lineTo(-x,l);
            geometry.lineTo(-x,0);
            geometry.lineTo(x,0);
            var stretched=new THREE.ExtrudeGeometry(geometry,this.extrudeSettings);
            var meshed=new THREE.Mesh(stretched,this.Addwoodtexture());
            return meshed;
        },
        DrawFillet(r)
        {
            var pointslist=[];
            var geometry=new THREE.Shape();
            var i=0;
            while(i<=Math.PI)
            {
                pointslist.push(new THREE.Vector2(r*Math.cos(i),r*Math.sin(i)));
                i+=0.1;
            }
            geometry.setFromPoints(pointslist);
            geometry.lineTo(r,0);
            var stretched=new THREE.ExtrudeGeometry(geometry,this.extrudeSettings);
            var meshed=new THREE.Mesh(stretched,this.Addwoodtexture());
            return meshed;
        },
        
        Addwoodtexture()
        {
            var floorMat = new THREE.MeshStandardMaterial( {
                roughness: 0.8,
                color: 0xffffff,
                metalness: 0.2,
                bumpScale: 0.0005
            } );
            var textureLoader = new THREE.TextureLoader();
            textureLoader.load( "../../static/images/woodtexture.jpg", function ( map ) {
                map.wrapS = THREE.RepeatWrapping;
                map.wrapT = THREE.RepeatWrapping;
                map.anisotropy = 4;
                map.repeat.set( 0.1, 0.1 );
                floorMat.map = map;
                floorMat.needsUpdate = true;
            } );
            return floorMat;
        },
        AddLine()
        {
            var material = new THREE.LineDashedMaterial({
                color:0xa0adb5,
                dashSize:1,
                gapSize:2
            })
            var geometry = new THREE.Geometry();
            geometry.vertices.push(new THREE.Vector3(-10*this.barwide,0,0));
            geometry.vertices.push(new THREE.Vector3(50*this.barwide,0,0));
            var line=new THREE.Line(geometry,material);
            line.computeLineDistances();
            this.scene.add(line);
        },
        Addswingblock(x,y,z)
        {
            var geometry = new THREE.CubeGeometry(5*this.barwide,2*this.barwide,3/2*this.barwide);
            var material = new THREE.MeshNormalMaterial(
                {
                    opacity:0.5,
                    transparent:true,
                }
            )
            var mesh = new THREE.Mesh(geometry,material);
            this.scene.add(mesh);
            mesh.position.set(x,y,z);
            return mesh;
        },
        animate() 
        {   
            this.shortbar.rotateZ(this.controls.speed);
            this.angleA+=this.controls.speed;
            if(this.angleA > 2*Math.PI)this.angleA-=2*Math.PI;
            if(this.angleA < 0)this.angleA+=2*Math.PI;
            var x0=0,y0=this.controls.e;
            var x1=x0+this.controls.a*Math.cos(this.angleA);
            var y1=y0+this.controls.a*Math.sin(this.angleA);
            var x2=x1+Math.sqrt(this.controls.b*this.controls.b-y1*y1),y2=0;
            var angleBB=Math.acos((x2-x1)/Math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1)));
            if(y2<y1)angleBB=-angleBB;
            this.xlist.push(x2);
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
            if(this.alist.length>0)
            {
                this.myChart.setOption(this.setEcharts(this.xlist,'#dd0d29','从动件位移'));
                this.myChart1.setOption(this.setEcharts(this.vlist,'#0e4bef','从动件速度'));
                this.myChart2.setOption(this.setEcharts(this.alist,'#0b9909','从动件加速度'));
            }
            this.short_bar.scale.y=this.controls.a/10;
            this.shorthalfcircle.position.set(0,this.controls.a,0);
            this.shortbar.position.set(x0,y0,this.barwide/4)
            this.swingblock.position.set(x2,y2,0);
            this.longbar.position.set(x1,y1,-this.barwide/4);
            this.long_bar.scale.y=this.controls.b/20;
            this.longhalfcircle.position.set(0,this.controls.b,0);
            this.longbar.rotateZ(angleBB-this.angleB);
            this.angleB=angleBB;
            this.renderer.render( this.scene, this.camera );
        },
        Gui()
        {
            this.controls=
            {
                speed:0,
                e:5*this.barwide,
                a:10*this.barwide,
                b:20*this.barwide,
            }
            var gui=new dat.GUI();
            //LongestPole为长度
            gui.add(this.controls,'e',-5*this.barwide,5*this.barwide).name("偏心距");
            gui.add(this.controls,'a',0,15*this.barwide).name("原动件长度");
            gui.add(this.controls,'b',20*this.barwide,30*this.barwide).name("连杆长度");
            gui.add(this.controls,'speed',-0.1,0.1).name("原动件角速度");
        },
        //speedFar 最大的圆自转速度 speedMiddle 最小圆转速 omegaH 公转速度 omega2 自转速度
        Topage(path)
        {
            this.$router.push(path);
        },
        AddSkyBox()
        {
            this.skybox=new THREE.BoxBufferGeometry(5000,5000,5000);
            for(var i=0;i<=5;i++)
            {
                this.SixSidesOfBox[i]=this.setpath+this.SixSidesOfBox[i]+this.format;
            }
            for(i=0;i<=5;i++)
            {
                this.skyboxTexture[i]=new THREE.MeshBasicMaterial
                ({map:new THREE.TextureLoader().load(this.SixSidesOfBox[i]),side:THREE.BackSide});
            }
            this.skyboxmeshed=new THREE.Mesh(this.skybox,this.skyboxTexture);
            this.skyboxmeshed.position.x=0;
            this.skyboxmeshed.position.y=0;
            this.skyboxmeshed.position.z=0;
            this.scene.add(this.skyboxmeshed);
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