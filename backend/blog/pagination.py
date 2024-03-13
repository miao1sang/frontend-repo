from rest_framework.pagination import PageNumberPagination


class APIViewPageNumberPaginations():
    class APIViewBasePaginations(PageNumberPagination):
        page_size = 2  # 每页数据量
        page_query_param = 'page'  # ?page=1跳转页
        max_page_size = 10  # 每页最大数据量
        page_size_query_param = 'size'

    def __init__(self, request, serializer, queryset):
        """
        :param request: 当前的请求
        :param serializer:  模型类的序列化器
        :param queryset:  要操作的模型对象
        """
        self.request = request
        self.serializer = serializer
        self.queryset = queryset

    def start(self):
        # 1、实例分页对象
        paginat = self.APIViewBasePaginations()
        # 2、拿到分页后的数据
        page_list = paginat.paginate_queryset(queryset=self.queryset, request=self.request, view=self)
        # 3、对分页后的数据将进行序列化
        ser = self.serializer(instance=page_list, many=True)
        count = paginat.page.paginator.count  # 总数据量
        next_page = 1 if paginat.get_next_link() else 0  # 有下一页，返回1，没有返回0
        previous_page = 1 if paginat.get_previous_link() else 0  # 有上一页时，返回1，没有返回0
        page_size = paginat.page_size  # 每页大小
        pages = count // page_size  # 总页数
        current_page = self.request.query_params.get('page')
        try:
            current_page = int(current_page)
        except Exception as e:
            current_page = 'error'
        if count % page_size:
            pages += 1
        return {
            'data': ser.data,  # 当前页的数据
            'next': next_page,  # 是否有下一页
            'previous': previous_page,  # 是否有上一页
            'count': count,  # 总数据量
            'pages': pages,  # 总页数
            'current_page': current_page  # 当前的页数
        }
