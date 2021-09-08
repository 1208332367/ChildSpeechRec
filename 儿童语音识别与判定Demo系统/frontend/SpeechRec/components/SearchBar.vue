<template>
	<view class="search">
		<input class="text" placeholder="输入资源名称搜索"/>
		<image src="../static/index/search.png" mode="aspectFit"></image>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				
			};
		}
	}
</script>

<style>
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
		max-width:85%;
		font-size: small;
		color: #808080;
		/*border:#000000 solid 2px;*/
		display: flex;
		align-items: center;
		color: #000000;
	}
	.search image {
		width:50rpx;
		height:30px;
		/*border:#000000 solid 2px;*/	
	}
</style>
