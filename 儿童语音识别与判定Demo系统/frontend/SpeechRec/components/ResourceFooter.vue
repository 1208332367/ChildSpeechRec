<template>
	<view class="container">
		<view class="left">
			<view class="item" style="margin-left: 5rpx;">
				<image src="../static/component/resource/watch.png" mode="aspectFit"></image>
				<text>{{item.visitCount}}</text>	
			</view>
			<view class="item">
				<image src="../static/component/resource/store.png" mode="aspectFit"></image>
				<text>{{item.storeCount}}</text>
			</view>
			<view class="item">
				<image src="../static/component/resource/comment.png" mode="aspectFit"></image>
				<text>{{item.commentCount}}</text>
			</view>
		</view>
		<view class="right">
			<view v-if="isDetail" class="item">
				<view @click="storeResource">收藏</view>
				<view @click="reportResource">举报</view>
			</view>
			<view v-if="!isDetail" class="item">
				{{item.downloadCount}}次下载
			</view>
			<view class="item" style="margin-right: 2rpx;">
				{{item.ctime}}
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
			};
		},
		props:{
			isDetail: {
				type: Boolean,
				default: true
			},
			item: {
				type: Object,
				default(){
					return{}	
				}
			},
		},
		methods:{
			storeResource:function(){
				var that = this
				try{
					let current_userinfo = uni.getStorageSync('userInfo')
					uni.showModal({
						showCancel: true,
						title: '确定收藏该资源？',
						success: (res) =>  {
							if(res.confirm){
								uni.request({
									url: getApp().globalData.rootUrl + 'user/storeResource',
									data: {
										ResourceID: that.item.ResourceID,
										UserID: current_userinfo.UserID,
									},			
									method:'POST',
									header:{
										'content-type': 'application/x-www-form-urlencoded'
									},
									success: (res) => {
										if(res.data.code)
											getApp().errorToast(res.data.msg)
										else{
											getApp().successToast("收藏成功")
											that.item.storeCount ++
										}
									},
									fail: (res) => {
										getApp().requestFailToast()
									}
								})
							}
						}
					})			
				}catch(e){
					
				}			
			},
			reportResource:function(){
				var that = this
				try{
					let current_userinfo = uni.getStorageSync('userInfo')
					uni.showModal({
						showCancel: true,
						title: '确定举报该资源？',
						success: (res) =>  {
							if(res.confirm){
								uni.request({
									url: getApp().globalData.rootUrl + 'resource/reportResource',
									data: {
										ResourceID: that.item.ResourceID,
										UserID: current_userinfo.UserID,
									},			
									method:'POST',
									header:{
										'content-type': 'application/x-www-form-urlencoded'
									},
									success: (res) => {
										if(res.data.code)
											getApp().errorToast(res.data.msg)
										else{
											getApp().successToast("举报成功")
										}
									},
									fail: (res) => {
										getApp().requestFailToast()
									}
								})
							}
						}
					})	
				}catch(e){
					
				}
			},
		}
	}
</script>

<style>
	.container{
		width: 100%;
		display: flex;
		flex-direction: row;
		height: 25px;
		/*border: #000000 solid 2px;*/
		justify-content: space-between;
		font-size: 90%;
		
	}
	.container .left{
		width: 40%;
		height: 100%;
		/*border: #000000 solid 2px;*/
		display: flex;
		flex-direction: row;
		align-items: center;
		color: #333333;
		/*border-bottom: #D3D3D3 solid 2px;*/
	}
	.container .left .item{
		height: 100%;
		/*border: #000000 solid 2px;*/
		display: flex;
		flex-direction: row;
		align-items: center;
		margin-left: 10rpx;
	}
	@media only screen and (min-width: 1029px){
		.container .left .item{
			margin-left: 20px;
		}
	}
	.container .left .item image{
		width:35rpx;
		height:100%;
		margin-left: 5rpx;
	}
	.container .left .item text{
		margin-left: 2rpx;
	}
	.container .right{
		width: 60%;
		/*border: #000000 solid 2px;*/
		height: 100%;
		display: flex;
		flex-direction: row;
		align-items: center;
		justify-content:flex-end;
		color: #AAAAAA;
		/*border-bottom: #D3D3D3 solid 2px;*/
	}
	.container .right .item{
		/*border: #000000 solid 2px;*/
		height: 100%;
		display: flex;
		flex-direction: row;
		margin-right: 10rpx;
		align-items: center;
	}
	.container .right .item view{
		margin-right: 5rpx;
	}
	@media only screen and (min-width: 1029px){
		.container .right .item{
			margin-right: 30px;
		}
		.container .right .item view{
			margin-right: 10px;
		}
	}
</style>
