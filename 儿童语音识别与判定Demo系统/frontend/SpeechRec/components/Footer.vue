<template>
	<view>
		<view class="footer">
			<text>CopyRight©王佳镐&emsp;华东师范大学计算机科学与技术学院</text>
			<uni-link href="https://beian.miit.gov.cn/" text="浙ICP备19031710号-1"></uni-link>
		</view>
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
	.footer{
		width: 100%;
		height: 30px;
		color: #AAAAAA;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		margin-top:30px;
	}
	.footer uni-link{
		font-size: small;
		color: #AAAAAA;
	}
</style>
