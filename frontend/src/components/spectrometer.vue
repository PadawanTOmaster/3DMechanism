<template>
<div>
    <el-row >
        <div style="top:15px;left:15px;z-index:1000;position:absolute;opacity:0.8;">
            <el-button type="success" round @click="Topage('/threed')">返回</el-button>
            <!-- <el-button @click="show1=!show1" type="success" round>看图</el-button>
            <el-button @click="show2=!show2" type="success" round>看讲解</el-button> -->
        </div>
    </el-row>

    <div style="z-index:1000;position:absolute;left:50px;top:80px;color:white;font-weight:bold;
    text-align:left;width:300px">
        <span class="demonstration">望远镜旋转角度(°) 从-150°到150°</span>
        <el-slider v-model="rotationAngle" :max=maxAngle :min=minAngle></el-slider>
        <div style="height:50px;"></div>
        <span>添加平面镜&emsp;</span>
        <el-switch
            v-model="valuePlaneMirror"
            active-color="#13ce66"
            inactive-color="#dcdddb"
            @change="switchForPlaneMirror"
            >
        </el-switch>
        <br><br>
        <span class="demonstration" v-if="valuePlaneMirror==true">平面镜旋转角度(°) 从0°到360°</span>
        <el-slider v-model="planeMirrorCurrentAngle" :max=planeMirrorMax :min=planeMirrorMin v-if="valuePlaneMirror==true" @input="modifyPlaneMirrorAngle"></el-slider>
        <br><br>
        <span>添加三棱镜&emsp;</span>
        <el-switch
            v-model="valuePrism"
            active-color="#13ce66"
            inactive-color="#dcdddb"
            @change="switchForPrism"
            >
        </el-switch>
        <br><br>
        <span>开启钠光灯&emsp;</span>
        <el-switch
            v-model="valueLamp"
            active-color="#13ce66"
            inactive-color="#dcdddb"
            @change="switchForLamp"
            >
        </el-switch>
    </div>

    <div style="z-index:1000;position:absolute;right:100px;color:white;font-weight:bold;
    text-align:right;width:300px">
        <img v-if="valuePlaneMirror==true" style="width:400px;" src="../../static/images/reticle.png"/>
    </div>
    <div :style="greenCrossStyle+staticStyle">
        <img v-if="valuePlaneMirror==true && hasGreenCross==true" style="width:80px;" src="../../static/images/greencross.png"/>
    </div>
    <div id="webGL_container" style="position:absolute;z-index:0">
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
import {STLLoader} from 'three/examples/jsm/loaders/STLLoader.js'
import { Vector3 } from 'three'

