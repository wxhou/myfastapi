import os
import sys
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(BASE_DIR)
import uuid
import asyncio

from sqlalchemy import select, values, delete
from app.core.db import async_session
from app.utils.logger import logger
from app.api.goods.model import Goods, GoodsCategory


row1_data = [
    {
        'sub_categorys': [
            {
                'sub_categorys': [
                    {
                        'code': 'yr',
                        'name': '羊肉'
                    },
                    {
                        'code': 'ql',
                        'name': '禽类'
                    },
                    {
                        'code': 'zr',
                        'name': '猪肉'
                    },
                    {
                        'code': 'nr',
                        'name': '牛肉'
                    }
                ],
                'code': 'jprl',
                'name': '精品肉类'
            },
            {
                'sub_categorys': [
                    {
                        'code': 'cb',
                        'name': '参鲍'
                    },
                    {
                        'code': 'yu',
                        'name': '鱼'
                    },
                    {
                        'code': 'xia',
                        'name': '虾'
                    },
                    {
                        'code': 'xb',
                        'name': '蟹/贝'
                    }
                ],
                'code': 'hxsc',
                'name': '海鲜水产'
            },
            {
                'sub_categorys': [
                    {
                        'code': 'xhd_xyd',
                        'name': '松花蛋/咸鸭蛋'
                    },
                    {
                        'code': 'jd',
                        'name': '鸡蛋'
                    }
                ],
                'code': 'dzp',
                'name': '蛋制品'
            },
            {
                'sub_categorys': [
                    {
                        'code': 'sc',
                        'name': '生菜'
                    },
                    {
                        'code': 'bc',
                        'name': '菠菜'
                    },
                    {
                        'code': 'yj',
                        'name': '圆椒'
                    },
                    {
                        'code': 'xlh',
                        'name': '西兰花'
                    }
                ],
                'code': 'ycl',
                'name': '叶菜类'
            },
            {
                'sub_categorys': [

                ],
                'code': 'gjl',
                'name': '根茎类'
            },
            {
                'sub_categorys': [

                ],
                'code': 'qgl',
                'name': '茄果类'
            },
            {
                'sub_categorys': [

                ],
                'code': 'jgl',
                'name': '菌菇类'
            },
            {
                'sub_categorys': [

                ],
                'code': 'jksx',
                'name': '进口生鲜'
            }
        ],
        'code': 'sxsp',
        'name': '生鲜食品'
    },
    {
        'sub_categorys': [
            {
                'sub_categorys': [
                    {
                        'code': 'wly',
                        'name': '五粮液'
                    },
                    {
                        'code': 'lzlj',
                        'name': '泸州老窖'
                    },
                    {
                        'code': 'mt',
                        'name': '茅台'
                    }
                ],
                'code': 'bk',
                'name': '白酒'
            },
            {
                'sub_categorys': [

                ],
                'code': 'ptj',
                'name': '葡萄酒'
            },
            {
                'sub_categorys': [

                ],
                'code': 'yj',
                'name': '洋酒'
            },
            {
                'sub_categorys': [

                ],
                'code': 'pj',
                'name': '啤酒'
            },
            {
                'sub_categorys': [
                    {
                        'code': 'qtpp',
                        'name': '其他品牌'
                    },
                    {
                        'code': 'hj',
                        'name': '黄酒'
                    },
                    {
                        'code': 'ysj',
                        'name': '养生酒'
                    }
                ],
                'code': 'qtjp',
                'name': '其他酒品'
            },
            {
                'sub_categorys': [

                ],
                'code': 'yls',
                'name': '饮料/水'
            },
            {
                'sub_categorys': [
                    {
                        'code': 'bld',
                        'name': '白兰地'
                    },
                    {
                        'code': 'wsj',
                        'name': '威士忌'
                    }
                ],
                'code': 'hj',
                'name': '红酒'
            }
        ],
        'code': 'jsyl',
        'name': '酒水饮料'
    },
    {
        'sub_categorys': [
            {
                'sub_categorys': [
                    {
                        'code': '其他食用油',
                        'name': '其他食用油'
                    },
                    {
                        'code': '菜仔油',
                        'name': '菜仔油'
                    },
                    {
                        'code': '花生油',
                        'name': '花生油'
                    },
                    {
                        'code': '橄榄油',
                        'name': '橄榄油'
                    },
                    {
                        'code': '礼盒',
                        'name': '礼盒'
                    }
                ],
                'code': '食用油',
                'name': '食用油'
            },
            {
                'sub_categorys': [
                    {
                        'code': '面粉/面条',
                        'name': '面粉/面条'
                    },
                    {
                        'code': '大米',
                        'name': '大米'
                    },
                    {
                        'code': '意大利面',
                        'name': '意大利面'
                    }
                ],
                'code': '米面杂粮',
                'name': '米面杂粮'
            },
            {
                'sub_categorys': [
                    {
                        'code': '调味油/汁',
                        'name': '调味油/汁'
                    },
                    {
                        'code': '酱油/醋',
                        'name': '酱油/醋'
                    }
                ],
                'code': '厨房调料',
                'name': '厨房调料'
            },
            {
                'sub_categorys': [

                ],
                'code': '南北干货',
                'name': '南北干货'
            },
            {
                'sub_categorys': [

                ],
                'code': '方便速食',
                'name': '方便速食'
            },
            {
                'sub_categorys': [

                ],
                'code': '调味品',
                'name': '调味品'
            }
        ],
        'code': '粮油副食',
        'name': '粮油副食'
    },
    {
        'sub_categorys': [
            {
                'sub_categorys': [
                    {
                        'code': '西红柿',
                        'name': '西红柿'
                    },
                    {
                        'code': '韭菜',
                        'name': '韭菜'
                    },
                    {
                        'code': '青菜',
                        'name': '青菜'
                    }
                ],
                'code': '有机蔬菜',
                'name': '有机蔬菜'
            },
            {
                'sub_categorys': [
                    {
                        'code': '甘蓝',
                        'name': '甘蓝'
                    },
                    {
                        'code': '胡萝卜',
                        'name': '胡萝卜'
                    },
                    {
                        'code': '黄瓜',
                        'name': '黄瓜'
                    }
                ],
                'code': '精选蔬菜',
                'name': '精选蔬菜'
            },
            {
                'sub_categorys': [
                    {
                        'code': '火龙果',
                        'name': '火龙果'
                    },
                    {
                        'code': '菠萝蜜',
                        'name': '菠萝蜜'
                    },
                    {
                        'code': '奇异果',
                        'name': '奇异果'
                    }
                ],
                'code': '进口水果',
                'name': '进口水果'
            },
            {
                'sub_categorys': [
                    {
                        'code': '水果礼盒',
                        'name': '水果礼盒'
                    },
                    {
                        'code': '苹果',
                        'name': '苹果'
                    },
                    {
                        'code': '雪梨',
                        'name': '雪梨'
                    }
                ],
                'code': '国产水果',
                'name': '国产水果'
            }
        ],
        'code': '蔬菜水果',
        'name': '蔬菜水果'
    },
    {
        'sub_categorys': [
            {
                'sub_categorys': [
                    {
                        'code': '果冻',
                        'name': '果冻'
                    },
                    {
                        'code': '枣类',
                        'name': '枣类'
                    },
                    {
                        'code': '蜜饯',
                        'name': '蜜饯'
                    },
                    {
                        'code': '肉类零食',
                        'name': '肉类零食'
                    },
                    {
                        'code': '坚果炒货',
                        'name': '坚果炒货'
                    }
                ],
                'code': '休闲零食',
                'name': '休闲零食'
            },
            {
                'sub_categorys': [
                    {
                        'code': '创意喜糖',
                        'name': '创意喜糖'
                    },
                    {
                        'code': '口香糖',
                        'name': '口香糖'
                    },
                    {
                        'code': '软糖',
                        'name': '软糖'
                    },
                    {
                        'code': '棒棒糖',
                        'name': '棒棒糖'
                    }
                ],
                'code': '糖果',
                'name': '糖果'
            },
            {
                'sub_categorys': [
                    {
                        'code': '夹心巧克力',
                        'name': '夹心巧克力'
                    },
                    {
                        'code': '白巧克力',
                        'name': '白巧克力'
                    },
                    {
                        'code': '松露巧克力',
                        'name': '松露巧克力'
                    },
                    {
                        'code': '黑巧克力',
                        'name': '黑巧克力'
                    }
                ],
                'code': '巧克力',
                'name': '巧克力'
            },
            {
                'sub_categorys': [
                    {
                        'code': '牛肉干',
                        'name': '牛肉干'
                    },
                    {
                        'code': '猪肉脯',
                        'name': '猪肉脯'
                    },
                    {
                        'code': '牛肉粒',
                        'name': '牛肉粒'
                    },
                    {
                        'code': '猪肉干',
                        'name': '猪肉干'
                    }
                ],
                'code': '肉干肉脯/豆干',
                'name': '肉干肉脯/豆干'
            },
            {
                'sub_categorys': [
                    {
                        'code': '鱿鱼足',
                        'name': '鱿鱼足'
                    },
                    {
                        'code': '鱿鱼丝',
                        'name': '鱿鱼丝'
                    },
                    {
                        'code': '墨鱼/乌贼',
                        'name': '墨鱼/乌贼'
                    },
                    {
                        'code': '鱿鱼仔',
                        'name': '鱿鱼仔'
                    },
                    {
                        'code': '鱿鱼片',
                        'name': '鱿鱼片'
                    }
                ],
                'code': '鱿鱼丝/鱼干',
                'name': '鱿鱼丝/鱼干'
            }
        ],
        'code': '休闲食品',
        'name': '休闲食品'
    },
    {
        'sub_categorys': [
            {
                'sub_categorys': [

                ],
                'code': '进口奶品',
                'name': '进口奶品'
            },
            {
                'sub_categorys': [

                ],
                'code': '国产奶品',
                'name': '国产奶品'
            },
            {
                'sub_categorys': [

                ],
                'code': '奶粉',
                'name': '奶粉'
            },
            {
                'sub_categorys': [

                ],
                'code': '有机奶',
                'name': '有机奶'
            },
            {
                'sub_categorys': [

                ],
                'code': '原料奶',
                'name': '原料奶'
            }
        ],
        'code': '奶类食品',
        'name': '奶类食品'
    },
    {
        'sub_categorys': [
            {
                'sub_categorys': [

                ],
                'code': '菌菇类',
                'name': '菌菇类'
            },
            {
                'sub_categorys': [

                ],
                'code': '腌干海产',
                'name': '腌干海产'
            },
            {
                'sub_categorys': [

                ],
                'code': '汤料',
                'name': '汤料'
            },
            {
                'sub_categorys': [

                ],
                'code': '豆类',
                'name': '豆类'
            },
            {
                'sub_categorys': [

                ],
                'code': '干菜/菜干',
                'name': '干菜/菜干'
            },
            {
                'sub_categorys': [

                ],
                'code': '干果/果干',
                'name': '干果/果干'
            },
            {
                'sub_categorys': [

                ],
                'code': '豆制品',
                'name': '豆制品'
            },
            {
                'sub_categorys': [

                ],
                'code': '腊味',
                'name': '腊味'
            }
        ],
        'code': '天然干货',
        'name': '天然干货'
    },
    {
        'sub_categorys': [
            {
                'sub_categorys': [

                ],
                'code': '白茶',
                'name': '白茶'
            },
            {
                'sub_categorys': [

                ],
                'code': '红茶',
                'name': '红茶'
            },
            {
                'sub_categorys': [

                ],
                'code': '绿茶',
                'name': '绿茶'
            }
        ],
        'code': '精选茗茶',
        'name': '精选茗茶'
    }
]


