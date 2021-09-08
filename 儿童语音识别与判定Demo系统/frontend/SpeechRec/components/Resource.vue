<template>
	<view class="container">
		<view class="header">
			<view class="left" @tap="onClick">
				<text class="title">{{item.title}}</text>
				<image v-if="item.visitCtrl == 0" src="../static/component/resource/lock.png" mode="aspectFit"></image>
				<view class="profession">{{item.professionName}}</view>
			</view>
			<view class="right">
				<view v-if="showScore">评分：{{item.avgScore}}</view>
				<image v-if="store" src="../static/component/resource/is_store.png" mode="aspectFit" @click="cancelStoreResource"></image>
				<!--
				<image v-if="cancelStore" src="../static/component/resource/cancel_store.png" mode="aspectFit"></image>
				-->
				<image v-if="cancelUpload" src="../static/component/resource/delete.png" mode="aspectFit" @click="cancelUploadResource"></image>
			</view>
		</view>
		
		<text class="intro" @tap="onClick">
			{{item.intro}}
		</text>
		
		<view v-if="isDetail" class="download">
			<view class="left" >
				<image src="../static/component/resource/download.png" mode="aspectFit"></image>
				<uni-link class="link" :href="item.webUrl" :text="item.fileSize" :ResourceID="item.ResourceID"></uni-link>
			</view>
			<view class="right">
				<view>上传者：{{item.uploaderNickName}}
				</view>
				<view>下载次数：{{item.downloadCount}}</view>
			</view>
		</view>
		
		<ResourceFooter v-bind:isDetail="isDetail" :item="item"></ResourceFooter>
	</view>
</template>

<script>
	export default {
		data() {
			return {
			};
		},
		props:{
			showScore: {
				type: Boolean,
				default: true
			},
			store: {
				type: Boolean,
				default: false
			},
			cancelUpload: {
				type: Boolean,
				default: false
			},
			isPrivate: {
				type: Boolean,
				default: false
			},
			isDetail: {
				type: Boolean,
				default: false
			},
			item: {
				type: Object,
				default(){
					return{}	
				}
			},		
		},
		methods:{
			onClick:function(){
				getApp().checkLoginStatus()
				let current_userinfo = null
				try{
					current_userinfo = uni.getStorageSync('userInfo')
					if(current_userinfo == 'empty' || current_userinfo.length == 0 || !current_userinfo)
						return		
				}catch(e){
					//console.log(e)
				}
				if(!this.isDetail){
					//console.log(current_userinfo.role)
					if(current_userinfo.role < 2 && this.item.visitCtrl == 0){
						getApp().errorToast("查看校内资源请先认证")
						return
					}
					//console.log("navigate to resourceDetail")	
					this.addVisitCount()
					uni.navigateTo({
						url:'/pages/resourceDetail/resourceDetail?ResourceID=' + this.item.ResourceID +'&UserID=' + current_userinfo.UserID
					})
				}
				//this.$emit('Click');
			},
			add:function(){
				var that = this
				uni.request({
					url: getApp().globalData.rootUrl + 'resource/addResourceVisit',
					data: {
						ResourceID: that.item.ResourceID,			
					},			
					method:'POST',
					header:{
						'content-type': 'application/x-www-form-urlencoded'
					},
					success: (res) => {
						//console.log(res.data)
					},
					fail: (res) => {
						//getApp().requestFailToast()
					}
				})
			},
			addVisitCount:function(){
				try{
					var resource_stamp = uni.getStorageSync('ResourceID_' + this.item.ResourceID.toString())		
					var current_stamp = getApp().getCurrentSecond()	
					uni.setStorageSync('ResourceID_' + this.item.ResourceID.toString(), current_stamp)
					var diff = current_stamp - resource_stamp
					if(diff > 3600 * 24){
						this.add()
					}	
				}catch(e){
					//console.log(e)
					var current_stamp = getApp().getCurrentSecond()
					//console.log(current_stamp.toString())
					uni.setStorageSync('ResourceID_' + this.item.ResourceID.toString(), current_stamp)
					this.add()
				}			
			},
			cancelUploadResource:function(){
				var that = this
				uni.showModal({
					showCancel: true,
					title: '确定删除该条资源？',
					success: (res) =>  {
						if(res.confirm){
							uni.request({
								url: getApp().globalData.rootUrl + 'user/cancelUploadResource',
								data: {
									ResourceID: that.item.ResourceID,			
								},			
								method:'POST',
								header:{
									'content-type': 'application/x-www-form-urlencoded'
								},
								success: (res) => {
									if(res.data.code)
										getApp().errorToast(res.data.msg)
									else{
										getApp().successToast("删除成功")
										uni.$emit('refreshMyUpload');
									}
								},
								fail: (res) => {
									getApp().requestFailToast()
								}
							})
						}
					},
				})		
			},
			cancelStoreResource:function(){
				var that = this
				uni.showModal({
					showCancel: true,
					title: '确定取消收藏？',
					success: (res) =>  {
						if(res.confirm){
							uni.request({
								url: getApp().globalData.rootUrl + 'user/cancelStoreResource',
								data: {
									StoreID: that.item.StoreID,			
								},			
								method:'POST',
								header:{
									'content-type': 'application/x-www-form-urlencoded'
								},
								success: (res) => {
									if(res.data.code)
										getApp().errorToast(res.data.msg)
									else{
										getApp().successToast("取消收藏成功")
										uni.$emit('refreshMyFavor');
									}
								},
								fail: (res) => {
									getApp().requestFailToast()
								}
							})
						}
					}
				})		
			},
		}
	}