export default {

    data(){
        return{
            scene:null,
            camera:null,
            renderer:null,
            axis:null,
            rotationAngle:0,
            maxAngle:150,
            minAngle:-150,
            eyepieceSet:null,
            eyepiece:null,
            set:null,
            collimator:null,
            eyepiecePotGroup:null,
            rotationInit:0,
            planemirror:null,
            valuePlaneMirror:false,
            planeMirrorMin:0,
            planeMirrorMax:360,
            planeMirrorCurrentAngle:0,
            marks:{
                0:'0°',
                360:'360°'
            },
            initPlaneMirrorAngle:0,
            planePoints:[],
            normalVector:null,
            planePoints2:[],
            planePoints3:[],
            hasGreenCross:true,
            staticStyle:"z-index:2000;position:absolute;top:60px;color:white;font-weight:bold;text-align:right;width:300px",
            greenCrossStyle:"right:294px;",
            valuePrism:false,
            valueLamp:false,
            prism:null,
            lamp:null
            }
        },
    methods:{
        
        init()
        {
            this.AddScene();
            this.AddCamera();
            this.AddRender();
            this.AddListener();
            this.AddOrbitControls();
            //this.AddAxis();
            this.AddModel();
            this.Addfloor();
            this.Addlight();
            this.animate();
        },
         
        AddScene()
        {
            this.scene=new THREE.Scene();
        },

        AddCamera()
        {
            this.camera=new THREE.PerspectiveCamera( 50, window.innerWidth/window.innerHeight,0.1,10000);
            this.camera.position.x=200;
            this.camera.position.y=200;
            this.camera.position.z=500;//40 40 40 //0 150 400
            this.camera.lookAt(0,-200,-200);
        },

        AddRender()
        {
            this.renderer=new THREE.WebGLRenderer({antialias : true});
            this.renderer.setClearColor(0x000000);
            this.renderer.setSize(window.innerWidth,window.innerHeight);
            document.getElementById("webGL_container").appendChild(this.renderer.domElement)
        },

        AddListener(){
            
            window.addEventListener( 'resize', ()=>{
                this.camera.aspect = window.innerWidth / window.innerHeight;
                this.camera.updateProjectionMatrix();
                this.renderer.setSize( window.innerWidth, window.innerHeight ); 
            }, false );
        },

        AddOrbitControls(){
            var OrbitControls = require('three-orbit-controls')(THREE);
            var obcontrol = new OrbitControls(this.camera,this.renderer.domElement);
        },
        AddLocatingSpot(){
            //本函数用来添加定位点
            var geometry1=new THREE.SphereGeometry(5,5,5);
            var material1 = new THREE.MeshBasicMaterial({color:0xB3DD,opacity:0,transparent:true});
            var mesh1 = new THREE.Mesh(geometry1,material1);
            this.scene.add(mesh1);
            mesh1.position.copy(this.set.position);
            mesh1.position.x -= 238;
            mesh1.position.y -=105;
            mesh1.name = 'spot1';

            var geometry3=new THREE.SphereGeometry(5,5,5);
            var material3 = new THREE.MeshBasicMaterial({color:0xB3DD,opacity:0,transparent:true});
            var mesh3 = new THREE.Mesh(geometry3,material3);
            this.scene.add(mesh3);
            mesh3.position.copy(mesh1.position);
            mesh3.position.x += 800;
            mesh3.name = 'spot3';

            // var material = new THREE.LineDashedMaterial({color:0xb91913});
            // var geometry = new THREE.Geometry();
            // geometry.vertices.push(mesh1.position);
            // geometry.vertices.push(mesh3.position);
            // var line = new THREE.Line(geometry, material);
            // this.scene.add(line);

        },
        AddModel(){
            var x = 150;
            var z = -100;
            //4个模型都向左挪150,向后挪-100
            var loader = new STLLoader();
            //望远镜架
            loader.load('../../static/models/eyepiece_holder.stl',(geometry)=>{
                var material = new THREE.MeshPhongMaterial( { color: 0xbebdc5,opacity:0.5,transparent:true} );
                this.eyepieceSet = new THREE.Mesh( geometry, material );
                this.eyepieceSet.position.set(x-240,-238,z);
                this.eyepieceSet.rotation.x = -Math.PI/2
                this.eyepieceSet.rotation.z = Math.PI/2;
                this.eyepieceSet.scale.set(5,5,5);
                this.eyepieceSet.name = 'eyepieceSet';
                this.scene.add(this.eyepieceSet);
            })
            /****************************************/
            var loader = new STLLoader();
            //望远镜
            loader.load('../../static/models/eyepiece.stl',(geometry)=>{
                var material = new THREE.MeshPhongMaterial( { color: 0xbebdc5,opacity:0.5,transparent:true} );
                this.eyepiece = new THREE.Mesh( geometry, material );
                this.eyepiece.scale.set(5,5,5);
                this.eyepiece.name = 'eyepiece';  

                var geometry2=new THREE.SphereGeometry(5,5,5);
                var material2 = new THREE.MeshBasicMaterial({color:0xB3DD,opacity:0,transparent:true});
                var mesh2 = new THREE.Mesh(geometry2,material2);
                mesh2.position.y += 500;
                mesh2.position.z +=135;
                mesh2.name = 'spot2';
                
                //在望远镜小灯泡和物镜处放置2平面
                //mesh3 小灯泡处平面
                //mesh4 物镜处平面
                var material = new THREE.MeshPhongMaterial({
                    color: 0xad4fde,
                    side: THREE.DoubleSide,
                    opacity:0,
                    transparent:true
                });
                var plane1 = new THREE.PlaneGeometry(10,10);
                var plane2 = new THREE.PlaneGeometry(10,10);
                var mesh3 = new THREE.Mesh(plane1, material);
                var mesh4 = new THREE.Mesh(plane2, material);
                mesh3.name = 'plane1';
                mesh4.name = 'plane2';
                
                mesh3.rotation.x = Math.PI/2;
                mesh3.position.y += 195;
                mesh3.position.z +=135;
                
                mesh4.rotation.x = Math.PI/2;
                mesh4.position.y += 48;
                mesh4.position.z +=135;
                mesh3.updateMatrix();
                mesh4.updateMatrix();

                //在两平面各添加一点
                //mesh5 灯泡处点
                //mesh6 目镜处点
                var material1 = new THREE.MeshBasicMaterial({color:0xB3DD});
                var spot5 = new THREE.SphereGeometry(2,2,2);
                var mesh5 = new THREE.Mesh(spot5,material1);
                mesh5.position.y += 195;
                mesh5.position.z +=130;
                mesh5.name = 'spot5';

                var spot6 = new THREE.SphereGeometry(2,2,2);
                var mesh6 = new THREE.Mesh(spot6,material1);
                mesh6.position.y += 48;
                mesh6.position.z +=133;
                mesh6.name = 'spot6';


                this.eyepiecePotGroup = new THREE.Group();
                this.eyepiecePotGroup.add(mesh2);
                this.eyepiecePotGroup.add(mesh3);
                this.eyepiecePotGroup.add(mesh4);
                this.eyepiecePotGroup.add(mesh5);
                this.eyepiecePotGroup.add(mesh6);

                this.eyepiecePotGroup.add(this.eyepiece);
                this.eyepiecePotGroup.rotation.set(-Math.PI/2,0,Math.PI/2);
                this.eyepiecePotGroup.position.set(x-240,-238,z);
                
                this.scene.add(this.eyepiecePotGroup);
                
            })
            /****************************************/
            var loader = new STLLoader();
            loader.load('../../static/models/set.stl',(geometry)=>{
                var material = new THREE.MeshPhongMaterial( { color: 0xbebdc5,opacity:0.5,transparent:true} );
                this.set = new THREE.Mesh( geometry, material );
                this.set.position.set(x,0,z);
                this.set.rotation.x = -Math.PI/2;
                this.set.rotation.z = Math.PI/2;
                this.set.scale.set(5,5,5);
                this.scene.add(this.set);
                this.AddLocatingSpot();
            })
            /****************************************/
            var loader = new STLLoader();
            //平行光管
            loader.load('../../static/models/collimator.stl',(geometry)=>{
                var material = new THREE.MeshPhongMaterial( { color: 0xbebdc5,opacity:0.5,transparent:true} );
                this.collimator = new THREE.Mesh( geometry, material );
                this.collimator.position.set(x,0,z);
                this.collimator.rotation.x = -Math.PI/2;
                this.collimator.rotation.z = Math.PI/2;
                this.collimator.scale.set(5,5,5);
                this.scene.add(this.collimator);
            })
            /****************************************/
            var loader = new STLLoader();
            //钠光灯
            loader.load('../../static/models/lamp.stl',(geometry)=>{
                var material = new THREE.MeshPhongMaterial( { color: 0x7ab8cc,opacity:0.8,transparent:true} );
                this.lamp = new THREE.Mesh( geometry, material );
                this.lamp.name = 'lamp';
                this.lamp.position.set(x+30,-300,z);
                this.lamp.rotation.x = -Math.PI/2;
                this.lamp.rotation.z = Math.PI;
                this.lamp.scale.set(5,5,7);
                this.scene.add(this.lamp);
            })
            
        },
        switchForPrism(){
            if(this.valuePrism==true){
                this.valuePlaneMirror=false;
                if(this.scene.getObjectByName('planemirror')!=undefined){
                    this.scene.remove(this.scene.getObjectByName('planemirror'));
                    this.scene.remove(this.scene.getObjectByName('plane_on_mirror'));
                    this.scene.remove(this.scene.getObjectByName('intersection'));
                    this.scene.remove(this.scene.getObjectByName('line2'));
                    this.scene.remove(this.scene.getObjectByName('line3'));
                    this.scene.remove(this.scene.getObjectByName('line4'));
                }
                this.AddPrism();
            }
            else{
                this.scene.remove(this.scene.getObjectByName('prism'));
            }
        },
        AddPrism(){
            var x = 150;
            var z = -100;
            var loader = new STLLoader();
            loader.load('../../static/models/prism.stl',(geometry)=>{
                var material = new THREE.MeshPhongMaterial( { color: 0xffaaaa,opacity:0.8,transparent:true} );
                this.prism = new THREE.Mesh( geometry, material );
                this.prism.position.set(x-240,-130,z);
                this.prism.rotation.x = -Math.PI/2;
                this.prism.rotation.z = -Math.PI/6;
                //让它以z轴旋转
                this.prism.scale.set(0.5,0.5,0.5);
                this.prism.name = 'prism';
                this.scene.add(this.prism);
            })
        },
        switchForLamp(){
            if(this.valueLamp==true){
                var geometry1=new THREE.SphereGeometry(5,5,5);
                var material1 = new THREE.MeshBasicMaterial({color:0xB3DD});
                var mesh1 = new THREE.Mesh(geometry1,material1);
                this.scene.add(mesh1);
                mesh1.name = 'smallspot';
                mesh1.position.set(180,-100,-100);
                

                var bulblight=new THREE.PointLight(0x66ffe6,1,800,2);
                bulblight.position.set(180,-100,-100);
                bulblight.name = 'bulb';
                this.scene.add(bulblight);
            }
            else{
                this.scene.remove(this.scene.getObjectByName('bulb'));
                this.scene.remove(this.scene.getObjectByName('smallspot'));

            }
            
        },
        switchForPlaneMirror(){
            if(this.valuePlaneMirror==true){
                this.valuePrism=false;
                if(this.scene.getObjectByName('prism')!=undefined){
                    this.scene.remove(this.scene.getObjectByName('prism'))
                }
                this.AddPlaneMirror();//加平面镜 平面镜上平面
                this.GetPlanePoints();
                this.AddRay();//加射线 加反射点
                this.AddReflectRay();//由反射点等 加蓝色反射光线
            }
            else if(this.valuePlaneMirror==false && this.scene.getObjectByName('planemirror')!=undefined){
                this.scene.remove(this.scene.getObjectByName('planemirror'));
                this.scene.remove(this.scene.getObjectByName('plane_on_mirror'));
                this.scene.remove(this.scene.getObjectByName('intersection'));
                this.scene.remove(this.scene.getObjectByName('line2'));
                this.scene.remove(this.scene.getObjectByName('line3'));
                this.scene.remove(this.scene.getObjectByName('line4'));
            }
        },
        AddPlaneMirror(){
            this.initPlaneMirrorAngle = Math.floor(Math.random()*360)*Math.PI/180;
            var x = 150;
            var z = -100;
            var loader = new STLLoader();
            loader.load('../../static/models/planemirror.stl',(geometry)=>{
                var material = new THREE.MeshPhongMaterial( { color: 0x31639c,opacity:0.8,transparent:true} );
                this.planemirror = new THREE.Mesh( geometry, material );
                this.planemirror.position.set(x-240,-138,z);
                this.planemirror.rotation.x = -Math.PI/2;
                this.planemirror.rotation.z = this.initPlaneMirrorAngle;
                //让它以z轴旋转
                this.planemirror.scale.set(5,5,5);
                this.planemirror.name = 'planemirror';
                this.scene.add(this.planemirror);
            })
            //平面镜上加平面
            var material1 = new THREE.MeshPhongMaterial({
                color: 0xad4fde,
                side: THREE.DoubleSide,
                opacity:0,
                transparent:true
            });
            var plane = new THREE.PlaneGeometry(10,20);
            var mesh = new THREE.Mesh(plane, material1);
            mesh.position.set(x-236,-138,z)
            mesh.name = 'plane_on_mirror';
            mesh.rotation.y = this.initPlaneMirrorAngle+Math.PI/2;
            mesh.updateMatrix();

            this.scene.add(mesh);
        },
        modifyPlaneMirrorAngle(){
            if(this.scene.getObjectByName('planemirror')!=undefined){
                this.scene.getObjectByName('planemirror').rotation.z=this.planeMirrorCurrentAngle*Math.PI/180+this.initPlaneMirrorAngle;
                this.scene.getObjectByName('plane_on_mirror').rotation.y=this.planeMirrorCurrentAngle*Math.PI/180+this.initPlaneMirrorAngle+Math.PI/2;
                this.scene.getObjectByName('plane_on_mirror').updateMatrix();
                this.GetPlanePoints();
                this.AddRay();//加射线 加反射点
                this.AddReflectRay();//由反射点等 加蓝色反射光线
            }
        },
        AddIntersectionOnPlaneMirror(target){
            //加反射点
            if(this.scene.getObjectByName('intersection')!=undefined){
                this.scene.remove(this.scene.getObjectByName('intersection'));
            }
            var geometry=new THREE.SphereGeometry(2,2,2);
            var material = new THREE.MeshBasicMaterial({color:0xB3DD});
            var mesh = new THREE.Mesh(geometry,material);
            mesh.name = 'intersection';
            this.scene.add(mesh);
            mesh.position.copy(target);
        },

        AddRay(){
            //射线
            var p1 = new THREE.Vector3(0,0,0);
            this.scene.getObjectByName('spot6').getWorldPosition(p1);
            var p2 = new THREE.Vector3(0,0,0);
            this.scene.getObjectByName('spot5').getWorldPosition(p2);
            var direction = new THREE.Vector3(p1.x-p2.x,p1.y-p2.y,p1.z-p2.z).normalize();
            var ray = new THREE.Ray(p2,direction);
            var plane = new THREE.Plane();
            plane.setFromCoplanarPoints(this.planePoints[0], this.planePoints[1], this.planePoints[2]);
            this.normalVector = plane.normal;
            var target = new THREE.Vector3(0,0,0);
            ray.intersectPlane(plane,target);
            //加反射点
            this.AddIntersectionOnPlaneMirror(target);    
        },
        GetPlanePoints(){
            this.planePoints=[];
            for(var i=0;i<this.scene.getObjectByName('plane_on_mirror').geometry.vertices.length;i++){
                var vector = new THREE.Vector3();
                vector.copy(this.scene.getObjectByName('plane_on_mirror').geometry.vertices[i]);
                vector.applyMatrix4(this.scene.getObjectByName('plane_on_mirror').matrix);
                this.planePoints.push(vector);
            }
        },
        AddReflectRay(){
            if(this.scene.getObjectByName('line2')!=undefined){
                this.scene.remove(this.scene.getObjectByName('line2'))
            }
            if(this.scene.getObjectByName('line3')!=undefined){
                this.scene.remove(this.scene.getObjectByName('line3'))
            }
            if(this.scene.getObjectByName('line4')!=undefined){
                this.scene.remove(this.scene.getObjectByName('line4'))
            }
            //加蓝色反射光线
            var material1 = new THREE.LineDashedMaterial({color:0xe71837,linewidth:5});
            var points = [];
            var p1 = new THREE.Vector3(0,0,0);
            this.scene.getObjectByName('spot5').getWorldPosition(p1);
            points.push(p1);
            points.push(this.scene.getObjectByName('intersection').position);
            var geometry1 = new THREE.BufferGeometry().setFromPoints( points );
            var line2 = new THREE.Line(geometry1, material1);
            line2.name = 'line2';
            this.scene.add(line2);

            var incidentRayPoint = p1;
            var e = incidentRayPoint.x;
            var f = incidentRayPoint.y;
            var g = incidentRayPoint.z;
            var pointOfIncidence = this.scene.getObjectByName('intersection').position;
            var h = pointOfIncidence.x;
            var i = pointOfIncidence.y;
            var j = pointOfIncidence.z;

            var a = this.normalVector.x*100+h;
            var b = this.normalVector.y*100+i;
            var c = this.normalVector.z*100+j;

            //孙宇飞
            var l = (e-h)*(e-h)+(f-i)*(f-i)+(g-j)*(g-j)
            var x = (h-a)*(l+2*Math.pow(e-h,2))-2*(e-h)*(i-b)*(i-f)-2*(e-h)*(j-c)*(j-g);
            var y = -2*(h-a)*(f-i)*(h-e)+(i-b)*(l+2*Math.pow(f-i,2))-2*(f-i)*(j-c)*(j-g);
            var z = -2*(h-a)*(g-j)*(h-e)-2*(i-b)*(g-j)*(i-f)+(j-c)*(l+2*Math.pow(g-j,2)); 

            //李侃
            // var x = 2*h-e-2*((a*(h-e)+b*(i-f)+c*(j-g))/(a*a+b*b+c*c))*a;
            // var y = 2*i-f-2*((a*(h-e)+b*(i-f)+c*(j-g))/(a*a+b*b+c*c))*b;
            // var z = 2*j-g-2*((a*(h-e)+b*(i-f)+c*(j-g))/(a*a+b*b+c*c))*c;

            var plane = new THREE.Plane();
            plane.setFromCoplanarPoints(this.planePoints2[0], this.planePoints2[1], this.planePoints2[2]);
            var direction1 = new THREE.Vector3(x-h,y-i,z-j).normalize();
            var ray1 = new THREE.Ray(new THREE.Vector3(h,i,j),direction1);
            var direction2 = new THREE.Vector3(h-x,i-y,j-z).normalize();
            var ray2 = new THREE.Ray(new THREE.Vector3(h,i,j),direction2);
            //从反射点开始向前 向后各一条射线
            var t1 = new THREE.Vector3(0,0,0);
            ray1.intersectPlane(plane,t1);
            var t2 = new THREE.Vector3(0,0,0);
            ray2.intersectPlane(plane,t2);
            var target = (t1.x==0 && t1.y==0 && t1.z==0)?t2:t1;
            //target这个点是反射光线与目镜的交点。
            if(target!=new THREE.Vector3(0,0,0)){
                var points = [];
                points.push(new THREE.Vector3(h,i,j));
                points.push(target);
                var geometry1 = new THREE.BufferGeometry().setFromPoints( points );
                var line3 = new THREE.Line(geometry1, material1);
                line3.name = 'line3';
                this.scene.add(line3); 
                //line3为反射光线
            }
            
            // if(target!=null){
            //     var points = [];
            //     points.push(new THREE.Vector3(h,i,j));
            //     points.push(target);
            //     var geometry1 = new THREE.BufferGeometry().setFromPoints( points );
            //     var line3 = new THREE.Line(geometry1, material1);
            //     line3.name = 'line3';
            //     this.scene.add(line3); 
            // }
            
            var plane1 = new THREE.Plane();
            plane1.setFromCoplanarPoints(this.planePoints3[0], this.planePoints3[1], this.planePoints3[2]);
            var direction = plane1.normal;
            var ray1 = new THREE.Ray(target,direction);
            var target1 = new THREE.Vector3(0,0,0);
            ray1.intersectPlane(plane1,target1);
            if(target1!=null){
                //target1是分划板反射光
                //p2是分划板灯泡光
                var points = [];
                points.push(target);
                points.push(target1);
                var geometry1 = new THREE.BufferGeometry().setFromPoints( points );
                var line4 = new THREE.Line(geometry1, material1);
                line4.name = 'line4';
                this.scene.add(line4); 
                var p2 = new THREE.Vector3(0,0,0);
                this.scene.getObjectByName('spot5').getWorldPosition(p2);
                this.greenCrossStyle = "right:"+((p2.z-target1.z+11)*12.45+20)+"px;";
                if((p2.z-target1.z+11)*12.45+20>294 || (p2.z-target1.z+11)*12.45+20<20){
                    this.hasGreenCross=false;
                }
                else{
                    this.hasGreenCross=true;
                }
            }
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
            var floorMat = new THREE.MeshPhongMaterial( {
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
        
        Addlight()
        {
            var bulblight1=new THREE.PointLight( 0xeee8aa);
            bulblight1.position.set(-1000,-200,400);
            this.scene.add(bulblight1);
            
            // var bulblight2=new THREE.PointLight(0xeee8aa);
            // bulblight2.position.set(-1000,-200,-400);
            // this.scene.add(bulblight2);

            var bulblight3=new THREE.PointLight( 0xeee8aa);
            bulblight3.position.set(1000,-200,400);
            this.scene.add(bulblight3);
            
            // var bulblight4=new THREE.PointLight(0xeee8aa);
            // bulblight4.position.set(1000,-200,-400);
            // this.scene.add(bulblight4);

        },
         
        AddAxis()
        {
            //x红 z蓝 y绿
            this.axis=new THREE.AxesHelper(200);
            this.scene.add(this.axis);
        },
        

        animate() 
        {   
            if(this.scene.getObjectByName('eyepieceSet')!=undefined && this.scene.getObjectByName('spot1')!=undefined && this.eyepiecePotGroup!=null){
                this.eyepieceSet.rotation.z=Math.PI/2+this.rotationAngle*Math.PI/180;
                this.eyepiecePotGroup.rotation.z=Math.PI/2+this.rotationAngle*Math.PI/180; 
                this.scene.getObjectByName('plane2').updateMatrix();
                this.scene.getObjectByName('plane1').updateMatrix();
                if(this.eyepiecePotGroup.rotation.z!=this.rotationInit){
                    this.planePoints2=[];
                    for(var i=0;i<this.scene.getObjectByName('plane2').geometry.vertices.length;i++){
                        var vector = this.scene.getObjectByName('plane2').geometry.vertices[i].clone();
                        vector.applyMatrix4(this.scene.getObjectByName('plane2').matrixWorld);
                        this.planePoints2.push(vector);
                    }
                    this.planePoints3=[];
                    for(var i=0;i<this.scene.getObjectByName('plane1').geometry.vertices.length;i++){
                        var vector = this.scene.getObjectByName('plane1').geometry.vertices[i].clone();
                        vector.applyMatrix4(this.scene.getObjectByName('plane1').matrixWorld);
                        this.planePoints3.push(vector);
                    }
                    //红线
                    // var material = new THREE.LineDashedMaterial({color:0xb91913});
                    // var geometry = new THREE.Geometry();
                    // geometry.vertices.push(this.scene.getObjectByName('spot2').matrixWorld.getPosition());
                    // geometry.vertices.push(this.scene.getObjectByName('spot1').position);
                    // var line = new THREE.Line(geometry, material);
                    // line.name = 'line1';
                    // this.scene.remove(this.scene.getObjectByName('line1'));
                    // this.scene.add(line);

                    if(this.scene.getObjectByName('plane_on_mirror')!=undefined){
                        //如果转动望远镜 射线也要重新添加
                        this.AddRay();//加射线 加反射点
                        this.AddReflectRay();//由反射点等 加蓝色反射光线 
                    }
                   
                    this.rotationInit = this.eyepiecePotGroup.rotation.z;
                }
                
                
            }
            
            this.renderer.render( this.scene, this.camera );
            requestAnimationFrame(this.animate);
        },
        
        AddGui()
        {
           
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