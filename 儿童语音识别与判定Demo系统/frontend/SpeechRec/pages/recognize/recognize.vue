<template>
	<view class="page">
		<view class="body">
		
			<view class="folderID">{{folderID}}</view>
			
			<view class="info" style="margin-top: 30px;">
				<view class="left">图片答案：</view>
				<view class="button_right" style="margin-left:0;width: 200px;">
					<input class="right_input" :value="new_answer" :placeholder="default_answer" @input="getInputAnswer"/>
				</view>
				<view class="button_right">
					<view class="confirm_button" @click="modifyAnswer">提交修改</view>
				</view>
			</view>
			
			<view class="info">
				<view class="left">音频数量：</view>
				<view class="right">{{wav_list_length}}</view>
			</view>
			
			<view class="info">
				<view class="left">讯飞识别：</view>
				<view class="right">{{recNum}} / {{wav_count}}</view>
				<view class="button_right">
					<view class="confirm_button" @click="recognizeAll">一键识别</view>
				</view>
			</view>
			
			<view class="info">
				<view class="left">人工判定：</view>
				
				<view class="right">
					<picker  @change="bindHumanPartPickerChange" :value="human_part_index" :range="human_part" >
						<view class="uni-input">{{human_part[human_part_index]}}</view>
					</picker>
					<image class="picker_img" src="../../static/down.png" mode="aspectFit"></image>
				</view>
				<view class="button_right">
					<view class="confirm_button" @click="getAllJudge">一键判定</view>
				</view>
			</view>
			
			<view class="wav_list">
				<view class="title">音频列表</view>
				<view class="content">
					<view class="row" style="font-weight: bold;border-bottom: #000000 solid 1px;border-top: #000000 solid 2px;">
						<view class="unit1">音频ID</view>
						<view class="unit_audio"></view>
						<view class="unit2">讯飞识别</view>
						<view class="unit3">认知判定</view>
					</view>
					<view class="content2">
						<block v-if="wav_list_length > 0">
							<block v-for="(value, wavID, index) in wav_list" :key="index">
								<view class="row">
									<view class="unit1" >
										{{wavID}}	
									</view>
									<view class="unit_audio">
										<image @click="playAudio(wavID)" class="audio_play_img" src="../../static/audio_play.png" mode="aspectFit"></image>
									</view>
									<view class="unit2">{{value.xunfei_word}}</view>
									<view class="unit3">{{value.judge}}</view>
								</view>
							</block>
						</block>
						<block v-else>
							<view class="empty_wav_list">暂无相关文件</view>
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
				folderID: '无音频',
				default_answer: '',
				new_answer: '',
				wav_list_length: 0,	
				wav_count: 0,
				recNum: 0,
				human: 0.3,
				human_part: [],
				human_part_index: 0,
				wav_list: {},	
			}
		},
		onLoad(option) {
			if(option.folderID)
				this.folderID = option.folderID
			if(option.wav_count)
				this.wav_count = option.wav_count
			if(option.recNum)
				this.recNum = option.recNum
			this.getHumanPart()
			this.getInfo()
		},	
		
		onShow:function(e){
			//this.getAllJudge()
		},
		
		methods:{
			data_init:function(e){
				this.wav_list_length = 0
				this.wav_list = {}
				this.human = '0.3'
				this.default_answer = ''
				this.new_answer = ''
				this.recNum = 0
				this.wav_count = 0
				this.human_part = []
				this.human_part_index = 0
			},
			getHumanIndex:function(){
				var human_part = this.human_part 
				for(var i = 0; i < human_part.length; i++){
					if(human_part[i] == this.human){
						this.human_part_index = i
						break
					}
				}
				
			},
			
			playAudio:function(wavID){
				var that = this
				var src = App.globalData.domain + 'media/files/' + this.folderID + '/wav/' + wavID + '.wav'
				console.log(src)
				var audio = new Audio()
				audio.src = src;
				let playPromise; 
				playPromise = audio.play();
				if (playPromise) {
				        playPromise.then(() => {
				            // 音频加载成功
				            // 音频的播放需要耗时
				          /*that.tiemr = setInterval(() => {
				            second--;
				            if (second <= 0) {
				              that.audio.pause()
				              clearInterval(that.tiemr);
				            }
				          }, 1000);*/
				        }).catch((e) => {
				          // 音频加载失败
				          console.error(e);
				        });
				      }
			},
			
			getInputAnswer:function(e){
				this.new_answer = e.target.value	
			},	
			
			modifyAnswer:function(e){
				var that = this
				if(!that.new_answer || that.new_answer == ''){
					App.errorToast('答案不能为空')
					return
				}
				//console.log(that.new_answer)
				uni.showModal({
					title:'请确认答案以[、]分隔，且不包含多余字符',
					success: (res) => {
						if(res.confirm){
							uni.request({
								url: App.globalData.rootUrl + 'recognize/modifyAnswer',
								data: {
									folderID: that.folderID,
									answer: that.new_answer
								},
								method:'POST',
								header:{
									'content-type': 'application/x-www-form-urlencoded'
								},
								success: (res) => {
									if(res.data.code)
										App.errorToast(res.data.msg)
									else{
										App.successToast('修改成功')
										setTimeout(function(){
										  that.getAllJudge()
										}, 700)										
									}
								},
								fail: (res) => {
									App.requestFailToast()
								}
							})
						}
					}
				})
				
			},
			
			getHumanPart:function(e){
				var that = this
				uni.request({
					url: App.globalData.rootUrl + 'recognize/getHumanPart',
					data: {
					},
					method:'POST',
					header:{
						'content-type': 'application/x-www-form-urlencoded'
					},
					success: (res) => {
						if(res.data.code)
							App.errorToast(res.data.msg)
						else{
							that.human_part = res.data.data.humanPart
							that.human_part_index = res.data.data.defaultIndex
						}
					},
					fail: (res) => {
						App.requestFailToast()
					}
				})
			},
			
			bindHumanPartPickerChange: function(e) {
			    //console.log('picker发送选择改变，携带值为', e.target.value)
			    this.human_part_index = e.target.value
				this.human = this.human_part[e.target.value]
			},
			
			recognizeAll:function(e){
				var that = this
				var wav_list = this.wav_list
				if(this.wav_count == this.recNum){
					App.errorToast('无需识别')
					return
				}
				uni.showModal({
					title:'识别耗时较长，确定进行？',
					success: (res) => {
						if(res.confirm){
							uni.request({
								url: App.globalData.rootUrl + 'recognize/getRecognize',
								data: {
									folderID: that.folderID,
								},
								method:'POST',
								header:{
									'content-type': 'application/x-www-form-urlencoded'
								},
								success: (res) => {		
									if(res.data.code)
										App.errorToast(res.data.msg)
									else{
										App.successToast('提交成功')	
									}
								},
								fail: (res) => {	
									App.requestFailToast()
								}
							})							
						}
					}
				})
			},
			
			/*
			judgeHasRec:function(e){
				var wav_list = this.wav_list
				this.hasRec = '已识别'
				for(var key in wav_list) {
					var value = wav[key]
					if(wav_list[key]['xunfei_word'] == '[未识别]'){
						this.hasRec = '未识别'
						break
					}
				}
				
			},*/
			
			getWavList:function(wav){
				var wav_list = {}
				for(var key in wav) {
					wav_list[key] = {}
					wav_list[key]['wavID'] = key
					
				　　var value = wav[key]				
					if(value['errcode'] == -1 || value['errcode'] == 500){
						wav_list[key]['xunfei_word'] = '[未识别]'
						wav_list[key]['judge'] = '[无]'	
					}
					if(value['errcode'] == 1){
						wav_list[key]['xunfei_word'] = '[空]'
						wav_list[key]['judge'] = '[无]'	
					}
					if(value['errcode'] == 0){
						wav_list[key]['xunfei_word'] = value['xunfei_word']
						if(value['need_human'] == 1)
							wav_list[key]['judge'] = '待定'
						else{
							wav_list[key]['judge'] = value['judge'] == 1? '正确': '错误'
						}
					}
				}
				this.wav_list = wav_list
			},
			
			getAllJudge:function(e){
				var that = this
				uni.showLoading({
					title: '加载中...'
				})
				uni.request({
					url: App.globalData.rootUrl + 'recognize/getAllJudge',
					data: {
						folderID: that.folderID,
						partPercent: that.human
					},
					method:'POST',
					header:{
						'content-type': 'application/x-www-form-urlencoded'
					},
					success: (res) => {
						setTimeout(function(){
						  uni.hideLoading()
						  if(res.data.code)
						  	App.errorToast(res.data.msg)
						  else{
						  	that.wav_list_length = res.data.data.wav_count
						  	that.getWavList(res.data.data.wav)
						  	that.default_answer = (res.data.data.answer.word_list).join('、')
						  	that.new_answer = ''
						  	that.recNum = res.data.data.recNum
						  	that.wav_count = res.data.data.wav_count
						  	that.human = res.data.data.human
						  	that.getHumanIndex()
						  }
						}, 500)	
						
					},
					fail: (res) => {
						uni.hideLoading()
						App.requestFailToast()
					}
				})
			},
			
			getInfo:function(e){
				var that = this
				uni.showLoading({
					title: '加载中...'
				})
				uni.request({
					url: App.globalData.rootUrl + 'recognize/getInfo',
					data: {
						folderID: that.folderID
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
							that.wav_list_length = res.data.data.wav_count
							that.getWavList(res.data.data.wav)
							that.default_answer = (res.data.data.answer.word_list).join('、')
							that.new_answer = ''
							that.recNum = res.data.data.recNum
							that.wav_count = res.data.data.wav_count
							that.human = res.data.data.human
							that.getHumanIndex()
							that.getAllJudge()
						}
					},
					fail: (res) => {
						uni.hideLoading()
						App.requestFailToast()
					}
				})
			},
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
		width: 85%;
		/*border: #000000 solid 2px;*/
	}
	
	.folderID{
		margin-top: 20px;
		font-weight: bold;
		font-size: 140%;
	}
	
	.info{
		display: flex;
		width: 100%;
		height:40px;
		/*border: #000000 solid 2px;*/
	}
	
	.info .left{
		width: 85px;
		height: 100%;
		display: flex;
		align-items: center;
		/*border: #000000 solid 2px;*/
	}
	
	.info .right_input{
		width: 100%;
		height: 70%;
		display: flex;
		align-items: center;
		border: #000000 solid 1px;
		border-radius: 5px;
	}
	
	.info .right{
		display: flex;
		width: 60px;
		height: 100%;
		align-items: center;
		
		/*border: #000000 solid 2px;*/
	}
	
	.info .right view{
		z-index: 999;
	}
	
	.picker_img{
		width: 30px;
		height:30px;
		z-index: -1;
	}
	
	.audio_play_img{
		width: 20px;
		height:20px;
	}
	
	.info .button_right{
		margin-left: 10px;
		width: 80px;
		height: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
		/*border: #000000 solid 2px;*/
	}
	
	.info .confirm_button{
		width: 100%;
		font-size: 90%;
		display: flex;
		height: 70%;
		align-items: center;
		justify-content: center;
		border-radius: 5px;
		background-color:#0067FF;
		
		color: #FFFFFF;
	}
	
	.wav_list{
		width: 100%;
		margin-top: 20px;
		/*border: #000000 solid 2px;*/
		display: flex;
		flex-direction: column;
		align-items: center;
	
	}
	.wav_list .title{
		width: 100%;
		text-align: center;
		font-weight: bold;
		font-size: 115%;
	}
	.wav_list .content{
		width: 100%;
		margin-top: 10px;
		max-height:400px;
		border-bottom: #000000 solid 2px;
		/*border: #000000 solid 2px;*/
	}
	.wav_list .content2{
		max-height:350px;
		width: 100%;
		overflow: auto;
	}
	.wav_list .content .row{
		width: 100%;
		height: 30px;
		display: flex;
		align-items: center;
		justify-content: space-between;
		/*border: #000000 solid 2px;*/
	}
	.wav_list .content .row .unit1{
		/*text-align: center;*/
		text-align: center;
		width: 50%;
		overflow: auto;
		/*border: #000000 solid 2px;*/
	}
	.wav_list .content .row .unit2{
		text-align: center;
		width: 35%;
		overflow: auto;
		/*border: #000000 solid 2px;*/
	}
	.wav_list .content .row .unit3{
		text-align: center;
		width: 10%;
		overflow: auto;
		/*border: #000000 solid 2px;*/
	}
	.wav_list .content .row .unit_audio{
		text-align: center;
		width: 4%;
		display: flex;
		align-items: center;
		justify-content: center;
		/*border: #000000 solid 2px;*/
	}
	.empty_wav_list{
		width: 100%;
		text-align: center;
	}


</style>
