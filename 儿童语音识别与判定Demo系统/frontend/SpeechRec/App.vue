<script>
	export default {
		globalData: {
			domain: 'http://localhost:8080/',
			rootUrl: 'http://localhost:8080/service/',
		},
		onLaunch: function() {
			console.log('App Launch')
		},	
		onShow: function() {
			console.log('App Show')
		},
		onHide: function() {
			console.log('App Hide')
		},
		methods:{
			requestFailToast:function(){
				uni.showToast({
					icon: 'none',
					title: '服务器无响应',
					duration: 1500
				})
			},
			errorToast:function(errMsg){
				uni.showToast({
					icon: 'none',
					title: errMsg,
					duration: 1500
				})
			},
			successToast:function(msg){
				uni.showToast({
					icon: 'success',
					title: msg,
					duration: 1500
				})
			},
		}
	}
</script>

<style>
	
</style>
