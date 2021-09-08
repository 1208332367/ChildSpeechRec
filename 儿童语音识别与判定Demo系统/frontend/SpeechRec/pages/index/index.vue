<template>
	<view class="page">
		<view class="body">
			
			<view class="control">
				<view class="title">儿童语音识别与判定</view>
				<view class="intro">
					<view style="font-size: 105%;">[说明]</view>
					1. 上传音频文件压缩包后，可以进行识别及正确性判定<br style="margin-top: 10px;">
					2. 支持修改答案与人工判定比例<br style="margin-top: 5px;">
					3. 讯飞识别为后台处理，需要一定时间<br style="margin-top: 5px;">
				</view>
				
				<view class="fileInfo" style="height: 70px;">
					<view class="left">文件上传：</view>
					<view class="right" style="border: #FFFFFF solid 2px;" >
						<uni-file-picker :file-extname="['zip']" limit="1" file-mediatype="all" title="zip文件, 不超过50M" @success="uploadSuccess" @fail="uploadFail" @delete="deleteFile"></uni-file-picker>
					</view>
				</view>
			</view>
			
			<view class="file_list">
				<view class="title">文件列表</view>
				<view class="content">
					<view class="row" style="font-weight: bold;border-bottom: #000000 solid 1px;border-top: #000000 solid 2px;">
						<view class="unit1">题目ID</view>
						<view class="unit2">识别情况</view>
						<view class="unit3">判定情况</view>
					</view>		
					<view class="content2">
						<block v-if="file_list_length > 0">
							<block v-for="(value, folderID, index) in file_list" :key="index">
								<view class="row">
									<view class="unit1" @click="navigateToPage2(folderID, value.recNum, value.wav_count)">{{folderID}}</view>
									<view class="unit2">{{value.recNum}} / {{value.wav_count}}</view>
									<view class="unit3">{{value.hasJudge == 1? '已判定': '未判定'}}</view>
								</view>
							</block>
						</block>
						<block v-else>
							<view class="empty_file_list">暂无相关文件</view>
						</block>
					</view>
				</view>			
			</view>
			
		</view>
	</view>	

</template>

<script>
	let App = getApp()
	export default{
		data(){
			return {
				file_list_length: 0,
				file_list: {}
			}
		},
		onShow:function(e){
			this.getFileList()
		},
		
		methods:{
			data_init:function(e){
				this.file_list_length = 0
				this.file_list = {}
			},
			
			getFileList:function(e){
				var that = this
				uni.showLoading({
					title: '加载中...'
				})
				uni.request({
					url: App.globalData.rootUrl + 'upload/getFileList',
					data: {	
					},
					method:'POST',
					header:{
						'content-type': 'application/x-www-form-urlencoded'
					},
					success: (res) => {
						uni.hideLoading()
						if(res.data.code)
							App.errorToast(res.data.msg)
						else{
							that.file_list_length = res.data.data.length
							that.file_list = res.data.data.all_data
						}
					},
					fail: (res) => {
						uni.hideLoading()
						App.requestFailToast()
					}
				})
			},
			
			uploadSuccess:function(e){
				//getApp().successToast("上传成功")
				var that = this
				this.filePath = e.tempFilePaths[0]
				this.filename = e.tempFiles[0].name.replace('.zip', '')
						
				uni.showLoading({
					title: '正在上传到服务器...'
				})
							
				uni.uploadFile({
					url: getApp().globalData.rootUrl + 'upload/uploadFile',
					filePath: that.filePath,
					name: 'file',
					formData: {
						'folderID': that.filename
					},			
					success: (res) => {					
						var new_res = JSON.parse(res.data)
						if(new_res.code)
							setTimeout(function(){
							  uni.hideLoading()
							  getApp().errorToast(new_res.msg)
							}, 1000)			
						else{
							setTimeout(function(){
							  uni.hideLoading()
							  getApp().successToast("上传成功")
							}, 1000)
							that.data_init()
							that.getFileList()
						}
					},
					fail: (res) => {
						uni.hideLoading()
						getApp().requestFailToast()
					}
				})
			},
			
			uploadFail:function(e){
				getApp().errorToast("文件上传失败")
				this.filePath = ''
				this.filename = ''
			},		
			
			deleteFile:function(){
				this.filePath = ''
				this.filename = ''
			},
			
			navigateToPage2:function(folderID, recNum, wav_count){
				//console.log(folderID)
				//console.log(hasRec)
				uni.navigateTo({
					url: '/pages/recognize/recognize?folderID=' + folderID + '&recNum=' + recNum + '&wav_count=' + wav_count
				})
			}
		}
	}
</script>

<style>
	.page{
		width: 100%;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		
		/*border: #000000 solid 2px;*/
	}
	
	.body{
		width: 95%;
		/*border: #000000 solid 2px;*/
	}
	
	.control{
		margin-left: 300rpx;
		margin-top: 30px;
	}	
	.control .title{
		font-weight: bold;
		font-size: 150%;
		width: 100%;
	}
	.control .intro{
		margin-top: 30px;
		/*border: #000000 solid 2px;*/
	}

	.control .fileInfo{
		width: 100%;
		height: 60px;
		margin-top: 10px;
		/*border: #000000 solid 2px;*/
		display: flex;
		align-items: center;
	}
	.fileInfo .left{
		width: 80px;
		margin-top: 10px;
		height: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
		/*border: #000000 solid 2px;*/
	}
	.fileInfo .right{
		width:70%;
		height: 60%;
		font-size: small;
		border: #3F536E solid 2rpx;
		display: flex;
		align-items: center;
		color: #000000;
		border-radius: 10rpx 10rpx 10rpx 10rpx;
		margin-left: 10rpx;
		padding-left:10rpx;
	}
	.fileInfo .right .upload_file{
		color: #00C7FF;
		font-weight: bold;
	}
	
	.file_list{
		margin-top: 20px;
		width: 100%;
		/*border: #000000 solid 2px;*/
		display: flex;
		flex-direction: column;
		align-items: center;

	}
	.file_list .title{
		width: 100%;
		text-align: center;
		font-weight: bold;
		font-size: 115%;
	}
	.file_list .content{
		width: 70%;
		margin-top: 10px;
		max-height: 400px;
		border-bottom: #000000 solid 2px;
		/*border: #000000 solid 2px;*/
	}
	.file_list .content2{
		max-height: 350px;
		overflow: auto;
		/*border: #000000 solid 2px;*/
	}
	.file_list .content .row{
		width: 100%;
		height: 30px;
		display: flex;
		align-items: center;
		justify-content: space-between;
		/*border: #000000 solid 2px;*/
	}
	.file_list .content .row .unit1{
		/*text-align: center;*/
		text-align: center;
		width: 50%;
		overflow: auto;
		/*border: #000000 solid 2px;*/
	}
	.file_list .content .row .unit2{
		/*text-align: center;*/
		text-align: center;
		width: 30%;
		overflow: auto;
		/*border: #000000 solid 2px;*/
	}
	.file_list .content .row .unit3{
		/*text-align: center;*/
		text-align: center;
		width: 20%;
		overflow: auto;
		/*border: #000000 solid 2px;*/
	}
	.empty_file_list{
		width: 100%;
		text-align: center;
	}

</style>