async def init_goods_category():
    async with async_session() as db:
        await db.execute(delete(GoodsCategory))
        for lev1_cat in row1_data:
            lev1_cat_obj = GoodsCategory(name=lev1_cat['name'], code=lev1_cat['code'])
            db.add(lev1_cat_obj)
            await db.flush()
            for lev2_cat in lev1_cat['sub_categorys']:
                lev2_cat_obj = GoodsCategory(name=lev2_cat['name'], code=lev2_cat['code'], parent_id=lev1_cat_obj.id)
                db.add(lev2_cat_obj)
                await db.flush()
                for lev3_cat in lev1_cat['sub_categorys']:
                    lev3_cat_obj = GoodsCategory(name=lev3_cat['name'], code=lev3_cat['code'], parent_id=lev2_cat_obj.id)
                    db.add(lev3_cat_obj)
                    await db.flush()
        await db.commit()

#!/usr/bin/env python
# encoding: utf-8

row2_data = [
    {
        'images': [
            'goods/images/1_P_1449024889889.jpg',
            'goods/images/1_P_1449024889264.jpg',
            'goods/images/1_P_1449024889726.jpg',
            'goods/images/1_P_1449024889018.jpg',
            'goods/images/1_P_1449024889287.jpg'
        ],
        'categorys': [
            '首页',
            '生鲜食品',
            '根茎类'
        ],
        'market_price': '￥232元',
        'name': '新鲜水果甜蜜香脆单果约800克',
        'desc': '食用百香果可以增加胃部饱腹感，减少余热量的摄入，还可以吸附胆固醇和胆汁之类有机分子，抑制人体对脂肪的吸收。因此，长期食用有利于改善人体营养吸收结构，降低体内脂肪，塑造健康优美体态。',
        'sale_price': '￥156元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/2_P_1448945810202.jpg',
            'goods/images/2_P_1448945810814.jpg'
        ],
        'categorys': [
            '首页',
            '生鲜食品',
            '海鲜水产'
        ],
        'market_price': '￥106元',
        'name': '田然牛肉大黄瓜条生鲜牛肉冷冻真空黄牛',
        'desc': '前腿+后腿+羊排共8斤，原生态大山放牧羊羔，曾经的皇室贡品，央视推荐，2005年北京招待全球财金首脑。五层专用包装箱+真空包装+冰袋+保鲜箱+顺丰冷链发货，路途保质期8天',
        'sale_price': '￥88元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/7_P_1448945104883.jpg',
            'goods/images/7_P_1448945104734.jpg'
        ],
        'categorys': [
            '首页',
            '生鲜食品',
            '叶菜类'
        ],
        'market_price': '￥286元',
        'name': '酣畅家庭菲力牛排10片澳洲生鲜牛肉团购套餐',
        'desc': None,
        'sale_price': '￥238元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/47_P_1448946213263.jpg',
            'goods/images/47_P_1448946213157.jpg'
        ],
        'categorys': [
            '首页',
            '生鲜食品',
            '根茎类'
        ],
        'market_price': '￥156元',
        'name': '日本蒜蓉粉丝扇贝270克6只装',
        'desc': None,
        'sale_price': '￥108元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/10_P_1448944572085.jpg',
            'goods/images/10_P_1448944572532.jpg',
            'goods/images/10_P_1448944572872.jpg'
        ],
        'categorys': [
            '首页',
            '生鲜食品',
            '海鲜水产'
        ],
        'market_price': '￥106元',
        'name': '内蒙新鲜牛肉1斤清真生鲜牛肉火锅食材',
        'desc': None,
        'sale_price': '￥88元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/4_P_1448945381985.jpg',
            'goods/images/4_P_1448945381013.jpg'
        ],
        'categorys': [
            '首页',
            '生鲜食品',
            '茄果类'
        ],
        'market_price': '￥90元',
        'name': '乌拉圭进口牛肉卷特级肥牛卷',
        'desc': None,
        'sale_price': '￥75元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/8_P_1448945032810.jpg',
            'goods/images/8_P_1448945032646.jpg'
        ],
        'categorys': [
            '首页',
            '生鲜食品',
            '进口生鲜'
        ],
        'market_price': '￥150元',
        'name': '五星眼肉牛排套餐8片装原味原切生鲜牛肉',
        'desc': None,
        'sale_price': '￥125元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/11_P_1448944388277.jpg',
            'goods/images/11_P_1448944388034.jpg',
            'goods/images/11_P_1448944388201.jpg'
        ],
        'categorys': [
            '首页',
            '生鲜食品',
            '海鲜水产'
        ],
        'market_price': '￥31元',
        'name': '澳洲进口120天谷饲牛仔骨4份原味生鲜',
        'desc': None,
        'sale_price': '￥26元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/6_P_1448945167279.jpg',
            'goods/images/6_P_1448945167015.jpg'
        ],
        'categorys': [
            '首页',
            '生鲜食品',
            '菌菇类'
        ],
        'market_price': '￥239元',
        'name': '潮香村澳洲进口牛排家庭团购套餐20片',
        'desc': None,
        'sale_price': '￥199元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/9_P_1448944791617.jpg',
            'goods/images/9_P_1448944791129.jpg',
            'goods/images/9_P_1448944791077.jpg',
            'goods/images/9_P_1448944791229.jpg'
        ],
        'categorys': [
            '首页',
            '生鲜食品',
            '根茎类'
        ],
        'market_price': '￥202元',
        'name': '爱食派内蒙古呼伦贝尔冷冻生鲜牛腱子肉1000g',
        'desc': None,
        'sale_price': '￥168元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/3_P_1448945490837.jpg',
            'goods/images/3_P_1448945490084.jpg'
        ],
        'categorys': [
            '首页',
            '生鲜食品',
            '精品肉类'
        ],
        'market_price': '￥306元',
        'name': '澳洲进口牛尾巴300g新鲜肥牛肉',
        'desc': '新鲜羊羔肉整只共15斤，原生态大山放牧羊羔，曾经的皇室贡品，央视推荐，2005年北京招待全球财金首脑。五层专用包装箱+真空包装+冰袋+保鲜箱+顺丰冷链发货，路途保质期8天',
        'sale_price': '￥255元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/48_P_1448943988970.jpg',
            'goods/images/48_P_1448943988898.jpg',
            'goods/images/48_P_1448943988439.jpg'
        ],
        'categorys': [
            '首页',
            '生鲜食品',
            '海鲜水产'
        ],
        'market_price': '￥126元',
        'name': '新疆巴尔鲁克生鲜牛排眼肉牛扒1200g',
        'desc': None,
        'sale_price': '￥88元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/5_P_1448945270390.jpg',
            'goods/images/5_P_1448945270067.jpg',
            'goods/images/5_P_1448945270432.jpg'
        ],
        'categorys': [
            '首页',
            '生鲜食品',
            '蛋制品'
        ],
        'market_price': '￥144元',
        'name': '澳洲进口安格斯牛切片上脑牛排1000g',
        'desc': '澳大利亚是国际公认的没有疯牛病和口蹄疫的国家。为了保持澳大利亚产品的高标准，澳大利亚牛肉业和各级政府共同努力简历了严格的标准和体系，以保证生产的整体化和产品的可追溯性',
        'sale_price': '￥120元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'images/201705/goods_img/53_P_1495068879687.jpg'
        ],
        'categorys': [
            '首页',
            '生鲜食品',
            '茄果类'
        ],
        'market_price': '￥120元',
        'name': '帐篷出租',
        'desc': None,
        'sale_price': '￥100元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/16_P_1448947194687.jpg'
        ],
        'categorys': [
            '首页',
            '酒水饮料',
            '红酒'
        ],
        'market_price': '￥23元',
        'name': '52度茅台集团国隆双喜酒500mlx6',
        'desc': '贵州茅台酒厂（集团）保健酒业有限公司生产，是以“龙”字打头的酒水。中国龙文化上下8000年，源远而流长，龙的形象是一种符号、一种意绪、一种血肉相联的情感。',
        'sale_price': '￥19元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/14_P_1448947354031.jpg',
            'goods/images/14_P_1448947354433.jpg'
        ],
        'categorys': [
            '首页',
            '酒水饮料',
            '饮料/水'
        ],
        'market_price': '￥43元',
        'name': '52度水井坊臻酿八號500ml',
        'desc': None,
        'sale_price': '￥36元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/12_P_1448947547989.jpg'
        ],
        'categorys': [
            '首页',
            '酒水饮料',
            '其他酒品'
        ],
        'market_price': '￥190元',
        'name': '53度茅台仁酒500ml',
        'desc': None,
        'sale_price': '￥158元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/46_P_1448946598711.jpg',
            'goods/images/46_P_1448946598301.jpg'
        ],
        'categorys': [
            '首页',
            '酒水饮料',
            '葡萄酒'
        ],
        'market_price': '￥38元',
        'name': '双响炮洋酒JimBeamwhiskey美国白占边',
        'desc': None,
        'sale_price': '￥28元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/21_P_1448946793276.jpg',
            'goods/images/21_P_1448946793153.jpg'
        ],
        'categorys': [
            '首页',
            '酒水饮料',
            '饮料/水'
        ],
        'market_price': '￥55元',
        'name': '西夫拉姆进口洋酒小酒版',
        'desc': None,
        'sale_price': '￥46元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/15_P_1448947257324.jpg',
            'goods/images/15_P_1448947257580.jpg'
        ],
        'categorys': [
            '首页',
            '酒水饮料',
            '洋酒'
        ],
        'market_price': '￥22元',
        'name': '茅台53度飞天茅台500ml',
        'desc': None,
        'sale_price': '￥18元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/13_P_1448947460386.jpg',
            'goods/images/13_P_1448947460276.jpg',
            'goods/images/13_P_1448947460353.jpg'
        ],
        'categorys': [
            '首页',
            '酒水饮料',
            '葡萄酒'
        ],
        'market_price': '￥42元',
        'name': '52度兰陵·紫气东来1600mL山东名酒',
        'desc': None,
        'sale_price': '￥35元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/50_P_1448946543091.jpg',
            'goods/images/50_P_1448946542182.jpg'
        ],
        'categorys': [
            '首页',
            '酒水饮料',
            '饮料/水'
        ],
        'market_price': '￥24元',
        'name': 'JohnnieWalker尊尼获加黑牌威士忌',
        'desc': None,
        'sale_price': '￥20元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/51_P_1448946466595.jpg',
            'goods/images/51_P_1448946466208.jpg'
        ],
        'categorys': [
            '首页',
            '酒水饮料',
            '洋酒'
        ],
        'market_price': '￥31元',
        'name': '人头马CLUB特优香槟干邑350ml',
        'desc': None,
        'sale_price': '￥26元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/17_P_1448947102246.jpg'
        ],
        'categorys': [
            '首页',
            '酒水饮料',
            '啤酒'
        ],
        'market_price': '￥54元',
        'name': '张裕干红葡萄酒750ml*6支',
        'desc': None,
        'sale_price': '￥45元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/20_P_1448946850602.jpg'
        ],
        'categorys': [
            '首页',
            '酒水饮料',
            '葡萄酒'
        ],
        'market_price': '￥46元',
        'name': '原瓶原装进口洋酒烈酒法国云鹿XO白兰地',
        'desc': None,
        'sale_price': '￥38元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/19_P_1448946951581.jpg',
            'goods/images/19_P_1448946951726.jpg'
        ],
        'categorys': [
            '首页',
            '酒水饮料',
            '白酒'
        ],
        'market_price': '￥82元',
        'name': '法国原装进口圣贝克干红葡萄酒750ml',
        'desc': None,
        'sale_price': '￥68元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/18_P_1448947011435.jpg'
        ],
        'categorys': [
            '首页',
            '酒水饮料',
            '白酒'
        ],
        'market_price': '￥67元',
        'name': '法国百利威干红葡萄酒AOP级6支装',
        'desc': None,
        'sale_price': '￥56元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/22_P_1448946729629.jpg'
        ],
        'categorys': [
            '首页',
            '酒水饮料',
            '洋酒'
        ],
        'market_price': '￥71元',
        'name': '芝华士12年苏格兰威士忌700ml',
        'desc': None,
        'sale_price': '￥59元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/45_P_1448946661303.jpg'
        ],
        'categorys': [
            '首页',
            '酒水饮料',
            '饮料/水'
        ],
        'market_price': '￥31元',
        'name': '深蓝伏特加巴维兰利口酒送预调酒',
        'desc': None,
        'sale_price': '￥18元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/32_P_1448948525620.jpg'
        ],
        'categorys': [
            '首页',
            '蔬菜水果',
            '精选蔬菜'
        ],
        'market_price': '￥43元',
        'name': '赣南脐橙特级果10斤装',
        'desc': None,
        'sale_price': '￥36元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/30_P_1448948663450.jpg',
            'goods/images/30_P_1448948662571.jpg',
            'goods/images/30_P_1448948663221.jpg'
        ],
        'categorys': [
            '首页',
            '蔬菜水果',
            '进口水果'
        ],
        'market_price': '￥11元',
        'name': '泰国菠萝蜜16-18斤1个装',
        'desc': '【懒人吃法】菠萝蜜果肉，冰袋保鲜，收货就吃，冰爽Q脆甜，2斤装，全国顺丰空运包邮，发出后48小时内可达，一线城市基本隔天可达',
        'sale_price': '￥9元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/31_P_1448948598947.jpg',
            'goods/images/31_P_1448948598475.jpg'
        ],
        'categorys': [
            '首页',
            '蔬菜水果',
            '国产水果'
        ],
        'market_price': '￥22元',
        'name': '四川双流草莓新鲜水果礼盒2盒',
        'desc': None,
        'sale_price': '￥18元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/35_P_1448948333610.jpg',
            'goods/images/35_P_1448948333313.jpg'
        ],
        'categorys': [
            '首页',
            '蔬菜水果',
            '有机蔬菜'
        ],
        'market_price': '￥67元',
        'name': '新鲜头茬非洲冰草冰菜',
        'desc': None,
        'sale_price': '￥56元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/36_P_1448948234405.jpg',
            'goods/images/36_P_1448948234250.jpg'
        ],
        'categorys': [
            '首页',
            '蔬菜水果',
            '有机蔬菜'
        ],
        'market_price': '￥6元',
        'name': '仿真蔬菜水果果蔬菜模型',
        'desc': None,
        'sale_price': '￥5元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/33_P_1448948479966.jpg',
            'goods/images/33_P_1448948479886.jpg'
        ],
        'categorys': [
            '首页',
            '蔬菜水果',
            '精选蔬菜'
        ],
        'market_price': '￥28元',
        'name': '现摘芭乐番石榴台湾珍珠芭乐',
        'desc': '''海南产精品释迦果,
        释迦是水果中的贵族,
        产量少,
        味道很甜,
        奶香十足,
        非常可口,
        果裹果园顺丰空运,
        保证新鲜.果子个大,
        一斤1-2个左右,
        大个头的果子更尽兴!
        ''',
        'sale_price': '￥23元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/34_P_1448948399009.jpg'
        ],
        'categorys': [
            '首页',
            '蔬菜水果',
            '国产水果'
        ],
        'market_price': '￥46元',
        'name': '潍坊萝卜5斤/箱礼盒',
        'desc': '脐橙规格是65-90MM左右（标准果果径平均70MM左右，精品果果径平均80MM左右），一斤大概有2-4个左右，脐橙产自江西省赣州市信丰县安西镇，全过程都是采用农家有机肥种植，生态天然',
        'sale_price': '￥38元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/43_P_1448948762645.jpg'
        ],
        'categorys': [
            '首页',
            '休闲食品'
        ],
        'market_price': '￥154元',
        'name': '休闲零食膨化食品焦糖/奶油/椒麻味',
        'desc': None,
        'sale_price': '￥99元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/38_P_1448949220255.jpg'
        ],
        'categorys': [
            '首页',
            '奶类食品',
            '奶粉'
        ],
        'market_price': '￥84元',
        'name': '蒙牛未来星儿童成长牛奶骨力型190ml*15盒',
        'desc': None,
        'sale_price': '￥70元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/44_P_1448948850187.jpg'
        ],
        'categorys': [
            '首页',
            '奶类食品',
            '进口奶品'
        ],
        'market_price': '￥70元',
        'name': '蒙牛特仑苏有机奶250ml×12盒',
        'desc': None,
        'sale_price': '￥32元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'images/201511/goods_img/49_P_1448162819889.jpg'
        ],
        'categorys': [
            '首页',
            '奶类食品'
        ],
        'market_price': '￥1元',
        'name': '1元支付测试商品',
        'desc': None,
        'sale_price': '￥1元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/40_P_1448949038702.jpg'
        ],
        'categorys': [
            '首页',
            '奶类食品',
            '进口奶品'
        ],
        'market_price': '￥70元',
        'name': '德运全脂新鲜纯牛奶1L*10盒装整箱',
        'desc': None,
        'sale_price': '￥58元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/39_P_1448949115481.jpg'
        ],
        'categorys': [
            '首页',
            '奶类食品',
            '有机奶'
        ],
        'market_price': '￥38元',
        'name': '木糖醇红枣早餐奶即食豆奶粉538g',
        'desc': None,
        'sale_price': '￥32元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/41_P_1448948980358.jpg'
        ],
        'categorys': [
            '首页',
            '奶类食品',
            '原料奶'
        ],
        'market_price': '￥26元',
        'name': '高钙液体奶200ml*24盒',
        'desc': None,
        'sale_price': '￥22元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/37_P_1448949284365.jpg'
        ],
        'categorys': [
            '首页',
            '奶类食品',
            '国产奶品'
        ],
        'market_price': '￥720元',
        'name': '新西兰进口全脂奶粉900g',
        'desc': None,
        'sale_price': '￥600元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'images': [
            'goods/images/42_P_1448948895193.jpg'
        ],
        'categorys': [
            '首页',
            '奶类食品',
            '进口奶品'
        ],
        'market_price': '￥43元',
        'name': '伊利官方直营全脂营养舒化奶250ml*12盒*2提',
        'desc': None,
        'sale_price': '￥36元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
{
        'sale_price': '￥156元',
        'images': [
            'goods/images/27_P_1448947771805.jpg'
        ],
        'market_price': '￥187元',
        'categorys': [
            '首页',
            '粮油副食',
            '厨房调料'
        ],
        'desc': None,
        'name': '维纳斯橄榄菜籽油5L/桶',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'sale_price': '￥15元',
        'images': [
            'goods/images/23_P_1448948070348.jpg'
        ],
        'market_price': '￥18元',
        'categorys': [
            '首页',
            '粮油副食',
            '食用油'
        ],
        'desc': None,
        'name': '糙米450gx3包粮油米面',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'sale_price': '￥45元',
        'images': [
            'goods/images/26_P_1448947825754.jpg'
        ],
        'market_price': '￥54元',
        'categorys': [
            '首页',
            '粮油副食',
            '调味品'
        ],
        'desc': None,
        'name': '精炼一级大豆油5L色拉油粮油食用油',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'sale_price': '￥26元',
        'images': [
            'goods/images/28_P_1448947699948.jpg',
            'goods/images/28_P_1448947699777.jpg'
        ],
        'market_price': '￥31元',
        'categorys': [
            '首页',
            '粮油副食',
            '南北干货'
        ],
        'desc': None,
        'name': '橄榄玉米油5L*2桶',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'sale_price': '￥9元',
        'images': [
            'goods/images/24_P_1448948023823.jpg',
            'goods/images/24_P_1448948023977.jpg'
        ],
        'market_price': '￥11元',
        'categorys': [
            '首页',
            '粮油副食',
            '方便速食'
        ],
        'desc': None,
        'name': '山西黑米农家黑米4斤',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'sale_price': '￥12元',
        'images': [
            'goods/images/25_P_1448947875346.jpg'
        ],
        'market_price': '￥14元',
        'categorys': [
            '首页',
            '粮油副食',
            '米面杂粮'
        ],
        'desc': None,
        'name': '稻园牌稻米油粮油米糠油绿色植物油',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        'sale_price': '￥12元',
        'images': [
            'goods/images/29_P_1448947631994.jpg'
        ],
        'market_price': '￥14元',
        'categorys': [
            '首页',
            '粮油副食',
            '食用油'
        ],
        'desc': None,
        'name': '融氏纯玉米胚芽油5l桶',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    }
]


async def init_goods():
    async with async_session() as db:
        await db.execute(delete(Goods))
        for row in row2_data:
            cate_id = await db.scalar(select(GoodsCategory.id).where(GoodsCategory.name==row['categorys'][-1]))
            obj = Goods(goods_name=row['name'],
                  market_price=int(row['market_price'][1:-1]),
                  goods_brief=row['desc'],
                  goods_sn=uuid.uuid4(),
                  shop_price=int(row['sale_price'][1:-1]),
                  category_id=cate_id)
            db.add(obj)
        await db.commit()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_goods())
