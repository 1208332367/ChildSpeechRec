<template>
	<block v-if="!isChoose">
		<view :class="[Span, Offset]" :style="'padding:2px '+ Gutter +'px;border-radius: 12px;border:#ffffff solid 2rpx;margin-left: 5rpx; margin-top: 1px;text-align: center;'"
		@tap="onClick" :data-type="type" :data-url="url" >
			<view v-if="bgClass!='' || bgStyle!=''" class="Bg" :class="bgClass" :style="Radius + bgStyle">
				<slot></slot>
			</view>
			<slot v-else></slot>
		</view>
	</block>
	
	<block v-else>
		<view  :class="[Span, Offset]" :style="'padding:2px '+ Gutter +'px;color: #ffffff; border-radius: 12px;border: #ff0000 solid 2rpx; background-color: #ff0000;margin-left: 5rpx; margin-top: 1px;text-align: center;'"
		@tap="onClick" :data-type="type" :data-url="url" >
		<view v-if="bgClass!='' || bgStyle!=''" class="Bg" :class="bgClass" :style="Radius + bgStyle">
				<slot></slot>
			</view>
			<slot v-else></slot>
		</view>
	</block>
</template>

<script>
	export default {
		name: "o-col",
		props:{
			span:{
				type:[Number,String],
				default:''
			},
			offset:{
				type:[Number,String],
				default:0
			},
			url:{
				type:String,
				default:''
			},
			type:{
				type:String,
				default:''
			},
			isChoose:{
				type: Boolean,
				default: false
			}
		},
		inject: ['gutter','bgclass','bgstyle','radius','cols'],
		computed:{
			Span(){
				if(this.cols!='') return '';
				else if(this.span =='' || this.span > 24) return 'o-col-24';
				else if(this.span < 1 ) return 'o-col-1';
				else return 'o-col-'+this.span;
			},
			Offset(){
				if(this.offset >= 1 && this.offset < 24) 
					return 'offset-' + this.offset;
				else return '';
			},
			Radius(){
				if(this.radius > 0)
					return 'border-radius:' + this.radius + 'rpx;overflow:hidden;';
				else return '';
			},
			bgStyle(){
				if(this.bgstyle != '')
					return 'background-color:'+this.bgstyle;
				else return '';
			},
			bgClass(){
				if(this.bgclass != '' && this.bgstyle == '')
					return this.bgclass;
				else return '';
			},
			Gutter(){
				if(this.gutter != '0' || this.gutter > 0)
					return this.gutter;
				else return ''
			}
		},
		methods: {
			
			onClick(e) {
				/*
				let url = e.currentTarget.dataset.url;
				let type = e.currentTarget.dataset.type;
				switch (type) {
					case 'tabbar':{ //跳转到tabbar页
						uni.switchTab({ url:url });
						break;
					}
					case 'back':{ //返回上一页，只有当前为非tabbar页能起作用
						uni.navigateBack({ delta:1 });
						break;
					}
					case 'modal':{ //弹出对话框
						uni.showModal({
							title:url,
							content:'test'
						});
						break;
					}
					case 'toast':{ //弹出提示框
						uni.showToast({
							icon:'none',
							title:url
						})
						break;
					}
					
					default:{ //非tabbar页跳转
						if (!url) {
							console.log('你点击了')
						}
						else {
							uni.navigateTo({ url:url })
						}
					}
				}*/
				this.$emit('Click');
			}
		}
	}
</script>

<style lang="scss">

	[class*="o-col-"] {
		float:left;
		box-sizing:border-box;
		.Bg{height:100%;}
	}
	.col-auto {flex: 0 0 auto;width: auto;max-width: 100%;}

	@for $col from 1 through 24 {
		.o-col-#{$col}{
			/* #ifdef APP-PLUS || H5 */
			flex: 0 0 calc(100%/24*#{$col});
			max-width:calc(100%/24*#{$col});
			/* #endif */
			/* #ifdef MP */
			width: calc(100%/24 * #{$col});
			/* #endif */
		}
	}

	@for $i from 1 through 23 {
		.offset-#{$i}{margin-left:calc(100%/24*#{$i})}
	}
	
	@for $col from 2 through 5 {
		.row.cols-#{$col}>*{
			flex:0 0 calc(100% / #{$col}) !important;
			max-width:calc(100% / #{$col}) !important;
			box-sizing:border-box;
		}
	}
	

</style>
