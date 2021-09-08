<template>
	<view class="app_header">
		<!--
		<image v-if="page_index>0" src="../static/index/navigate_back.png" mode="aspectFit"></image>
		-->
		<view class="search">
			<input class="text" placeholder="输入资源名称搜索" @input="getTitle"/>
			<image v-if="searchTitle.length == 0" src="../static/index/search.png" mode="aspectFit"></image>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				searchTitle: '',
			};
		},
		props:{
			/*page_index: {
				type: Number,
				default: 0
			}*/
		},
		methods:{
			getTitle:function(e){
				this.searchTitle = e.target.value	
				uni.$emit('getSearchTitle', this.searchTitle)
			},
		}
	}
</script>

<style>
	.app_header{
		position: fixed;
		z-index: 9999;
		width: 100%;
		height:60px;
		/*border: #000000 solid 2px;*/
		display: flex;
		justify-content: center;
		align-items: center;
		border-bottom: 2px solid #DDDDDD;
		background-color: #FFFFFF;
		
	}
	.app_header image {
		width:8%;
		height:30px;
		margin-right: 20rpx;
		/*border:#000000 solid 2px;*/
	}
	.search{
		padding: 2px;
		width: 80%;
		height: 40px;
		display: flex;
		align-items: center;
		border: #3F536E solid 2px;
		border-radius: 5px 5px 5px 5px;
		justify-content: space-between;
	}
	.search .text{
		overflow: auto;
		height:35px;
		width:85%;
		font-size: small;
		color: #808080;
		/*border:#000000 solid 2px;*/
		display: flex;
		align-items: center;
		color: #000000;
		padding-left:10rpx;
	}
	.search image {
		width:50rpx;
		height:30px;
		/*border:#000000 solid 2px;*/
	}
</style>