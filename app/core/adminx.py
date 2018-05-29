# -*- coding: utf-8 -*-
__author__ = 'fg615'

import xadmin

from .models import Product, Price, ProductHasPrice

"""
class PriceInline(object):
    model = Price
    extra = 0
"""

'''
    def get_extra(self, request, obj=None, **kwargs):
        """Dynamically sets the number of extra forms. 0 if the related object
        already exists or the extra configuration otherwise."""
        if obj:
            # Don't add any extra forms if the related object already exists.
            return 0
        return self.extra
        '''
'''
class ProductInline(object):
    model = Product
    extra = 0
'''

class ProductPriceAdmin(object):
    list_display = ['product', 'price', 'comments']
    search_fields = ['product', 'price', 'comments']
    list_filter = ['product', 'price', 'comments']
    #ordering = ['price_value']
        # readonly_fields = ['material_id', 'type']
    #list_editable = ['price_value', 'currency', 'type']



class ProductAdmin(object):
    list_display = ['material_id', 'name', 'desc', 'detail', 'type']
    search_fields = ['material_id', 'name', 'desc', 'type']
    list_filter = ['material_id', 'name', 'desc', 'type']
    ordering = ['-type']
    #readonly_fields = ['material_id', 'type']
    list_editable = ['desc']
    # exclude = ['fav_nums']
    #inlines = [PriceInline]
    #style_fields = {"detail":"ueditor"}
    #import_excel = True


class PriceAdmin(object):
    list_display = ['price_value', 'currency', 'type']
    search_fields = ['price_value', 'currency', 'type']
    list_filter = ['price_value', 'currency', 'type']
    ordering = ['price_value']
        # readonly_fields = ['material_id', 'type']
    list_editable = ['price_value', 'currency', 'type']
        # exclude = ['fav_nums']
    #inlines = [ProductInline]
        #style_fields = {"detail": "ueditor"}
       #import_excel = True
    """
    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):
        #在保存课程的时候统计课程机构的课程数
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()

    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            pass
        return super(CourseAdmin, self).post(request, args, kwargs)
"""
"""
class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    ordering = ['-click_nums']
    readonly_fields = ['click_nums']
    exclude = ['fav_nums']
    inlines = [LessonInline, CourseResourceInline]

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']
    model_icon = 'fa fa-film'


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course', 'name', 'download', 'add_time']

"""


class GlobalSettings(object):
    site_title = 'runming'  # 标题
    site_footer = 'runming'  # 页尾
    menu_style = 'accordion'  # 设置左侧菜单  折叠样式


class BaseSetting(object):
    enable_themes = True  # 使用主题
    use_bootswatch = True

from xadmin import views

xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(Product, ProductAdmin)
xadmin.site.register(Price, PriceAdmin)
xadmin.site.register(ProductHasPrice, ProductPriceAdmin)
#xadmin.site.register(Lesson, LessonAdmin)
#xadmin.site.register(Video, VideoAdmin)
#xadmin.site.register(CourseResource, CourseResourceAdmin)