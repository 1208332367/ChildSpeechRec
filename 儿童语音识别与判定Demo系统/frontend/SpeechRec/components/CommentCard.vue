<template>
	<view class="container">
		<view class="left">
			<view class="name">
				{{commentInfo.commenterName}}:
			</view>
			<view class="content">
				{{commentInfo.content}}
			</view>
		</view>
		<view class="right">
			<view class="stars">
				<block v-for="(item, index) in (commentInfo.score / 2)" :key="index">
					<image src="../static/component/comment/full_star.png" mode="aspectFit"></image>
				</block>
			</view>
			<view v-if="!commentInfo.canDelete" class="date">
				{{commentInfo.ctime}}
			</view>
			<view class="delete" v-if="commentInfo.canDelete"  @click="deleteComment">删除</view>
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
			commentInfo: {
				type: Object,
				default(){
					return{}	
				}
			},
			
		},
		methods:{
			deleteComment:function(){
				var that = this
				uni.showModal({
					showCancel: true,
					title: '确定删除评论？',
					success: (res) =>  {
						if(res.confirm){
							uni.request({
								url: getApp().globalData.rootUrl + 'resource/deleteComment',
								data: {
									CommentID: that.commentInfo.CommentID,
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
										setTimeout(function(){		  
										  uni.$emit("deleteComment")
										}, 1000)																								
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
		}
	}
</script>

<style>
	.container{
		width: 100%;
		/*border: #000000 solid 2rpx;*/
		display: flex;
		justify-content: space-between;
		height: 40px;
	}
	.container .left{
		display: flex;
		align-items: center;
		width: 50%;
		/*border: #000000 solid 2rpx;*/
		font-size: 95%;
	}
	@media only screen and (min-width: 1029px){
		.container .left{
			width: 75%;
			/*border: #000000 solid 2rpx;*/
		}
	}
	.container .left .name{
		color: #AAAAAA;
		/*width: 30%;*/
		/*border: #000000 solid 2rpx;*/
		height: 100%;
		overflow: auto;
		white-space:nowrap;
		display: flex;
		align-items: center;
	}
	.container .left .content{
		/*width: 70%;*/
		/*border: #000000 solid 2rpx;*/
		height: 100%;
		overflow: auto;
		white-space:nowrap;
		display: flex;
		align-items: center;
		padding-left:10rpx;
	}
	.container .right{
		height:100%;
		display: flex;
		align-items: center;
		justify-content: flex-end;
		/*border: #000000 solid 2rpx;*/
	}
	.container .right .delete{
		width: 60rpx;
		height: 100%;
		font-size: 95%;
		display: flex;
		align-items: center;
		justify-content: flex-end;
		color: #888888;
		/*border: #000000 solid 2rpx;*/
		padding-left: 10rpx;
	}
	.container .right .stars{
		height: 100%;
		display: flex;
		/*border: #000000 solid 2rpx;*/
		align-items: center;
		justify-content: flex-end;
	}
	.container .right .stars image{
		width: 30rpx;
		height: 100%;
		/*border: #000000 solid 2rpx;*/
	}
	.container .right .date{
		font-size: 95%;
		height: 100%;
		display: flex;
		align-items: center;
		color: #AAAAAA;
		padding-left: 20rpx;
	}
</style>