</script>

<style>
	.container{
		/*border: #000000 solid 2px;*/
		padding-top: 5px;
		width: 100%;
		/*height: 95px;*/
		display: flex;
		flex-direction: column;
		justify-content: space-between;
	}
	/* #ifdef MP-WEIXIN */
	.container{
		border-bottom: #D3D3D3 solid 2px;
	}
	/* #endif */
	.container .header{
		width: 100%;
		height:35px;
		/*border: #000000 solid 2px;*/
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		align-items: flex-end;
	}
	.container .header .left{
		width: 75%;
		height:100%;
		/*border: #000000 solid 2px;*/
		display: flex;
		flex-direction: row;
		align-items: center;
		justify-content: left;
	}	
	.container .header .left image{
		width:40rpx;
		height:100%;
		margin-left: 5rpx;
	}
	.container .header .left .title{
		height: 100%;
		max-width: 70%;
		width:auto;
		overflow: hidden;
		font-size: 105%;
		font-weight: bold;
		margin-left: 6rpx;
		display: flex;
		align-items: center;
		justify-content: left;
		/*border: #000000 solid 2rpx;*/
	}
	.container .header .left .profession{
		margin-left: 5rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: small;
		margin-left: 6rpx;
		border: #BBBBBB solid 5rpx;
		border-radius: 20rpx 20rpx 20rpx 20rpx;
		padding: 5rpx;
		padding-left: 10rpx;
		padding-right: 10rpx;
		font-size: 85%;
	}
	@media only screen and (min-width: 1029px){
		.container .header .left .profession{
			margin-left: 20px;
		}
		.container .header .left image{
			margin-left: 10px;
		}
	}
	.container .header .right{
		width: 25%;
		height:100%;
		/*border: #000000 solid 2px;*/
		display: flex;
		align-items: center;
		justify-content: flex-end;
		color: #333333;
		font-size: 95%;
	}
	.container .header .right image{
		width:45rpx;
		height:100%;
		/*border: #000000 solid 2px;*/
	}
	.container .intro{
		width: 90%;
		font-size: 90%;
		/*border: #000000 solid 2px;*/
		padding: 10rpx;
	}
	.download{
		height: 60px;
		/*border:  #000000 solid 2rpx;*/
		padding: 3rpx;
		display: flex;
		padding-top:5px;
		padding-bottom:5px;
		margin-left: 10rpx;
	}
	.download .left{
		/*max-width: 40%;*/
		height: 100%;
		display: flex;
		align-items: center;
		border:  #888888 solid 2rpx;
		border-right: 0;
		padding-right: 15rpx;
		padding-left: 15rpx;
		background-color: #BFEFFF;
	}	
	.download .left image{
		width:50rpx;
		height:100%;
	}
	.download .left .link{
		overflow: auto;
		font-weight: bold;
		font-size: 105%;
		margin-left: 15rpx;		
	}
	.download .right{
		max-width: 50%;
		height: 100%;
		border:  #888888 solid 2rpx;
		padding-left: 15rpx;
		padding-right: 15rpx;
		font-size: 90%;
	}
	.download .right view{
		height: 50%;
		overflow: auto;
		white-space:nowrap;
		display: flex;
		align-items: center;
		color: #666666;
	}
	@media only screen and (min-width: 1029px){
		.download{
			/*width: 50%;*/
		}
		.download .left{
			max-max-width: 30%;
		}
		.download .left image{
			width:30px;
			height:100%;
			margin-left: 5rpx;
		}
		.download .right{
			max-width: 70%;
			height: 100%;
		}
	}
</style>
